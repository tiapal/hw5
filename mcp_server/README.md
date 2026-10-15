# Campus Customs MCP Server

A FastMCP server (`server.py`) that gives the Campus Customs agents their shop facts and a few guarded actions. The tool logic lives in `shop_db.py`, which only this server uses.

**Database:** `data/campus_customs_new.db` (a copy of `data/campus_customs.db`). Reads open it read-only. Only the write tools below change it, and `run_tickets.py` resets it from the original before a full run.

## Ticket tools (read only)

- `check_tee_stock_and_reprint_invoice` (ticket 101): stock for the requested tee size, plus the linked reprint invoice and its vendor.
- `check_rent_due_and_cash` (ticket 102): the lease, today's date, the checking balance, and any payments on record.
- `check_hoodie_bulk_pricing_and_stock` (ticket 103): hoodie cost and list price, plus stock in the requested size vs. quantity asked for.

## General read tools

- `get_today`: the shop's "today" from the desk table.
- `list_open_tickets`, `list_tickets`, `get_ticket`: the work queue.
- `get_stock`: stock for one SKU and size.
- `list_vendors`, `get_vendor_invoices`, `get_invoice`: vendors and what is owed to them.
- `get_cash`, `get_pricing`, `get_lease`, `list_payments`: balances, prices and costs, rent, payments made.

## Write tools (cash only goes out)

- `record_approval`: records a human's yes for one action. Only the Boss uses it, after the human at the Table approves.
- `pay_invoice`, `pay_rent`, `order_stock`: make a payment and update the cash balance and payments table. Each one refuses without a recorded approval, refuses if cash is short (the balance never goes negative), and `order_stock` also refuses if the vendor has an open unpaid invoice.

## Backend-only tools

- `resolve_ticket`: marks a ticket resolved (the backend calls it when a run ends with nothing waiting for approval).
- `reset_database`: copies the original database over the working copy. No agent is given this tool.

See `output/harness.md` for which table each tool uses and which agent may call it.
