"""FastMCP server for Campus Customs.

The first three tools (tickets 101, 102, 103) only read. The rest read one table each, and the pay_* /
order_* tools write to data/campus_customs_new.db. The logic lives in shop_db.py, which the agents share.
"""
import sys
from pathlib import Path

from fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shop_db as db  # noqa: E402

mcp = FastMCP("campus-customs")


@mcp.tool
def check_tee_stock_and_reprint_invoice() -> dict:
    """Ticket 101: stock of the requested tee size, plus the linked reprint invoice and its vendor."""
    ticket = db.get_ticket(101)
    invoice = db.get_invoice(ticket["invoice_id"])
    vendor = [v for v in db.list_vendors() if v["id"] == invoice.get("vendor_id")]
    return {
        "ticket": ticket,
        "requested_item_stock": db.get_stock(ticket["sku"], ticket["size"]),
        "linked_invoice": [invoice] if invoice else [],
        "invoice_vendor": vendor,
    }


@mcp.tool
def check_rent_due_and_cash() -> dict:
    """Ticket 102: the lease behind the rent notice, today's date, and the checking balance."""
    ticket = db.get_ticket(102)
    lease = db.get_lease(ticket["lease_id"])
    return {
        "ticket": ticket,
        "lease": [lease] if lease else [],
        "desk": [{"date_today": db.get_today()}],
        "cash_accounts": db.get_cash(),
        "payments_on_record": db.list_payments(),
    }


@mcp.tool
def check_hoodie_bulk_pricing_and_stock() -> dict:
    """Ticket 103: list price and unit cost of the hoodie, and stock in the requested size vs. the quantity asked for."""
    ticket = db.get_ticket(103)
    return {
        "ticket": ticket,
        "pricing": db.get_pricing(ticket["sku"]),
        "requested_size_stock": db.get_stock(ticket["sku"], ticket["size"]),
        "qty_requested": ticket["qty"],
    }


# ---- general read tools ----

@mcp.tool
def get_today() -> str:
    """The shop's 'today' from the desk table (not the real date)."""
    return db.get_today()


@mcp.tool
def list_open_tickets() -> list[dict]:
    """All open tickets."""
    return db.list_open_tickets()


@mcp.tool
def get_ticket(ticket_id: int) -> dict:
    """One ticket by id."""
    return db.get_ticket(ticket_id)


@mcp.tool
def get_stock(sku: str, size: str) -> list[dict]:
    """Stock for one SKU and one size (stock is counted per size)."""
    return db.get_stock(sku, size)


@mcp.tool
def list_vendors() -> list[dict]:
    """Every vendor with its specialty and lead time in days."""
    return db.list_vendors()


@mcp.tool
def get_vendor_invoices(vendor_id: int) -> list[dict]:
    """All invoices from one vendor. An open one blocks new orders from that vendor."""
    return db.get_vendor_invoices(vendor_id)


@mcp.tool
def get_invoice(invoice_id: int) -> dict:
    """One invoice by id."""
    return db.get_invoice(invoice_id)


@mcp.tool
def get_cash() -> list[dict]:
    """Cash account balances."""
    return db.get_cash()


@mcp.tool
def get_pricing(sku: str) -> list[dict]:
    """List price and unit cost for a SKU."""
    return db.get_pricing(sku)


@mcp.tool
def get_lease(lease_id: int) -> dict:
    """One lease by id: landlord, monthly rent, next due date."""
    return db.get_lease(lease_id)


@mcp.tool
def list_payments() -> list[dict]:
    """Payments already made."""
    return db.list_payments()


# ---- write tools (cash only goes out; each one refuses instead of breaking a rule) ----

@mcp.tool
def record_approval(kind: str, ref: str, approved_by: str) -> dict:
    """Record a human's yes for one action (kind: invoice, rent or purchase; ref: invoice id, lease id, or
    'sku|size|qty|vendor_id'). Only the Boss calls this, and only after the human at the Table said yes."""
    return db.record_approval(kind, ref, approved_by)


@mcp.tool
def pay_invoice(invoice_id: int) -> dict:
    """Pay a vendor invoice in full. Refuses without a recorded human approval, or if cash is short."""
    return db.pay_invoice(invoice_id)


@mcp.tool
def pay_rent(lease_id: int) -> dict:
    """Pay one month of rent. Refuses without a recorded human approval, or if cash is short."""
    return db.pay_rent(lease_id)


@mcp.tool
def order_stock(sku: str, size: str, qty: int, vendor_id: int) -> dict:
    """Pay a vendor for stock (qty x unit cost). Refuses without a recorded human approval, if cash is short,
    or if the vendor has an open unpaid invoice."""
    return db.order_stock(sku, size, qty, vendor_id)


@mcp.tool
def list_tickets() -> list[dict]:
    """Every ticket, open or resolved."""
    return db.list_tickets()


@mcp.tool
def resolve_ticket(ticket_id: int) -> dict:
    """Mark a ticket resolved. Called by the backend once a run finishes with nothing waiting for approval."""
    return db.resolve_ticket(ticket_id)


@mcp.tool
def reset_database() -> str:
    """Copy the original database over the working copy (fresh start). Not given to any agent."""
    return db.reset_database()


if __name__ == "__main__":
    mcp.run()
