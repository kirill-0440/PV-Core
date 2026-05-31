# Publication Checklist

Use this before publishing PVCore or submitting the BitGN ECOM1 architecture
writeup.

## Repository

- [ ] `README.md` describes the project honestly.
- [ ] `LICENSE` is present.
- [ ] Unit tests pass.
- [ ] ECOM refund demo produces `pvcore.commit.v0_1`.
- [ ] Duplicate refund fixture produces `pvcore.obstruction_report.v0_1`.
- [ ] No private stack names are present.
- [ ] No secrets, tokens, or local credentials are present.

## BitGN ECOM1

- [ ] Replace `ACCOUNTID` in the filename.
- [ ] Replace `source_code`.
- [ ] Replace `run-YOUR_ECOM1_PROD_RUN_ID`.
- [ ] Fill actual model names.
- [ ] Fill actual runtime settings.
- [ ] Confirm `challenge: ecom`.
- [ ] Confirm the run ids are eligible `bitgn/ecom1-prod` runs.

## External Actions

- [ ] Explicit approval to create the public GitHub repository.
- [ ] Explicit approval to push the initial commit.
- [ ] Explicit approval to fork `bitgn/bitgn-architectures`.
- [ ] Explicit approval to open the PR.
