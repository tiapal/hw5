"""Accounting Ama: loads prompts/accounting.md, returns AccountingReport, and may only use the MCP tools listed below."""
from pydantic_ai import Agent

from llm import load_prompt, make_model, tools_for
from models import AccountingReport, Deps

NAME = "Accounting Ama"
MCP_TOOLS = ("get_today", "get_cash", "get_invoice", "get_vendor_invoices", "get_pricing", "list_payments", "get_lease", "pay_invoice", "pay_rent", "order_stock")
TOOL_NOTES = """
HOW YOUR TOOLS WORK (code notes, not shop policy):
- Your shop facts come only from your MCP tools. pay_invoice, pay_rent and order_stock refuse unless the Boss has already got a human approval recorded, and they refuse if cash is short. If one refuses, report the refusal (payment_status "refused"); never try to work around it.
- Only call a pay tool after the Boss tells you the human approved that exact payment. Otherwise set payment_status "waiting_for_approval" and describe the payment for the Boss.
- order_stock needs the vendor_id, sku, size and qty Ina proposed.
"""


def build() -> Agent[Deps, AccountingReport]:
    agent = Agent(
        make_model(),
        deps_type=Deps,
        output_type=AccountingReport,
        toolsets=[tools_for(*MCP_TOOLS)],
        retries=2,
    )

    @agent.instructions
    def system_prompt() -> str:
        return load_prompt("accounting") + TOOL_NOTES

    return agent
