# Campus Customs Harness

Source: `data/campus_customs_new.db` (a copy of `data/campus_customs.db`; the original is untouched). Every shop fact reaches the agents through the MCP server in `mcp_server/server.py`.

## Tables

### tickets (3 rows)
Fields: `id`, `type`, `requester`, `subject`, `sku`, `size`, `qty`, `lease_id`, `invoice_id`, `status`, `notes`, `created_at`
Why it matters: it is the work queue; each open ticket points to the other tables through `sku`/`size`, `lease_id`, and `invoice_id`.

### inventory (10 rows)
Fields: `sku`, `name`, `size`, `qty`, `location`
Why it matters: it shows what is in stock per size and where it sits, which decides whether an order can ship now.

### pricing (4 rows)
Fields: `sku`, `unit_cost`, `list_price`
Why it matters: it gives cost and list price per product, so any discount can be checked against what the shop pays.

### vendors (3 rows)
Fields: `id`, `name`, `specialty`, `lead_days`
Why it matters: it says who supplies or ships what and how many days they need.

### invoices (1 row)
Fields: `id`, `vendor_id`, `amount`, `due_date`, `status`, `description`
Why it matters: it records money owed to vendors and links to `vendors` through `vendor_id`. An open invoice blocks new orders from that vendor.

### leases (1 row)
Fields: `id`, `space_name`, `landlord`, `monthly_rent`, `next_due`, `notes`
Why it matters: it holds the rent amount and due date for the shop space.

### cash_accounts (1 row)
Fields: `name`, `balance`, `date`
Why it matters: it shows how much cash is available before any bill is paid.

### payments (0 rows at start)
Fields: `id`, `kind`, `ref_id`, `amount`, `account`, `paid_at`, `approved_by`
Why it matters: it records payments already made and who approved them; the pay tools add a row each time money goes out.

### desk (1 row)
Fields: `date_today`, `notes`
Why it matters: it holds the shop's "today" (2026-08-31), which every "due in N days" judgment depends on.

### approvals (added in Problem 5; created on first use, not in the original database)
Fields: `id`, `kind`, `ref`, `approved_by`, `used`
Why it matters: it holds the human's yes for one purchase or payment; a pay tool refuses unless a matching unused approval exists, then marks it used. A database reset removes it.

## Agents (`backend/`)

Prompts live in `backend/prompts/<agent>.md`; data types in `backend/models.py`; delegation and the run loop in `backend/team.py`.

