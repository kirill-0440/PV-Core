---
source_code: https://github.com/kirill-0440/PV-Core
run_ids:
  - run-YOUR_ECOM1_PROD_RUN_ID
author: ""
author_linkedin: ""
author_github: https://github.com/kirill-0440
company: ""
impact: Uses proof-carrying reasoning to turn e-commerce tasks into proposals, witnesses, obligations, verifications, and explicit obstruction reports before acting.
challenge: ecom
---

# PVCore Witness Geometry Agent for ECOM1

PVCore is a proof-carrying architecture for policy-constrained e-commerce
agents. Instead of treating a model answer as final, it converts each task into
a typed pipeline:

```text
Goal -> Proposal -> Witness -> Obligation -> Verification -> Commit | ObstructionReport
```

For ECOM1, the architecture is intended for agents that must reason over
catalogue data, inventory, customer records, payments, policies, support
tickets, returns, refunds, and audit trails while deciding whether to act,
refuse, or escalate.

This draft is an architecture writeup template. It should only be submitted to
the ECOM1 architecture repository after replacing `ACCOUNTID` and `run_ids`
with real public values from an eligible `bitgn/ecom1-prod` run.

## How does it work?

The main loop is:

```text
task
  -> reconstruct commerce context
  -> propose a candidate action
  -> collect witnesses from the e-commerce OS
  -> generate obligations
  -> verify obligations
  -> commit action or return obstruction
```

The key runtime objects are:

- `Goal`: the customer, merchant, policy, and task context.
- `Proposal`: the candidate checkout, refund, return, support, or refusal
  action.
- `Witness`: catalogue rows, inventory state, customer records, payment status,
  policy text, ticket history, and audit events supporting the proposal.
- `Obligation`: a typed claim that must be discharged before acting.
- `Verification`: the result of checking an obligation.
- `Commit`: an accepted action with witnesses and verification records.
- `ObstructionReport`: a safe stop with failed stage, reason, and repair hints.

The agent should inspect state before acting. It does not treat retrieved
context as trusted until the relevant obligations have been generated and
checked.

The task is finished only when either:

- every required obligation is accepted and the action can be committed; or
- a blocking obligation produces an obstruction report.

## Models

Fill in the actual models used for the submitted ECOM1 runs:

- Main solver: `MODEL_NAME`
- Classifier/router/planner, if any: `MODEL_NAME_OR_NONE`
- Evaluator or evolution loop, if any: `MODEL_NAME_OR_NONE`
- Runtime settings that mattered: `TEMPERATURE`, `MAX_TOKENS`, `TOOL_POLICY`

The architecture does not require a specific closed model. It is designed to
work with local or open models when the verifier and witness interface are
strict enough.

## E-commerce OS Reasoning

PVCore maps each commerce subsystem into witness sources and obligations.

### Catalogue and product matching

Catalogue claims should be witnessed by product records, variants, attributes,
prices, merchant constraints, and availability windows.

Example obligations:

- the selected product exists;
- the requested variant matches the customer intent;
- price, currency, and promotion constraints are consistent;
- substitution is allowed by policy.

### Inventory, warehouses, shipping, and store coverage

Inventory and fulfillment claims should be witnessed by stock records,
warehouse or store coverage, shipping eligibility, delivery constraints, and
reservation status.

Example obligations:

- stock is available in a valid location;
- shipping destination is covered;
- delivery timing satisfies the task;
- the action does not oversell inventory.

### Customer records, baskets, orders, and payments

Customer-sensitive actions should be witnessed by customer identity, basket
state, order state, payment status, fraud or risk flags, and authorization
rules.

Example obligations:

- customer identity and order ownership match;
- payment state allows the requested action;
- basket mutation is permitted;
- customer data access is scoped to the task.

### Merchant policies and policy addenda

Policy reasoning should be witness-backed. The agent should cite the active
policy version and addenda relevant to discounts, refunds, returns,
replacements, payments, privacy, and escalation.

Example obligations:

- policy version is applicable at the task time;
- refund or return window is open;
- exception handling is explicitly allowed;
- manual escalation is required when policy is ambiguous.

### Support tickets, returns, refunds, and escalations

Support actions should be tied to ticket history, prior promises, previous
refunds, return state, and audit trail.

Example obligations:

- no duplicate refund is created;
- prior support commitments are respected;
- return authorization is valid;
- escalation is required for unsafe or unsupported actions.

### Audit trails, logs, and evidence

Each accepted action should include a compact audit record:

```text
task id
proposal id
witness ids
obligation ids
verification results
action or obstruction
residual risk
```

## Acting, Refusing, and Escalating

PVCore's rule is:

```text
No trusted action without discharged obligations.
```

The agent is allowed to mutate state only when:

- the task is within the benchmark tool authority;
- identity, ownership, and policy checks pass;
- all action-specific obligations are accepted;
- no unresolved obstruction remains for the target action.

The agent refuses or escalates when:

- required records are missing;
- assumptions conflict;
- policy is ambiguous or unavailable;
- payment, refund, or customer-data authority is insufficient;
- the requested action would violate merchant or customer constraints;
- context transport fails between user request, policy, and system state.

## Problems

Expected failure modes:

- Missing witness: a model proposes an action without enough commerce evidence.
- Incompatible assumptions: user request, policy, and system state disagree.
- Failed verification: a refund, return, shipping, or authorization rule does
  not pass.
- Non-commuting transport: a statement valid in the customer conversation is
  not valid in the payment, inventory, or policy context.
- Unresolved obligation: the agent cannot prove that an action is safe.

## Solutions

The architecture improves reliability by making failure explicit:

- every action proposal generates obligations;
- every obligation has a verifier type;
- every accepted action carries witnesses;
- unresolved obligations become obstruction reports;
- hallucination is treated as an unreported transport defect.

Things deliberately kept simple:

- one typed loop instead of many hidden agent modes;
- explicit obstruction reports instead of speculative retries;
- compact witness records rather than full formal proof for every claim;
- policy-first action gating before tool mutation.

## What Would You Improve Next?

The next version should add:

- executable verifier stubs for common commerce obligations;
- a structured witness index over catalogue, inventory, orders, policies, and
  tickets;
- Lean definitions for the core PVCore types;
- a replayable audit log for each benchmark task;
- comparison tests against ungated tool-using agents;
- stronger transport-defect detection between policy, payment, and customer
  contexts.

## Lessons From ECOM1

ECOM1-style commerce agents need more than retrieval and tool calls. They need a
typed distinction between:

- answer;
- proposal;
- witnessed proposal;
- verified action;
- obstruction.

Commerce tasks combine business policy, customer identity, payment state,
inventory constraints, and auditability. A useful agent must know when to act,
but also when to stop and report the exact missing witness or failed obligation.

PVCore frames that stopping behavior as part of the architecture rather than as
a fallback after the model gets confused.

## Optional: Diagram

```text
            commerce task
                 |
                 v
              Goal
                 |
                 v
             Proposal
                 |
        +--------+--------+
        |                 |
        v                 v
   Witness Search   Obligation Generation
        |                 |
        +--------+--------+
                 |
                 v
            Verification
                 |
        +--------+--------+
        |                 |
        v                 v
  Verified Commit   Obstruction Report
```
