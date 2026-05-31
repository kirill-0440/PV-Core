from __future__ import annotations

from .types import Obligation, Proposal, Witness


def generate_refund_obligations(proposal: Proposal, witnesses: list[Witness]) -> list[Obligation]:
    del proposal, witnesses
    return [
        Obligation(
            id="O-ORDER-EXISTS",
            claim="The referenced order exists.",
            verifier_type="order_exists",
        ),
        Obligation(
            id="O-CUSTOMER-OWNS-ORDER",
            claim="The requesting customer owns the referenced order.",
            verifier_type="customer_owns_order",
        ),
        Obligation(
            id="O-PAYMENT-CAPTURED",
            claim="The order payment is captured and refundable.",
            verifier_type="payment_captured",
        ),
        Obligation(
            id="O-REFUND-WINDOW-OPEN",
            claim="The refund request is inside the active policy window.",
            verifier_type="refund_window_open",
        ),
        Obligation(
            id="O-NO-DUPLICATE-REFUND",
            claim="No previous refund exists for this order.",
            verifier_type="no_duplicate_refund",
        ),
    ]
