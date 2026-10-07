RepoGuard MCP Server

Overview:
- Exposes tools via MCP to scan a repository for potential secrets.
- Primary tool: scan_secrets(path?, include_exts?, exclude_dirs?)
- Secondary tool: rules()

Run locally:
1. Install deps: pip install -r requirements.txt
2. Start server: python -m mcp run practices/practice_04/mcp/server.py

OpenCode integration:
- Configured under key mcp.repo-guard in opencode.json, transport=local stdio.
- Agent can call tool "scan_secrets".

Notes:
- Skips binaries and files >2MB.
- Excludes common build/cache directories.
- Patterns are a pragmatic subset; tweak in server.py if needed.
