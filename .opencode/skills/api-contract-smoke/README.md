API Contract Smoke Skill

Purpose:
- Minimal, generic smoke checks for any HTTP service. You control base_url and endpoints via JSON config.

Config locations (priority):
1. Environment variable `API_SMOKE_CONFIG` pointing to a JSON config file.
2. `config/api_smoke.json` at repo root.
3. First JSON in `.opencode/skills/api-contract-smoke/config/` excluding files with `template` or `example` in the name.

Files:
- config/local_example.json — example configuration for a demo service (ignored by the hook auto-discovery because of "example" in name).
- reports/ — output directory for generated markdown reports.

Hook:
- `.opencode/hooks/pre-push` runs the smoke if a config is found by the above rules. It blocks push on FAIL.