| Agent | File | Can ask | MCP tools it may use |
|---|---|---|---|
| Boss | `boss.py` | Ina, Ama, Father, Jervis, the human (`ask_human`) | `get_today`, `list_open_tickets`, `get_ticket` (and records the human's approval through `record_approval` inside `ask_human`) |
| Inventory Ina | `inventory.py` | Ama | `get_ticket`, `get_stock`, `list_vendors`, `get_today` |
| Accounting Ama | `accounting.py` | nobody | `get_today`, `get_cash`, `get_invoice`, `get_vendor_invoices`, `get_pricing`, `list_payments`, `get_lease`, `pay_invoice`, `pay_rent`, `order_stock` |
| Facilities Father | `facilities.py` | Ama | `get_ticket`, `get_lease`, `get_today`, `list_payments` |
| Customer Service Jervis | `customer_service.py` | nobody | none (writes drafts from the Boss's brief) |

Every agent loop step is appended to `output/audit_trail.json` (never wiped).

## MCP tools (`mcp_server/server.py`)

| Tool | Table(s) it uses | Writes? | What it is for |
|---|---|---|---|
| `check_tee_stock_and_reprint_invoice` | tickets, inventory, invoices, vendors | no | Ticket 101: size S tee stock (0) plus linked invoice 501 and its vendor. |
| `check_rent_due_and_cash` | tickets, leases, desk, cash_accounts, payments | no | Ticket 102: the lease, today's date, the checking balance, payments on record. |
| `check_hoodie_bulk_pricing_and_stock` | tickets, pricing, inventory | no | Ticket 103: hoodie cost and list price, size M stock vs. 20 requested. |
| `get_today` | desk | no | The shop's "today". |
| `list_open_tickets` | tickets | no | All open tickets. |
| `get_ticket` | tickets | no | One ticket by id. |
| `list_tickets` | tickets | no | Every ticket, open or resolved (Problem 7; used by the backend, not the agents). |
| `get_stock` | inventory | no | Stock for one SKU and size. |
| `list_vendors` | vendors | no | Vendors with specialty and lead days. |
| `get_vendor_invoices` | invoices | no | Every invoice from one vendor. |
| `get_invoice` | invoices | no | One invoice by id. |
| `get_cash` | cash_accounts | no | Cash balances. |
| `get_pricing` | pricing | no | List price and unit cost for a SKU. |
| `get_lease` | leases | no | One lease by id. |
| `list_payments` | payments | no | Payments already made. |
| `record_approval` | approvals | yes | Records the human's yes (through the Boss's `ask_human` in the terminal run, or the backend's approve route). |
| `pay_invoice` | invoices, approvals, cash_accounts, payments, desk | yes | Pays a vendor invoice in full and marks it paid. |
| `pay_rent` | leases, approvals, cash_accounts, payments, desk | yes | Pays one month of rent. |
| `order_stock` | vendors, invoices, pricing, approvals, cash_accounts, payments, desk | yes | Pays a vendor for qty x unit cost; stock arrives after the lead time, so `inventory` does not change. |

| `resolve_ticket` | tickets | yes | Marks a ticket resolved (Problem 7; the backend calls it when a run ends with nothing waiting for approval). |
| `reset_database` | all tables (file copy of the original database) | yes | Puts the database back to the original values (Problem 7; backend and `run_tickets.py` only, never an agent). |

The first three tools were built in Problem 2; the rest were added in Problems 5 and 7.

## Backend routes (`backend/main.py`)

Start from `backend/` with `uvicorn main:app --reload --port 8000` (http://localhost:8000). Every route goes through the MCP tools above.

- `GET /tickets`: the three tickets, each `open` or `resolved`, with any payment waiting for approval and the last run.
- `POST /tickets/{ticket_id}/run`: starts the agent team on that ticket and returns a run id at once (one run at a time).
- `GET /events?limit=50&ticket_id=`: the most recent audit trail entries, i.e. what each agent said and which tools it used.
- `POST /approvals/{approval_id}/approve`: after a human clicks Approve, records the approval and makes the payment or purchase (the only route that changes cash).
- `POST /approvals/{approval_id}/deny`: after a human clicks Deny, nothing is paid; the denial is remembered so the Boss is not asked for the same thing again.
- `GET /cash`: the current checking balance from `cash_accounts`.
- `POST /reset`: puts the database back to the original values for a fresh run.

Agents only prepare a payment: when the Boss asks the human, the request shows up under `pending_approvals` on `GET /tickets` until someone approves it.

## Dashboard (`frontend/`)

A React + Vite + TypeScript board that only calls the routes above (backend at http://localhost:8000, which allows the page origin http://localhost:5173). Start it with `npm run dev` in `frontend/`.

- **Ticket pile** (left): the three tickets, open or resolved (pink RESOLVED stamp).
- **The desk** (middle): Start the team, a status banner, any payment waiting for a human with neutral grey **Approve & pay** and **Deny** buttons, the five agents at the table, and a "Who did what" summary per agent.
- **Ticket tape** (right): the full text of what each agent said and which tools they used, from `GET /events`.
- **Cash drawer** (top): the checking balance, which drops when an approved payment goes through.
- Design choices are in `output/design.md`; screenshots of the resolved tickets are in `output/resolved_board.html`.

## Safety

- Human approval is required for ANY purchase or payment; the pay tools refuse without a recorded approval.
- The pay tools refuse if cash is short, so the balance never goes negative. Cash only goes out; revenue is not modeled.
- A vendor with an open unpaid invoice gets no new orders.
- Never discount below unit cost; never invent numbers; "today" is `desk.date_today`.
- The 4 limit: at most 4 questions per specialist per ticket, 4 minutes per ticket, 3 levels of delegation, and 40 model calls per ticket.
- No real emails, calls or messages to vendors, landlords or customers; everything stays on the board.
- A customer's money may only be used for what they paid for.
- Never share card details, and never tell a customer to give us an SSN, card details or a password. These rules are in the agent prompts; any agent output that mentions them is also flagged in the audit trail.
- Customer messages stay short: Jervis does not share internal details (vendors, lead times, invoices, approvals, cost, cash), and an out-of-stock item gets one fixed message.
- A human can deny any request; the pay tools only ever act on a recorded human approval, and a denied request is never paid.
- The database is reset to the original values before a full run (`POST /reset`, or `run_tickets.py`).
