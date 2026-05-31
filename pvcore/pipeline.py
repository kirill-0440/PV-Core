from __future__ import annotations

from typing import Any

from .obligations import generate_refund_obligations
from .types import Commit, Goal, ObstructionReport, Proposal, Verification, Witness
from .verifiers import verify_all


def propose(goal: Goal) -> Proposal:
    if goal.intent != "refund_order":
        return Proposal(
            goal=goal,
            construction={"action": "refuse", "reason": "unsupported_intent"},
            assumptions=[],
        )
    return Proposal(
        goal=goal,
        construction={
            "action": "create_refund",
            "order_id": goal.context.get("order_id"),
            "customer_id": goal.context.get("customer_id"),
        },
        assumptions=["commerce records and policy witnesses are current for the request date"],
    )


def witness_search(goal: Goal, witness_records: list[dict[str, Any]]) -> list[Witness]:
    witnesses: list[Witness] = []
    for index, record in enumerate(witness_records):
        evidence = dict(record)
        witnesses.append(
            Witness(
                supports=goal.intent,
                evidence=evidence,
                provenance={
                    "source": evidence.get("source", "example-fixture"),
                    "index": index,
                },
            )
        )
    return witnesses


def generate_obligations(proposal: Proposal, witnesses: list[Witness]):
    if proposal.goal.intent == "refund_order":
        return generate_refund_obligations(proposal, witnesses)
    return []


def commit_or_obstruct(
    proposal: Proposal,
    witnesses: list[Witness],
    verifications: list[Verification],
) -> Commit | ObstructionReport:
    failed = [verification for verification in verifications if verification.result != "accepted"]
    if failed:
        return ObstructionReport(
            goal=proposal.goal,
            failed_at="verify",
            obstruction={
                "type": "failed_obligation",
                "failed_obligations": [item.obligation_id for item in failed],
                "certificates": [item.certificate for item in failed],
            },
            repair_hints=[
                "add missing witness records",
                "repair inconsistent commerce state",
                "escalate when policy or authority remains ambiguous",
            ],
        )
    return Commit(
        proposal=proposal,
        witnesses=witnesses,
        verifications=verifications,
        trusted_state={
            "trusted": True,
            "rule": "all obligations accepted",
        },
    )


def run_pvcore(goal: Goal, witness_records: list[dict[str, Any]]) -> Commit | ObstructionReport:
    proposal = propose(goal)
    witnesses = witness_search(goal, witness_records)
    obligations = generate_obligations(proposal, witnesses)
    verifications = verify_all(goal, obligations, witnesses)
    return commit_or_obstruct(proposal, witnesses, verifications)
