"""Boss: loads prompts/boss.md, returns BossResult. Delegates to all four specialists and asks the human."""
from pydantic_ai import Agent, RunContext

import audit
from llm import campus_customs, load_prompt, make_model, tools_for
from models import BossResult, Deps

NAME = "Boss"
MCP_TOOLS = ("get_today", "list_open_tickets", "get_ticket")
TOOL_NOTES = """
HOW YOUR TOOLS WORK (code notes, not shop policy):
- Read tickets with get_ticket / list_open_tickets. Delegate with ask_inventory_ina, ask_accounting_ama,
  ask_facilities_father and ask_customer_service_jervis. Each takes one clear question and returns that agent's report.
- ask_human is the Table. Use it before ANY purchase or payment: say exactly what would be paid, to whom, and how much.
  It returns approved, denied or pending. Only after "approved" may you tell Ama to pay. On "pending" the human decides
  later on the board: leave the payment unpaid, say it is waiting for approval, and finish your answer (human_approved null).
  For ask_human, kind is "invoice" (ref = invoice id), "rent" (ref = lease id) or "purchase" (ref = "sku|size|qty|vendor_id").
- Post your final answer as the BossResult.
"""


def build() -> Agent[Deps, BossResult]:
    agent = Agent(
        make_model(),
        deps_type=Deps,
        output_type=BossResult,
        toolsets=[tools_for(*MCP_TOOLS)],
        retries=2,
    )

    @agent.instructions
    def system_prompt() -> str:
        return load_prompt("boss") + TOOL_NOTES

    @agent.tool
    async def ask_human(ctx: RunContext[Deps], kind: str, ref: str, description: str) -> str:
        """Ask the human at the Table to approve one purchase or payment. Returns 'approved' or 'denied'."""
        if kind not in ("invoice", "rent", "purchase"):
            return "kind must be invoice, rent or purchase"
        yes = await ctx.deps.human(kind, ref, description)
        decision = "pending" if yes is None else "approved" if yes else "denied"
        ctx.deps.log.append(f"TABLE: {description} -> {decision}")
        audit.append(
            {"run_id": ctx.deps.run_id, "ticket_id": ctx.deps.ticket_id, "agent": "Boss", "kind": "human_decision",
             "approval_kind": kind, "ref": ref, "description": description, "decision": decision}
        )
        if yes is None:
            return "pending: the human has not decided yet. Do NOT tell Ama to pay. Report this payment as waiting for approval."
        if not yes:
            return "denied"
        # The approval is recorded in the database through the MCP server; Ama's pay tools check for it.
        await campus_customs.direct_call_tool("record_approval", {"kind": kind, "ref": ref, "approved_by": "human at the Table"})
        return "approved"

    return agent
