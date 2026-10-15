"""Append-only audit trail: output/audit_trail.json.

Every agent loop step (the prompt it got, each model reply, each tool call and what came back, each
delegation, the human's decision, the final answer) is appended as one entry. The file is a JSON list that
is read, extended and written back; it is never wiped between runs.
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

AUDIT_FILE = Path(__file__).resolve().parent.parent / "output" / "audit_trail.json"
MAX_TEXT = 2000  # long tool results are cut so the file stays readable; the cut is marked

# Customer-facing text must never ask for these (shop safety rules). Matches are flagged in the trail.
UNSAFE_ASK = re.compile(r"\b(ssn|social security|card number|credit card|debit card|cvv|cvc|password|passcode|pin)\b", re.I)


def _clip(value) -> str:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + f"...[cut, {len(text)} chars total]"


def append(entry: dict) -> None:
    """Add one entry to the end of the trail (creating the file the first time)."""
    entry = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), **entry}
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    trail: list = []
    if AUDIT_FILE.exists() and AUDIT_FILE.stat().st_size:
        try:
            trail = json.loads(AUDIT_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # Never lose history: keep the unreadable file aside and start a fresh list.
            AUDIT_FILE.rename(AUDIT_FILE.with_suffix(f".corrupt-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"))
    trail.append(entry)
    tmp = AUDIT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(trail, indent=2, default=str), encoding="utf-8")
    os.replace(tmp, AUDIT_FILE)


def record_node(run_id: str, ticket_id: int, agent: str, depth: int, step: int, node) -> None:
    """Write the entries for one step of one agent's loop. `node` comes from agent.iter()."""
    from pydantic_ai import Agent
    from pydantic_ai.messages import TextPart, ToolCallPart, ToolReturnPart, UserPromptPart

    base = {"run_id": run_id, "ticket_id": ticket_id, "agent": agent, "depth": depth, "step": step}
    if Agent.is_user_prompt_node(node):
        append({**base, "kind": "prompt", "text": _clip(str(node.user_prompt))})
    elif Agent.is_model_request_node(node):
        for part in node.request.parts:
            if isinstance(part, ToolReturnPart):
                append({**base, "kind": "tool_result", "tool": part.tool_name, "result": _clip(part.content)})
            elif isinstance(part, UserPromptPart):
                append({**base, "kind": "model_request", "text": _clip(str(part.content))})
    elif Agent.is_call_tools_node(node):
        for part in node.model_response.parts:
            if isinstance(part, ToolCallPart):
                append({**base, "kind": "tool_call", "tool": part.tool_name, "args": _clip(part.args)})
            elif isinstance(part, TextPart):
                append({**base, "kind": "model_text", "text": _clip(part.content)})
    elif Agent.is_end_node(node):
        output = node.data.output if hasattr(node.data, "output") else node.data
        text = output.model_dump_json() if hasattr(output, "model_dump_json") else str(output)
        append({**base, "kind": "final_output", "output": _clip(text)})
        flag_unsafe(run_id, ticket_id, agent, depth, text)


def flag_unsafe(run_id: str, ticket_id: int, agent: str, depth: int, text: str) -> None:
    """Flag (in the trail) any agent output that mentions card details, SSNs or passwords."""
    match = UNSAFE_ASK.search(text)
    if match:
        append(
            {
                "run_id": run_id, "ticket_id": ticket_id, "agent": agent, "depth": depth,
                "kind": "guardrail_flag",
                "detail": f"Output mentions '{match.group(0)}'. Agents must never ask customers for or share card details, SSNs or passwords.",
            }
        )
