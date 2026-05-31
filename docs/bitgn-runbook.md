# BitGN ECOM1 Runbook

This runbook records how to obtain the real `run_ids` needed for the BitGN
ECOM1 architecture submission.

Do not invent run ids. Do not commit API keys.

## Current Public Source

```text
https://github.com/kirill-0440/PV-Core
```

## Required Inputs

```text
BITGN_ACCOUNT_ID:
BITGN_API_KEY: stored only in local environment
ECOM1 benchmark id: bitgn/ecom1-prod
main model:
planner model:
evaluator model:
runtime settings:
```

## Steps

1. Register on BitGN.
2. Create a BitGN API key.
3. Store the key locally, outside git.
4. Run a practice or sandbox task first, if available.
5. Run the eligible ECOM1 task set.
6. Record the returned `run_id`.
7. Record model names and runtime settings used for that exact run.
8. Render the final architecture markdown.
9. Submit only after checking eligibility and receiving explicit approval.

## Environment

Use environment variables rather than committed config files:

```bash
export BITGN_API_KEY="..."
export BITGN_ACCOUNT_ID="..."
export BITGN_CHALLENGE="ecom"
export BITGN_BENCHMARK="bitgn/ecom1-prod"
```

Use `.env.example` only as a template.

## Run Evidence Template

Fill this after the run:

```yaml
bitgn_account_id:
benchmark: bitgn/ecom1-prod
run_ids:
  - run-
source_code: https://github.com/kirill-0440/PV-Core
main_model:
planner_model:
evaluator_model:
runtime_settings:
started_at:
completed_at:
result_url:
notes:
```

## Render Final Submission

After the real values are known:

```bash
python3 tools/render_pvcore_bitgn_ecom1_submission.py \
  --account-id REAL_BITGN_ACCOUNT_ID \
  --source-code https://github.com/kirill-0440/PV-Core \
  --run-id run-REAL_ECOM1_PROD_RUN \
  --main-model "MODEL" \
  --planner-model "MODEL_OR_NONE" \
  --evaluator-model "MODEL_OR_NONE" \
  --runtime-settings "temperature=...,max_tokens=...,tool_policy=..."
```

The rendered file belongs in:

```text
2026-05-30-ecom1/REAL_BITGN_ACCOUNT_ID_pvcore-witness-geometry-agent.md
```

## Submission Blockers

Submission remains blocked until all of these are known:

- BitGN account id.
- Eligible ECOM1 run id.
- Actual model names.
- Actual runtime settings.
- Approval to fork, branch, push, and open a PR.

## Safety Notes

- Do not commit `.env.local`.
- Do not paste the API key into prompts, issues, PRs, logs, or markdown.
- Do not claim Hall of Fame eligibility unless the run is actually eligible.
- Do not submit placeholder run ids.
