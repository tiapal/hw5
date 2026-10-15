"""Customer Service Jervis: loads prompts/customer_service.md, returns DraftMessage, and may only use the MCP tools listed below."""
from pydantic_ai import Agent

from llm import load_prompt, make_model, tools_for
from models import DraftMessage, Deps

NAME = "Customer Service Jervis"
MCP_TOOLS = ()
TOOL_NOTES = """
HOW YOUR TOOLS WORK (code notes, not shop policy):
- You have no tools. Everything you know is in the Boss's brief.
"""


def build() -> Agent[Deps, DraftMessage]:
    agent = Agent(
        make_model(),
        deps_type=Deps,
        output_type=DraftMessage,
        toolsets=[],
        retries=2,
    )

    @agent.instructions
    def system_prompt() -> str:
        return load_prompt("customer_service") + TOOL_NOTES

    return agent
