"""Inventory Ina: loads prompts/inventory.md, returns StockReport, and may only use the MCP tools listed below."""
from pydantic_ai import Agent

from llm import load_prompt, make_model, tools_for
from models import StockReport, Deps

NAME = "Inventory Ina"
MCP_TOOLS = ("get_ticket", "get_stock", "list_vendors", "get_today")
TOOL_NOTES = """
HOW YOUR TOOLS WORK (code notes, not shop policy):
- Your shop facts come only from your MCP tools: get_ticket, get_stock(sku, size), list_vendors, get_today.
- To ask whether a vendor has an open unpaid invoice, use ask_accounting_ama. You cannot read invoices yourself.
- You can only propose orders. You have no tool that spends money.
"""


def build() -> Agent[Deps, StockReport]:
    agent = Agent(
        make_model(),
        deps_type=Deps,
        output_type=StockReport,
        toolsets=[tools_for(*MCP_TOOLS)],
        retries=2,
    )

    @agent.instructions
    def system_prompt() -> str:
        return load_prompt("inventory") + TOOL_NOTES

    return agent
