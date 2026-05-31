# PVCore Typed Blueprint

## Interface

```text
PVCore : Goal -> VerifiedCommit + ObstructionReport
```

## Pipeline

```text
Goal
  -> Proposal
  -> Witness
  -> Obligation
  -> Verification
  -> VerifiedCommit | ObstructionReport
```

## Rule

```text
No trusted answer without discharged obligations.
```

## Minimal Implementation

The current implementation contains a small ECOM refund verifier. It accepts a
refund only when these obligations pass:

- order exists;
- customer owns order;
- payment is captured;
- refund window is open;
- no duplicate refund exists.

If an obligation fails, PVCore returns an obstruction report instead of an
unqualified answer.
