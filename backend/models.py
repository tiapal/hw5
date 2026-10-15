"""Data types for the Campus Customs agent team: what each agent hands back, and what they all share."""
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Literal

from pydantic import BaseModel, Field


class StockReport(BaseModel):
    """Inventory Ina's answer."""
    sku: str
    size: str
    on_hand: int | None = Field(description="Quantity in stock for that SKU and size, or null if unknown")
    location: str | None = None
    requested: int | None = None
    enough: bool | None = None
    shortage: int | None = Field(default=None, description="How many we are short, if any")
    vendor_name: str | None = None
    vendor_id: int | None = None
    lead_days: int | None = None
    vendor_has_open_invoice: bool | None = None
    proposed_order_qty: int | None = Field(default=None, description="What Ina proposes to order; the Boss approves or denies")
    notes: str = ""


class AccountingReport(BaseModel):
    """Accounting Ama's answer."""
    answer: str = Field(description="Plain answer to what was asked, using only numbers the tools returned")
    cash_balance: float | None = None
    invoice_id: int | None = None
    invoice_amount: float | None = None
    invoice_overdue: bool | None = None
    list_price: float | None = None
    unit_cost: float | None = None
    margin_per_item: float | None = None
    payment_status: Literal["none", "waiting_for_approval", "paid", "refused", "denied"] = "none"
    payment_detail: str = ""


class FacilitiesReport(BaseModel):
    """Facilities Father's answer."""
    lease_id: int | None = None
    landlord: str | None = None
    monthly_rent: float | None = None
    next_due: str | None = None
    today: str | None = None
    days_left: int | None = Field(default=None, description="Negative if overdue")
    payment_status: Literal["none", "requested_from_ama", "waiting_for_approval", "paid", "refused"] = "none"
    notes: str = ""


class DraftMessage(BaseModel):
    """Customer Service Jervis's answer."""
    message: str = Field(description="Draft message for the customer, ready for the Boss to post")
    facts_used: list[str] = Field(default_factory=list)
    missing_facts: list[str] = Field(default_factory=list)


class Evidence(BaseModel):
    fact: str
    source: Literal["Inventory Ina", "Accounting Ama", "Facilities Father", "Customer Service Jervis", "ticket", "human"]


class BossResult(BaseModel):
    """The Boss's final answer for one ticket, posted to the Table."""
    ticket_id: int
    decision: str = Field(description="One sentence")
    evidence: list[Evidence]
    money_spent: float = 0.0
    human_approved: bool | None = Field(default=None, description="null if no money was involved")
    customer_message: str = Field(description="The message Jervis drafted, as posted")


# Asks the human at the Table: (kind, ref, description). True = yes, False = no,
# None = not decided yet (the web board shows an Approve button and the human decides later).
HumanApprover = Callable[[str, str, str], Awaitable[bool | None]]


@dataclass
class Deps:
    """Shared by every agent in one ticket run."""
    human: HumanApprover
    run_id: str = ""  # one id per ticket run, written on every audit trail entry
    ticket_id: int = 0
    depth: int = 0  # how many agents deep the delegation is; capped so agents cannot loop forever
    log: list[str] = field(default_factory=list)  # the Table's transcript
