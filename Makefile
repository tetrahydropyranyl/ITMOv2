.PHONY: install test step1 step2 step3 smoke

install:
    @echo "Installing Python deps (for smoke skill)"
    @python3 -m pip -q install -r requirements.txt || true

test: step1 step2 step3

step1:
	@$(MAKE) -s -C practices/practice_01 test

step2:
	@$(MAKE) -s -C practices/practice_02 test

step3:
    @$(MAKE) -s -C practices/practice_03 test

smoke:
    @python3 .opencode/scripts/api_contract_smoke.py --config .opencode/skills/api-contract-smoke/config/demo_httpbin.json --report .opencode/skills/api-contract-smoke/reports/demo_run.md || true
    @echo "Smoke report: .opencode/skills/api-contract-smoke/reports/demo_run.md"
