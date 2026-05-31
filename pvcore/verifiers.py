from __future__ import annotations

from collections.abc import Callable
from datetime import date
from typing import Any

from .types import Goal, Obligation, Verification, Witness


def evidence_by_kind(witnesses: list[Witness], kind: str) -> list[dict[str, Any]]:
    return [w.evidence for w in witnesses if w.evidence.get("kind") == kind]


def _accepted(obligation: Obligation, evidence: dict[str, Any]) -> Verification:
    return Verification(
        obligation_id=obligation.id,
        result="accepted",
        certificate={"verifier": obligation.verifier_type, "evidence": evidence},
    )


def _rejected(obligation: Obligation, reason: str) -> Verification:
    return Verification(
        obligation_id=obligation.id,
        result="rejected",
        certificate={"verifier": obligation.verifier_type, "reason": reason},
    )


def verify_order_exists(goal: Goal, obligation: Obligation, witnesses: list[Witness]) -> Verification:
    order_id = goal.context.get("order_id")
    for order in evidence_by_kind(witnesses, "order"):
        if order.get("order_id") == order_id:
            return _accepted(obligation, {"order_id": order_id})
    return _rejected(obligation, f"order not found: {order_id}")


def verify_customer_owns_order(goal: Goal, obligation: Obligation, witnesses: list[Witness]) -> Verification:
    order_id = goal.context.get("order_id")
    customer_id = goal.context.get("customer_id")
    for order in evidence_by_kind(witnesses, "order"):
        if order.get("order_id") == order_id and order.get("customer_id") == customer_id:
            return _accepted(obligation, {"order_id": order_id, "customer_id": customer_id})
    return _rejected(obligation, "customer does not own order")


def verify_payment_captured(goal: Goal, obligation: Obligation, witnesses: list[Witness]) -> Verification:
    order_id = goal.context.get("order_id")
    for payment in evidence_by_kind(witnesses, "payment"):
        if payment.get("order_id") == order_id and payment.get("status") == "captured":
            return _accepted(obligation, {"order_id": order_id, "payment_status": "captured"})
    return _rejected(obligation, "payment is not captured")


def verify_refund_window_open(goal: Goal, obligation: Obligation, witnesses: list[Witness]) -> Verification:
    order_id = goal.context.get("order_id")
    request_date = date.fromisoformat(str(goal.context.get("request_date")))
    order_date: date | None = None
    for order in evidence_by_kind(witnesses, "order"):
        if order.get("order_id") == order_id:
            order_date = date.fromisoformat(str(order.get("created_at")))
            break
    if order_date is None:
        return _rejected(obligation, "order date missing")
    for policy in evidence_by_kind(witnesses, "policy"):
        if policy.get("policy_id") == goal.context.get("policy_id"):
            window_days = int(policy.get("refund_window_days", 0))
            elapsed = (request_date - order_date).days
            if 0 <= elapsed <= window_days:
                return _accepted(obligation, {"elapsed_days": elapsed, "window_days": window_days})
            return _rejected(obligation, f"refund window closed: elapsed={elapsed}, window={window_days}")
    return _rejected(obligation, "refund policy missing")


def verify_no_duplicate_refund(goal: Goal, obligation: Obligation, witnesses: list[Witness]) -> Verification:
    order_id = goal.context.get("order_id")
    for refund in evidence_by_kind(witnesses, "refund"):
        if refund.get("order_id") == order_id and refund.get("status") in {"created", "settled"}:
            return _rejected(obligation, f"duplicate refund exists: {refund.get('refund_id')}")
    return _accepted(obligation, {"order_id": order_id, "duplicate_refund": False})


VERIFIERS: dict[str, Callable[[Goal, Obligation, list[Witness]], Verification]] = {
    "order_exists": verify_order_exists,
    "customer_owns_order": verify_customer_owns_order,
    "payment_captured": verify_payment_captured,
    "refund_window_open": verify_refund_window_open,
    "no_duplicate_refund": verify_no_duplicate_refund,
}


def verify_all(goal: Goal, obligations: list[Obligation], witnesses: list[Witness]) -> list[Verification]:
    results: list[Verification] = []
    for obligation in obligations:
        verifier = VERIFIERS.get(obligation.verifier_type)
        if verifier is None:
            results.append(_rejected(obligation, f"unknown verifier: {obligation.verifier_type}"))
            continue
        results.append(verifier(goal, obligation, witnesses))
    return results
