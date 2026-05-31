from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


VerificationResult = Literal["accepted", "rejected"]


@dataclass(frozen=True)
class Goal:
    context: dict[str, Any]
    intent: str
    constraints: list[str]
    success_type: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Goal":
        return cls(
            context=dict(data.get("context", {})),
            intent=str(data.get("intent", "")),
            constraints=[str(item) for item in data.get("constraints", [])],
            success_type=str(data.get("success_type", "")),
        )


@dataclass(frozen=True)
class Proposal:
    goal: Goal
    construction: dict[str, Any]
    assumptions: list[str]


@dataclass(frozen=True)
class Witness:
    supports: str
    evidence: dict[str, Any]
    provenance: dict[str, Any]


@dataclass(frozen=True)
class Obligation:
    id: str
    claim: str
    verifier_type: str
    status: str = "open"


@dataclass(frozen=True)
class Verification:
    obligation_id: str
    result: VerificationResult
    certificate: dict[str, Any] | None = None


@dataclass(frozen=True)
class Commit:
    proposal: Proposal
    witnesses: list[Witness]
    verifications: list[Verification]
    trusted_state: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "pvcore.commit.v0_1",
            "status": "verified",
            **asdict(self),
        }


@dataclass(frozen=True)
class ObstructionReport:
    goal: Goal
    failed_at: str
    obstruction: dict[str, Any]
    repair_hints: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "pvcore.obstruction_report.v0_1",
            "status": "obstructed",
            **asdict(self),
        }
