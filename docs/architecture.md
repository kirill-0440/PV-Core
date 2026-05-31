# Architecture

PVCore is a small proof-carrying reasoning runtime.

The runtime separates five concerns:

1. Goal reconstruction.
2. Proposal construction.
3. Witness collection.
4. Obligation generation.
5. Verification and commit or obstruction.

The minimal Python implementation is intentionally direct:

```text
pvcore/types.py        typed records
pvcore/pipeline.py     execution loop
pvcore/obligations.py  obligation generation
pvcore/verifiers.py    verifier functions
```

The ECOM example shows a refund flow where every accepted result carries
verification certificates, and duplicate refund attempts become obstruction
reports.
