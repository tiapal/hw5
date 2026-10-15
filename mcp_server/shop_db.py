"""Plain functions that read and write data/campus_customs_new.db.

The MCP server (server.py) and the PydanticAI agents (backend/) both call these, so the shop rules
live in one place. Reads open the database read-only. Writes happen only in the pay_* / order_* functions,
and every one of them refuses (returns ok=False) instead of breaking a rule.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "campus_customs_new.db"
ORIGINAL_DB_PATH = DB_PATH.with_name("campus_customs.db")
ACCOUNT = "checking"


def _query(sql: str, params: tuple = ()) -> list[dict]:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(sql, params)]
    finally:
        conn.close()


# ---------- reads ----------

def get_today() -> str:
    return _query("SELECT date_today FROM desk")[0]["date_today"]


def get_ticket(ticket_id: int) -> dict:
    rows = _query("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    return rows[0] if rows else {}


def list_open_tickets() -> list[dict]:
    return _query("SELECT * FROM tickets WHERE status = 'open' ORDER BY id")


def get_stock(sku: str, size: str) -> list[dict]:
    return _query(
        "SELECT sku, name, size, qty, location FROM inventory WHERE sku = ? AND size = ?", (sku, size)
    )


def list_vendors() -> list[dict]:
    return _query("SELECT * FROM vendors ORDER BY id")


def get_invoice(invoice_id: int) -> dict:
    rows = _query("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    return rows[0] if rows else {}


def get_vendor_invoices(vendor_id: int) -> list[dict]:
    return _query("SELECT * FROM invoices WHERE vendor_id = ? ORDER BY id", (vendor_id,))


def get_cash() -> list[dict]:
    return _query("SELECT * FROM cash_accounts")


def get_pricing(sku: str) -> list[dict]:
    return _query("SELECT * FROM pricing WHERE sku = ?", (sku,))


def get_lease(lease_id: int) -> dict:
    rows = _query("SELECT * FROM leases WHERE id = ?", (lease_id,))
    return rows[0] if rows else {}


def list_payments() -> list[dict]:
    return _query("SELECT * FROM payments ORDER BY id")


# ---------- approvals: the Boss records a human's yes; pay tools consume it ----------

def _ensure_approvals(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS approvals (id INTEGER PRIMARY KEY, kind TEXT NOT NULL, ref TEXT NOT NULL, "
        "approved_by TEXT NOT NULL, used INTEGER NOT NULL DEFAULT 0)"
    )


def record_approval(kind: str, ref: str, approved_by: str) -> dict:
    """Record that a human approved one action. kind is invoice, rent or purchase; ref says which one."""
    if kind not in ("invoice", "rent", "purchase") or not approved_by.strip():
        return {"ok": False, "reason": "kind must be invoice, rent or purchase, and approved_by must be a human's name."}
    conn = sqlite3.connect(DB_PATH)
    try:
        _ensure_approvals(conn)
        conn.execute("INSERT INTO approvals (kind, ref, approved_by) VALUES (?, ?, ?)", (kind, ref, approved_by))
        conn.commit()
        return {"ok": True, "kind": kind, "ref": ref, "approved_by": approved_by}
    finally:
        conn.close()


def _take_approval(kind: str, ref: str) -> str | None:
    """Return the approver's name and mark that approval used, or None if the human never approved it."""
    conn = sqlite3.connect(DB_PATH)
    try:
        _ensure_approvals(conn)
        row = conn.execute(
            "SELECT id, approved_by FROM approvals WHERE kind = ? AND ref = ? AND used = 0 ORDER BY id LIMIT 1",
            (kind, ref),
        ).fetchone()
        if not row:
            return None
        conn.execute("UPDATE approvals SET used = 1 WHERE id = ?", (row[0],))
        conn.commit()
        return row[1]
    finally:
        conn.close()


def purchase_ref(sku: str, size: str, qty: int, vendor_id: int) -> str:
    return f"{sku}|{size}|{qty}|{vendor_id}"


# ---------- writes (cash only ever goes out) ----------

