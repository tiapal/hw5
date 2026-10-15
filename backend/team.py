"""Wires the five agents together so they can delegate to each other, and runs tickets.

Who can ask whom (matches the prompts):
  Boss -> Ina, Ama, Father, Jervis      Ina -> Ama      Father -> Ama      Jervis -> nobody
Guards against runaway loops: a depth cap on delegation, a cap on total model requests, and a time limit.
"""
import asyncio
import uuid
from dataclasses import replace

from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

import accounting
import audit
import boss
import customer_service
import facilities
import inventory
from llm import campus_customs
from models import BossResult, Deps, HumanApprover

MAX_DEPTH = 3
MAX_MODEL_REQUESTS = 40
TIME_LIMIT_SECONDS = 4 * 60  # the Boss prompt's "never more than 4 minutes"

team: dict[str, Agent] = {}


async def _run_agent(name: str, prompt: str, deps: Deps, **run_kwargs):
    """Run one agent loop, appending every step to output/audit_trail.json as it happens."""
    step = 0
    async with team[name].iter(prompt, deps=deps, **run_kwargs) as run:
        async for node in run:
            step += 1
            audit.record_node(deps.run_id, deps.ticket_id, name, deps.depth, step, node)
    return run.result


def _connect(caller: str, callee: str, tool_name: str, doc: str) -> None:
    """Give `caller` a tool that runs `callee` with a question and returns its report."""

    async def ask(ctx: RunContext[Deps], question: str) -> str:
        if ctx.deps.depth >= MAX_DEPTH:
            return "Too many agents deep. Stop delegating and answer with what you have."
        ctx.deps.log.append(f"{caller} -> {callee}: {question}")
        result = await _run_agent(callee, question, replace(ctx.deps, depth=ctx.deps.depth + 1), usage=ctx.usage)
        ctx.deps.log.append(f"{callee} -> {caller}: {result.output.model_dump_json()}")
        return result.output.model_dump_json()

    ask.__name__ = tool_name
    ask.__doc__ = doc
    team[caller].tool(ask)


def build_team() -> dict[str, Agent]:
    team.clear()
    team.update(
        {
            "Boss": boss.build(),
            "Inventory Ina": inventory.build(),
            "Accounting Ama": accounting.build(),
            "Facilities Father": facilities.build(),
            "Customer Service Jervis": customer_service.build(),
        }
    )
    _connect("Boss", "Inventory Ina", "ask_inventory_ina", "Ask Inventory Ina about stock (by SKU and size) or vendors.")
    _connect("Boss", "Accounting Ama", "ask_accounting_ama", "Ask Accounting Ama about cash, invoices, prices and margins, or tell him a human approved a payment so he can pay it.")
    _connect("Boss", "Facilities Father", "ask_facilities_father", "Send Facilities Father a lease or rent request.")
    _connect("Boss", "Customer Service Jervis", "ask_customer_service_jervis", "Give Jervis the facts and what you want to say; he returns a draft customer message.")
    _connect("Inventory Ina", "Accounting Ama", "ask_accounting_ama", "Ask Accounting Ama whether a vendor has an open unpaid invoice, or hand him a shortage so he can prepare the purchase.")
    _connect("Facilities Father", "Accounting Ama", "ask_accounting_ama", "Ask Accounting Ama to prepare the rent payment (amount, landlord, due date) and check the cash.")
    return team


async def run_ticket(ticket_id: int, human: HumanApprover, run_id: str | None = None) -> tuple[BossResult, list[str]]:
    """Run the Boss on one ticket. Returns his result and the Table's transcript."""
    deps = Deps(human=human, run_id=run_id or uuid.uuid4().hex[:8], ticket_id=ticket_id)
    audit.append({"run_id": deps.run_id, "ticket_id": ticket_id, "agent": "Boss", "kind": "run_start"})
    try:
        result = await asyncio.wait_for(
            _run_agent(
                "Boss", f"Handle ticket {ticket_id}.", deps,
                usage_limits=UsageLimits(request_limit=MAX_MODEL_REQUESTS),
            ),
            timeout=TIME_LIMIT_SECONDS,
        )
    except BaseException as error:  # a stop (limit, timeout, crash) is part of the audit story too
        audit.append({"run_id": deps.run_id, "ticket_id": ticket_id, "agent": "Boss", "kind": "run_stopped", "reason": f"{type(error).__name__}: {error}"})
        raise
    audit.append({"run_id": deps.run_id, "ticket_id": ticket_id, "agent": "Boss", "kind": "run_end"})
    return result.output, deps.log


async def run_all(ticket_ids: list[int], human: HumanApprover) -> list[tuple[BossResult, list[str]]]:
    build_team()
    out = []
    async with campus_customs:
        for ticket_id in ticket_ids:
            out.append(await run_ticket(ticket_id, human))
    return out
