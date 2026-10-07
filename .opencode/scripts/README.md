API Contract Smoke

This directory contains the smoke test runner script `api_contract_smoke.py` used by the pre-push hook.

Usage:
- Manual: `python3 .opencode/scripts/api_contract_smoke.py --config .opencode/skills/api-contract-smoke/config/local_example.json --report .opencode/skills/api-contract-smoke/reports/manual.md`
- Hook: see `.opencode/hooks/pre-push`. Activate with `ln -sf ../../.opencode/hooks/pre-push .git/hooks/pre-push && chmod +x .opencode/hooks/pre-push`.