def _pay(kind: str, ref_id: int | None, amount: float, approved_by: str) -> dict:
    """Record one payment and lower the balance, in a single transaction. Refuses if cash is short."""
    if not approved_by.strip():
        return {"ok": False, "reason": "A human approval (approved_by) is required for any payment."}
    if amount <= 0:
        return {"ok": False, "reason": "The amount must be more than zero."}
    conn = sqlite3.connect(DB_PATH)
    try:
        balance = conn.execute("SELECT balance FROM cash_accounts WHERE name = ?", (ACCOUNT,)).fetchone()[0]
        if amount > balance:
            return {
                "ok": False,
                "reason": f"Not enough cash: balance is {balance:.2f}, payment is {amount:.2f}. Balances never go negative.",
            }
        today = conn.execute("SELECT date_today FROM desk").fetchone()[0]
        conn.execute("UPDATE cash_accounts SET balance = balance - ?, date = ? WHERE name = ?", (amount, today, ACCOUNT))
        cur = conn.execute(
            "INSERT INTO payments (kind, ref_id, amount, account, paid_at, approved_by) VALUES (?, ?, ?, ?, ?, ?)",
            (kind, ref_id, amount, ACCOUNT, today, approved_by),
        )
        conn.commit()
        return {"ok": True, "payment_id": cur.lastrowid, "amount": amount, "new_balance": balance - amount}
    finally:
        conn.close()


def pay_invoice(invoice_id: int) -> dict:
    """Pay a vendor invoice in full, then mark it paid. Refuses if it is not open or cash is short."""
    invoice = get_invoice(invoice_id)
    if not invoice:
        return {"ok": False, "reason": f"Invoice {invoice_id} does not exist."}
    if invoice["status"] != "open":
        return {"ok": False, "reason": f"Invoice {invoice_id} is already {invoice['status']}."}
    if invoice["amount"] > get_cash()[0]["balance"]:
        return _pay("invoice", invoice_id, invoice["amount"], "unused")  # refusal message only
    approver = _take_approval("invoice", str(invoice_id))
    if not approver:
        return {"ok": False, "reason": "No human approval is recorded for this invoice. Ask the Boss to get one."}
    result = _pay("invoice", invoice_id, invoice["amount"], approver)
    if result["ok"]:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE invoices SET status = 'paid' WHERE id = ?", (invoice_id,))
        conn.commit()
        conn.close()
    return result


def pay_rent(lease_id: int) -> dict:
    """Pay one month of rent for a lease. Refuses if cash is short."""
    lease = get_lease(lease_id)
    if not lease:
        return {"ok": False, "reason": f"Lease {lease_id} does not exist."}
    if lease["monthly_rent"] > get_cash()[0]["balance"]:
        return _pay("rent", lease_id, lease["monthly_rent"], "unused")  # refusal message only
    approver = _take_approval("rent", str(lease_id))
    if not approver:
        return {"ok": False, "reason": "No human approval is recorded for this rent payment. Ask the Boss to get one."}
    return _pay("rent", lease_id, lease["monthly_rent"], approver)


def order_stock(sku: str, size: str, qty: int, vendor_id: int) -> dict:
    """Pay a vendor for a stock order (qty x unit cost). Refuses if the vendor has an open unpaid invoice.

    New stock arrives after the vendor's lead time, so this does not change the inventory table.
    """
    if qty <= 0:
        return {"ok": False, "reason": "The quantity must be more than zero."}
    vendors = {v["id"]: v for v in list_vendors()}
    if vendor_id not in vendors:
        return {"ok": False, "reason": f"Vendor {vendor_id} does not exist."}
    open_invoices = [i for i in get_vendor_invoices(vendor_id) if i["status"] == "open"]
    if open_invoices:
        ids = ", ".join(str(i["id"]) for i in open_invoices)
        return {"ok": False, "reason": f"Vendor has an open unpaid invoice ({ids}); they will not ship until it is paid."}
    pricing = get_pricing(sku)
    if not pricing:
        return {"ok": False, "reason": f"No pricing for {sku}, so the cost is unknown."}
    cost = pricing[0]["unit_cost"] * qty
    if cost > get_cash()[0]["balance"]:
        return _pay("purchase", None, cost, "unused")  # refusal message only
    approver = _take_approval("purchase", purchase_ref(sku, size, qty, vendor_id))
    if not approver:
        return {"ok": False, "reason": "No human approval is recorded for this order. Ask the Boss to get one."}
    result = _pay("purchase", None, cost, approver)
    if result["ok"]:
        result["lead_days"] = vendors[vendor_id]["lead_days"]
    return result


def list_tickets() -> list[dict]:
    return _query("SELECT * FROM tickets ORDER BY id")


def resolve_ticket(ticket_id: int) -> dict:
    """Mark an open ticket resolved. Nothing else about the ticket changes."""
    ticket = get_ticket(ticket_id)
    if not ticket:
        return {"ok": False, "reason": f"Ticket {ticket_id} does not exist."}
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE tickets SET status = 'resolved' WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    return {"ok": True, "ticket_id": ticket_id, "status": "resolved"}


def reset_database() -> str:
    """Copy the original database over the working copy. Do this before a full run."""
    import shutil

    shutil.copyfile(ORIGINAL_DB_PATH, DB_PATH)
    return f"Reset {DB_PATH.name} from {ORIGINAL_DB_PATH.name}."
