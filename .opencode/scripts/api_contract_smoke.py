#!/usr/bin/env python3
import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

import requests


@dataclass
class EndpointCheck:
    method: str
    path: str
    expect_status: int = 200
    expect_headers: Dict[str, str] = None
    required_json_fields: List[str] = None


@dataclass
class ReadinessConfig:
    path: str = "/health"
    expect_status: int = 200
    timeout_sec: int = 30
    interval_sec: float = 1.0


def load_config(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    # Basic validation
    if 'base_url' not in cfg:
        raise ValueError('config must contain base_url')
    if 'endpoints' not in cfg or not isinstance(cfg['endpoints'], list):
        raise ValueError('config must contain endpoints array')
    return cfg


def wait_readiness(base_url: str, readiness: Dict[str, Any]) -> List[str]:
    logs: List[str] = []
    path = readiness.get('path', '/health')
    expect_status = int(readiness.get('expect_status', 200))
    timeout_sec = int(readiness.get('timeout_sec', 30))
    interval_sec = float(readiness.get('interval_sec', 1.0))
    url = base_url.rstrip('/') + path
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            r = requests.get(url, timeout=5)
            logs.append(f"[readiness] GET {url} -> {r.status_code}")
            if r.status_code == expect_status:
                return logs
        except Exception as e:
            logs.append(f"[readiness] GET {url} error: {e}")
        time.sleep(interval_sec)
    logs.append(f"[readiness] timeout after {timeout_sec}s waiting for status {expect_status}")
    return logs


def check_endpoint(base_url: str, ep: Dict[str, Any]) -> Dict[str, Any]:
    method = ep.get('method', 'GET').upper()
    path = ep['path']
    expect_status = int(ep.get('expect_status', 200))
    expect_headers = {k.lower(): v for k, v in (ep.get('expect_headers') or {}).items()}
    required_json_fields = ep.get('required_json_fields') or []
    url = base_url.rstrip('/') + path
    result = {
        'url': url,
        'method': method,
        'expect_status': expect_status,
        'status': None,
        'pass': True,
        'failures': [],
    }
    try:
        r = requests.request(method, url, timeout=10)
        result['status'] = r.status_code
        if r.status_code != expect_status:
            result['pass'] = False
            result['failures'].append(f"status {r.status_code} != {expect_status}")
        # Headers check
        for hk, hv in expect_headers.items():
            actual = r.headers.get(hk, r.headers.get(hk.capitalize()))
            if actual is None:
                result['pass'] = False
                result['failures'].append(f"missing header {hk}")
            elif hv != '*' and actual != hv:
                result['pass'] = False
                result['failures'].append(f"header {hk}: '{actual}' != '{hv}'")
        # JSON fields
        if required_json_fields:
            try:
                data = r.json()
            except Exception as e:
                result['pass'] = False
                result['failures'].append(f"response not JSON: {e}")
            else:
                for f in required_json_fields:
                    if isinstance(data, dict):
                        if f not in data:
                            result['pass'] = False
                            result['failures'].append(f"missing json field '{f}'")
                    else:
                        result['pass'] = False
                        result['failures'].append("json root is not an object")
                        break
    except Exception as e:
        result['pass'] = False
        result['failures'].append(f"request error: {e}")
    return result


def render_report(readiness_logs: List[str], results: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    overall_pass = all(r['pass'] for r in results)
    summary = "PASS" if overall_pass else "FAIL"
    lines.append(f"# API Contract Smoke: {summary}")
    lines.append("")
    lines.append("## Readiness")
    for l in readiness_logs:
        lines.append(f"- {l}")
    lines.append("")
    lines.append("## Endpoints")
    for r in results:
        status = "PASS" if r['pass'] else "FAIL"
        lines.append(f"### {r['method']} {r['url']} — {status}")
        lines.append(f"- Expected status: {r['expect_status']}, got: {r['status']}")
        if r['failures']:
            lines.append("- Failures:")
            for f in r['failures']:
                lines.append(f"  - {f}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='API Contract Smoke')
    parser.add_argument('--config', required=True, help='Path to config JSON')
    parser.add_argument('--report', default=None, help='Path to write markdown report')
    args = parser.parse_args()

    cfg = load_config(args.config)
    base_url = cfg['base_url']

    # Readiness
    readiness_cfg = cfg.get('readiness') or {}
    readiness_logs = wait_readiness(base_url, readiness_cfg)

    # Proceed regardless; readiness is informational here but strongly hints issues
    results: List[Dict[str, Any]] = []
    for ep in cfg['endpoints']:
        results.append(check_endpoint(base_url, ep))

    report = render_report(readiness_logs, results)
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(report)
    else:
        print(report)

    ok = all(r['pass'] for r in results)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
