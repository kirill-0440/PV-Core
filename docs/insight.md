# PVCore Insight

## One-Line Summary

PVCore is a typed architecture for proof-carrying AI reasoning: answers must
come with witnesses, obligations, verification records, and obstruction reports.

## Problem

Most AI systems return answers as if text alone were a final object.

That interface hides the important parts of reasoning:

- what goal was actually solved;
- what assumptions were introduced;
- what evidence supports the proposal;
- which obligations remain open;
- which verifier accepted or rejected each claim;
- where context transport failed.

The result is a system that can sound coherent while silently losing the
geometry of its own reasoning.

## Core Shift

PVCore replaces:

```text
User -> LLM -> Answer
```

with:

```text
Goal -> Proposal -> Witness -> Obligation -> Verification -> Commit
```

The returned object is either:

```text
VerifiedCommit
```

or:

```text
ObstructionReport
```

This means failure is first-class. A system should not pretend to know when it
has missing witnesses, incompatible assumptions, failed verification, or
unresolved obligations.

## Witness Geometry

The central idea is that reasoning moves through contexts.

A context can be a user request, a codebase, a Lean environment, a knowledge
graph, a document corpus, or a domain model.

When a system translates between contexts, it performs a transport:

```text
source context -> target context
```

Every transport carries assumptions. If the assumptions do not commute with the
target context, the system should report a defect instead of producing an
unqualified answer.

Working slogan:

```text
Hallucination ~= unreported transport defect.
```

## Why Typed Obligations Matter

Each proposal generates obligations.

Examples:

- a code change must typecheck;
- a theorem must compile;
- a retrieved claim must cite a source;
- a migration must have rollback;
- a generated answer must preserve stated constraints;
- a cross-context translation must declare assumptions.

PVCore treats these obligations as typed objects, not informal comments.

The rule is:

```text
No trusted answer without discharged obligations.
```

## Why This Matters For Agents

Agents need a way to stop safely.

Without obstruction reports, an agent is pressured to keep generating plausible
next steps. With typed obstructions, stopping becomes a valid output:

```text
I cannot produce a verified commit because obligation O failed at verifier V.
Here is the minimal repair path.
```

This is the difference between an agent that improvises and an agent that
carries proof obligations.

## Research Direction

PVCore is initially a blueprint, not a finished verifier.

The next research layers are:

- Lean definitions for goals, proposals, witnesses, obligations, and commits;
- executable checkers for small examples;
- obstruction reports for failed RAG and agent tasks;
- context transport models;
- obligation fibrations;
- institution-based semantics for heterogeneous reasoning contexts.

## Public Positioning

PVCore is not a claim that every AI answer can be fully formally proven.

It is a claim that AI systems should expose the difference between:

- answered;
- witnessed;
- verified;
- trusted;
- obstructed.

That distinction is the beginning of proof-carrying reasoning.

