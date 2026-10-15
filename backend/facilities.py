"""Facilities Father: loads prompts/facilities.md, returns FacilitiesReport, and may only use the MCP tools listed below."""
from pydantic_ai import Agent

from llm import load_prompt, make_model, tools_for
from models import FacilitiesReport, Deps

NAME = "Facilities Father"
MCP_TOOLS = ("get_ticket", "get_lease", "get_today", "list_payments")
TOOL_NOTES = """
HOW YOUR TOOLS WORK (code notes, not shop policy):
- Your shop facts come only from your MCP tools: get_ticket, get_lease, get_today, list_payments.
- To get rent paid, use ask_accounting_ama. You cannot pay anything yourself.
"""


def build() -> Agent[Deps, FacilitiesReport]:
    agent = Agent(
        make_model(),
        deps_type=Deps,
        output_type=FacilitiesReport,
        toolsets=[tools_for(*MCP_TOOLS)],
        retries=2,
    )

    @agent.instructions
    def system_prompt() -> str:
        return load_prompt("facilities") + TOOL_NOTES

    return agent
