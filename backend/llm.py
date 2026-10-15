"""Shared setup for every agent: the model (OpenAI through Portkey), the MCP server, and prompt loading.

All shop facts come from the campus-customs MCP server (mcp_server/server.py) over data/campus_customs_new.db.
Each agent only gets the MCP tools on its own allow-list.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

BASE_DIR = Path(__file__).resolve().parent
HW_DIR = BASE_DIR.parent
PROMPTS_DIR = BASE_DIR / "prompts"

# One MCP server shared by the whole team (started with `async with campus_customs:` in team.py).
# A .py path starts the server over stdio with the same Python the backend runs in (the venv in ~/venvs/hw5).
campus_customs = MCPToolset(HW_DIR / "mcp_server" / "server.py")


class MissingApiKey(RuntimeError):
    """PORTKEY_API_KEY isn't set."""


def make_model() -> OpenAIChatModel:
    """OpenAI model called through Portkey. The key comes from PORTKEY_API_KEY in the root .env file."""
    for folder in (BASE_DIR, HW_DIR, HW_DIR.parent):
        load_dotenv(folder / ".env")
    key = os.getenv("PORTKEY_API_KEY")
    if not key:
        raise MissingApiKey("PORTKEY_API_KEY is not set. Add it to your .env file.")
    client = AsyncOpenAI(
        api_key=key,
        base_url="https://api.portkey.ai/v1",
        default_headers={"x-portkey-api-key": key},
    )
    return OpenAIChatModel("gpt-5.6-luna", provider=OpenAIProvider(openai_client=client))


def load_prompt(name: str) -> str:
    """Read prompts/<name>.md fresh each time, so edits apply without restarting."""
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def tools_for(*names: str):
    """The MCP server, limited to the named tools."""
    allowed = set(names)
    return campus_customs.filtered(lambda ctx, tool: tool.name in allowed)
