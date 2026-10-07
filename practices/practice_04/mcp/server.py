import os
import re
import json
from typing import Any, Dict, List, Optional, Tuple

# MCP Python SDK
from mcp.server import MCPServer


# Server instance discovered by `mcp run server.py`
mcp = MCPServer("RepoGuard")


# --- Secret detection rules ---
# Each rule is (name, compiled_regex)
RULES: List[Tuple[str, re.Pattern]] = []


def _add_rule(name: str, pattern: str, flags: int = re.IGNORECASE) -> None:
    RULES.append((name, re.compile(pattern, flags)))


# Common secret patterns (pragmatic subset)
_add_rule("PRIVATE_KEY_BLOCK", r"-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----")
_add_rule("AWS_ACCESS_KEY_ID", r"\bAKIA[0-9A-Z]{16}\b", flags=re.IGNORECASE)
_add_rule("AWS_SECRET_ACCESS_KEY", r"\baws_secret_access_key\b\s*[:=]\s*[\'\"][^\'\"]{20,}[\'\"]")
_add_rule("GCP_API_KEY", r"\bAIza[0-9A-Za-z\-_]{35}\b")
_add_rule("GITHUB_TOKEN", r"\bghp_[A-Za-z0-9]{36}\b")
_add_rule("SLACK_TOKEN", r"\bxox(?:b|p|a|r|s)-[0-9A-Za-z-]{10,}\b")
_add_rule("STRIPE_SECRET_KEY", r"\bsk_(?:live|test)_[A-Za-z0-9]{24}\b")
_add_rule("JWT", r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")
_add_rule("PASSWORD_ASSIGNMENT", r"\bpassword\s*[:=]\s*[\'\"][^\'\"]{8,}[\'\"]")
_add_rule("GENERIC_API_KEY", r"\b(api[_-]?key|secret[_-]?key|token)\s*[:=]\s*[\'\"][A-Za-z0-9_\-]{16,}[\'\"]")


DEFAULT_INCLUDE_EXTS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".json",
    ".yml",
    ".yaml",
    ".md",
    ".txt",
    ".env",
    ".ini",
    ".cfg",
    ".sh",
    ".tf",
    ".xml",
    ".html",
    ".css",
    ".sql",
    ".rb",
    ".go",
    ".java",
    ".kt",
}

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "out",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".opencode/node_modules",
}


def _is_binary(content: bytes) -> bool:
    # Heuristic: presence of NUL byte, or high ratio of non-text bytes
    if b"\x00" in content:
        return True
    sample = content[:1024]
    # Treat as text if decodes cleanly as UTF-8
    try:
        sample.decode("utf-8")
        return False
    except UnicodeDecodeError:
        return True


def _scan_file(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "rb") as f:
            raw = f.read()
        if len(raw) > 2 * 1024 * 1024:  # skip >2MB files
            return []
        if _is_binary(raw):
            return []
        text = raw.decode("utf-8", errors="ignore")
    except Exception:
        return []

    issues: List[Dict[str, Any]] = []
    for name, regex in RULES:
        for m in regex.finditer(text):
            # determine line number
            start = m.start()
            line_no = text.count("\n", 0, start) + 1
            snippet = text[max(0, start - 40) : m.end() + 40]
            # minimize snippet whitespace
            snippet = snippet.replace("\n", " ")
            issues.append({
                "rule": name,
                "line": line_no,
                "match": m.group(0)[:120],
                "context": snippet[:200],
            })
    return issues


def _should_scan_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in DEFAULT_INCLUDE_EXTS or ext == ""


def run_secret_scan(
    root: str,
    include_exts: Optional[List[str]] = None,
    exclude_dirs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    root = os.path.abspath(root)
    include = {e.lower() for e in include_exts} if include_exts else DEFAULT_INCLUDE_EXTS
    exclude = set(exclude_dirs) if exclude_dirs else DEFAULT_EXCLUDE_DIRS

    files_scanned = 0
    findings: List[Dict[str, Any]] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories in-place for performance
        dirnames[:] = [d for d in dirnames if os.path.relpath(os.path.join(dirpath, d), root) not in exclude and d not in exclude]

        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, root)

            # skip large or hidden special paths fast
            if any(part in exclude for part in rel.split(os.sep)):
                continue

            if not _should_scan_file(fp):
                # allow explicit include override
                ext = os.path.splitext(fp)[1].lower()
                if ext not in include:
                    continue

            files_scanned += 1
            issues = _scan_file(fp)
            for issue in issues:
                entry = {"file": rel}
                entry.update(issue)
                findings.append(entry)

    summary = {
        "root": root,
        "files_scanned": files_scanned,
        "issues_found": len(findings),
    }
    return {"summary": summary, "issues": findings}


@mcp.tool()
def scan_secrets(
    path: Optional[str] = None,
    include_exts: Optional[List[str]] = None,
    exclude_dirs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Scan a repository for potential secrets.

    Args:
        path: Directory to scan. Defaults to REPO_ROOT env or current directory.
        include_exts: Optional list of file extensions (with dot) to include.
        exclude_dirs: Optional list of directory names/paths to exclude.

    Returns:
        Object with fields: summary {root, files_scanned, issues_found}, issues[{file, line, rule, match, context}]
    """
    root = path or os.environ.get("REPO_ROOT", ".")
    result = run_secret_scan(root=root, include_exts=include_exts, exclude_dirs=exclude_dirs)
    return result


@mcp.tool()
def rules() -> Dict[str, Any]:
    """List secret detection rules available on this server."""
    return {"rules": [name for name, _ in RULES]}


# Note: We intentionally do not call any runner here.
# Use: `python -m mcp run practices/practice_04/mcp/server.py` to start this server over stdio.
