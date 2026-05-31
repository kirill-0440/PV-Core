# PVCore

Proof-Carrying Reasoning via Witness Geometry.

```yaml
title: PVCore Typed Blueprint
subtitle: Proof-Carrying Reasoning via Witness Geometry
version: 0.1
status: research-blueprint
audience:
  - AI agents
  - formal methods
  - Lean
  - category theory
  - knowledge systems
model_names:
  - local/open models if applicable
```

## Interface

```text
PVCore : Goal -> VerifiedCommit + ObstructionReport
```

PVCore accepts a goal and returns either a verified commit or an obstruction
report.

The system is designed for AI reasoning workflows where a bare answer is not
enough. Every trusted result must carry witnesses, obligations, verification
records, and residual obstructions.

## Core Flow

```text
Goal
  -> Proposal
  -> Witness
  -> Obligation
  -> Verification
  -> VerifiedCommit | ObstructionReport
```

The core rule is:

```text
No trusted answer without discharged obligations.
```

## Core Types

```lean
structure Goal where
  context      : Context
  intent       : Intent
  constraints  : List Constraint
  successType  : Type

structure Proposal where
  goal         : Goal
  construction : Construction
  assumptions  : List Assumption

structure Witness where
  supports     : Proposal
  evidence     : Evidence
  provenance   : Provenance

structure Obligation where
  generatedBy  : Proposal
  claim        : Claim
  verifierType : VerifierType
  status       : ObligationStatus

structure Verification where
  obligation   : Obligation
  result       : VerificationResult
  certificate  : Option Certificate

structure Commit where
  proposal      : Proposal
  witnesses     : List Witness
  verifications : List Verification
  trustedState  : TrustedState

structure ObstructionReport where
  goal          : Goal
  failedAt      : PipelineStage
  obstruction   : Obstruction
  repairHints   : List RepairHint
```

## Typed Execution

```lean
def runPVCore
  (g : Goal)
  : Either ObstructionReport Commit :=
  let p  := propose g
  let ws := witnessSearch p
  let os := generateObligations p ws
  let vs := verifyAll os
  commitOrObstruct p ws os vs
```

## Context Transport

PVCore treats reasoning as transport between contexts.

```lean
structure Transport where
  source      : Context
  target      : Context
  translation : Translation
  assumptions : List Assumption
  defect      : Option TransportDefect
```

A reasoning failure is not only a wrong answer. It can be a failed transport
between contexts.

## Transport Defects

```lean
inductive DefectKind where
  | missingWitness
  | incompatibleAssumptions
  | failedVerification
  | nonCommutingTransport
  | unresolvedObligation
```

Working slogan:

```text
Hallucination ~= unreported transport defect.
```

## Repository Layout

```text
PVCore/
  README.md
  blueprint.md
  docs/
    architecture.md
    open-problems.md
    insight.md
  lean/
    PVCore/
      Core.lean
      Goal.lean
      Witness.lean
      Obligation.lean
      Transport.lean
      Verification.lean
      Obstruction.lean
  examples/
    rag-example.md
    agent-example.md
    lean-example.md
```

## Public Insight

PVCore is a typed architecture for proof-carrying AI systems.

Instead of returning bare answers, the system returns answers equipped with
witnesses, obligations, verification records, and obstruction reports.

The goal is to move from:

```text
User -> LLM -> Answer
```

to:

```text
Goal -> Proposal -> Witness -> Obligation -> Verification -> Commit
```

This makes AI reasoning auditable, compositional, and suitable for formal
verification.

## Open Problems

```text
OP-001 Witness-valued semantics
OP-002 Obligation fibrations
OP-003 Context transport defects
OP-004 Institution-based AI
OP-005 Lean formalization
OP-006 Proof-carrying agents
```

## Status

This repository is currently a research blueprint with a minimal executable
commerce verifier example. It is not yet a complete verifier for arbitrary
reasoning tasks.

## Minimal Demo

Run the ECOM refund example:

```bash
PYTHONPATH=. python3 examples/ecom/run_refund.py
python3 -m unittest discover -s tests
```

The positive fixture returns a `pvcore.commit.v0_1` object. The duplicate-refund
fixture returns a `pvcore.obstruction_report.v0_1` object.
