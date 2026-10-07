---
name: api-contract-smoke
description: Use ONLY when you need to verify service readiness and perform a short API contract smoke check for key endpoints. Trigger on keywords: smoke, api contract, health, readiness, openapi, json schema. Use in ITMOv2 root; runs .opencode/scripts/api_contract_smoke.py with a provided config.
---

# API Contract Smoke

Purpose: verify that a service is up and responding as expected on a small set of critical endpoints. This skill:

- Waits for readiness (polls a health/ready endpoint)
- Sends a few HTTP requests to key endpoints
- Verifies status codes, content-type headers, and presence of required JSON fields
- Produces a Markdown report and non-zero exit on failure

Use when:

- You changed backend API behavior, response shapes, or headers
- You updated OpenAPI/JSON schemas and want to check compatibility quickly
- You want a fast signal in pre-push or after-edit hooks

Inputs:

- Config JSON file with `base_url`, `readiness`, and `endpoints` (see examples under `config/`)
- Optional report path; defaults to `reports/<timestamp>.md`

How to run:

1. Provide a config file:
   - Demo (httpbin): `.opencode/skills/api-contract-smoke/config/demo_httpbin.json`
   - Local service template: `.opencode/skills/api-contract-smoke/config/local_example.json`
2. Ask the agent to run the command:
   - `api-contract-smoke .opencode/skills/api-contract-smoke/config/demo_httpbin.json`
   or
   - Run via bash: `python .opencode/scripts/api_contract_smoke.py --config <path> --report .opencode/skills/api-contract-smoke/reports/latest.md`

Agent steps:

- Use the bash tool to invoke the Python script with the given config
- On failure, open the generated report and summarize failures; suggest minimal diffs to restore contract
- On success, paste the summary block from the report

Notes:

- Keep the endpoint list small (2–4) to keep smoke fast (<90s)
- If OpenAPI is available, derive required fields from the spec and add them to the config
- To simulate a failing run for demo, temporarily change an expected header or required field

Outputs:

- Markdown report with a section per endpoint and an overall PASS/FAIL
- Exit code 0 on success, 1 if any check fails (suitable for hooks)
