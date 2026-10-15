"""FastAPI backend for the dashboard.  Start it from this folder:  uvicorn main:app --reload --port 8000

Every shop fact and every change to cash goes through the campus-customs MCP server (the same one the agents use).
Agents only PREPARE payments. The approve route below is the only thing that makes money move.
"""
import asyncio
import json
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import audit
import team
from llm import campus_customs

# Waiting-for-human payment requests prepared by the agents, and the last run of each ticket (lives while the server runs).
approvals: dict[int, dict] = {}
last_runs: dict[int, dict] = {}
running: dict = {}  # {"ticket_id": ..., "run_id": ...} while an agent run is in progress


async def mcp(tool: str, args: dict | None = None):
    """Call one MCP tool and return its plain result."""
    result = await campus_customs.direct_call_tool(tool, args or {})
    if hasattr(result, "data") and result.data is not None:
        return result.data
    if hasattr(result, "structured_content") and result.structured_content is not None:
        content = result.structured_content
        return content.get("result", content) if isinstance(content, dict) else content
    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    team.build_team()
    async with campus_customs:  # starts the MCP server for the whole life of the backend
        yield


app = FastAPI(title="Campus Customs backend", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _pending_for(ticket_id: int) -> list[dict]:
    return [a for a in approvals.values() if a["ticket_id"] == ticket_id and a["status"] == "pending"]


@app.get("/tickets")
async def get_tickets():
    """The tickets, each open or resolved, with any payment waiting for approval and the last run."""
    tickets = await mcp("list_tickets")
    return [
        {
            "id": t["id"], "type": t["type"], "requester": t["requester"], "subject": t["subject"],
            "status": t["status"],  # open or resolved
            "running": running.get("ticket_id") == t["id"],
            "pending_approvals": _pending_for(t["id"]),
            "last_run": last_runs.get(t["id"]),
        }
        for t in tickets
    ]


async def _run(ticket_id: int, run_id: str) -> None:
    async def human(kind: str, ref: str, description: str):
        """The agents prepare a payment; it waits here for a human to click Approve or Deny."""
        if any(a["ticket_id"] == ticket_id and a["kind"] == kind and a["ref"] == ref and a["status"] == "denied" for a in approvals.values()):
            return False  # a human already said no to exactly this; do not ask again
        approval_id = len(approvals) + 1
        approvals[approval_id] = {
            "id": approval_id, "ticket_id": ticket_id, "run_id": run_id, "kind": kind, "ref": ref,
            "description": description, "status": "pending",
        }
        return None  # not decided yet

    try:
        result, _ = await team.run_ticket(ticket_id, human, run_id=run_id)
        last_runs[ticket_id] = {"run_id": run_id, "status": "finished", "result": result.model_dump()}
        if not _pending_for(ticket_id):  # nothing left waiting on a human, so the ticket is done
            await mcp("resolve_ticket", {"ticket_id": ticket_id})
    except BaseException as error:  # the stop is already written to the audit trail by team.run_ticket
        last_runs[ticket_id] = {"run_id": run_id, "status": "failed", "error": f"{type(error).__name__}: {error}"}
        if isinstance(error, asyncio.CancelledError):
            raise
    finally:
        running.clear()


@app.post("/tickets/{ticket_id}/run", status_code=202)
async def run_ticket(ticket_id: int):
    """Start the agent team on one ticket (returns at once; poll /events and /tickets to watch it)."""
    ticket_ids = [t["id"] for t in await mcp("list_tickets")]
    if ticket_id not in ticket_ids:
        raise HTTPException(404, f"Ticket {ticket_id} does not exist.")
    if running:
        raise HTTPException(409, f"A run is already in progress (ticket {running['ticket_id']}).")
    run_id = uuid.uuid4().hex[:8]
    running.update({"ticket_id": ticket_id, "run_id": run_id})
    last_runs[ticket_id] = {"run_id": run_id, "status": "running"}
    asyncio.create_task(_run(ticket_id, run_id))
    return {"run_id": run_id, "ticket_id": ticket_id, "status": "running"}


@app.get("/events")
async def get_events(limit: int = 50, ticket_id: int | None = None):
    """The most recent audit trail entries (what each agent said, which tools it used), newest last."""
    if not audit.AUDIT_FILE.exists() or not audit.AUDIT_FILE.stat().st_size:
        return []
    try:
        trail = json.loads(audit.AUDIT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if ticket_id is not None:
        trail = [e for e in trail if e.get("ticket_id") == ticket_id]
    return trail[-max(1, min(limit, 500)):]


@app.post("/approvals/{approval_id}/approve")
async def approve(approval_id: int):
    """A human clicked Approve. Record the approval and make the payment through the MCP pay tools."""
    request = approvals.get(approval_id)
    if not request:
        raise HTTPException(404, f"Approval {approval_id} does not exist.")
    if request["status"] != "pending":
        raise HTTPException(409, f"Approval {approval_id} is already {request['status']}.")

    kind, ref = request["kind"], request["ref"]
    await mcp("record_approval", {"kind": kind, "ref": ref, "approved_by": "human at the Table"})
    if kind == "invoice":
        paid = await mcp("pay_invoice", {"invoice_id": int(ref)})
    elif kind == "rent":
        paid = await mcp("pay_rent", {"lease_id": int(ref)})
    else:  # purchase: ref is "sku|size|qty|vendor_id"
        sku, size, qty, vendor_id = ref.split("|")
        paid = await mcp("order_stock", {"sku": sku, "size": size, "qty": int(qty), "vendor_id": int(vendor_id)})

    request["status"] = "paid" if paid.get("ok") else "refused"
    request["result"] = paid
    audit.append(
        {"run_id": request["run_id"], "ticket_id": request["ticket_id"], "agent": "human", "kind": "human_decision",
         "approval_kind": kind, "ref": ref, "description": request["description"],
         "decision": "approved", "payment_result": paid}
    )
    return request


@app.post("/approvals/{approval_id}/deny")
async def deny(approval_id: int):
    """A human clicked Deny. Nothing is paid; the agents will be told no if they ask for the same thing again."""
    request = approvals.get(approval_id)
    if not request:
        raise HTTPException(404, f"Approval {approval_id} does not exist.")
    if request["status"] != "pending":
        raise HTTPException(409, f"Approval {approval_id} is already {request['status']}.")
    request["status"] = "denied"
    audit.append(
        {"run_id": request["run_id"], "ticket_id": request["ticket_id"], "agent": "human", "kind": "human_decision",
         "approval_kind": request["kind"], "ref": request["ref"], "description": request["description"], "decision": "denied"}
    )
    return request


@app.get("/cash")
async def get_cash():
    """The current checking balance."""
    accounts = await mcp("get_cash")
    checking = next(a for a in accounts if a["name"] == "checking")
    return {"account": "checking", "balance": checking["balance"], "as_of": checking["date"]}


@app.post("/reset")
async def reset():
    """Put the database back to the original values for a fresh run."""
    if running:
        raise HTTPException(409, "A run is in progress. Wait for it to finish before resetting.")
    message = await mcp("reset_database")
    approvals.clear()
    last_runs.clear()
    audit.append({"kind": "database_reset", "agent": "backend", "detail": message})
    return {"message": message}
