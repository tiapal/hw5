"""Reset the database, then have the agent team work the open tickets. Every purchase or payment asks you first.

Usage:  ~/venvs/hw5/bin/python run_tickets.py [ticket ids...]      (default: 101 102 103)
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "mcp_server"))

import shop_db  # only used here to reset the working copy before a run; agents never import it
from team import run_all


async def ask_at_the_table(kind: str, ref: str, description: str) -> bool:
    answer = await asyncio.to_thread(input, f"\n[THE TABLE] Approve? {description}\n  (y/n): ")
    return answer.strip().lower() in ("y", "yes")


async def main() -> None:
    ids = [int(a) for a in sys.argv[1:]] or [101, 102, 103]
    print(shop_db.reset_database())
    for result, log in await run_all(ids, ask_at_the_table):
        print("\n--- Table transcript ---")
        print("\n".join(log))
        print("\n=== Ticket", result.ticket_id, "===")
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
