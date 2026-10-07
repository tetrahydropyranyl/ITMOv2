---
description: Run API Contract Smoke against a config file.
agent: build
model: openai/gpt-5
---

Run the API Contract Smoke checker for the provided config file.

Steps:

- Ensure Python is available, then execute:

```bash
python3 .opencode/scripts/api_contract_smoke.py --config $ARGUMENTS --report .opencode/skills/api-contract-smoke/reports/latest.md
```

- If the command exits non-zero, open `.opencode/skills/api-contract-smoke/reports/latest.md`, summarize the failures, and propose the minimum change to restore the contract.

- If it passes, paste the summary header line and list endpoints with PASS.
