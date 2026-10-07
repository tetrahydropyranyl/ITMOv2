"""Ask five questions to two local Ollama models in isolated sessions.

This script builds a minimal context from demo files and sends each
question in a fresh session to avoid context carryover.

Outputs JSON responses to ./results/{model}_q{n}.json and prints a short log.
Standard library only.
"""

import json
import time
import urllib.request
from pathlib import Path


def load_context() -> str:
    root = Path(__file__).resolve().parent
    files = [
        (root / "README.md", "README.md"),
        (root / "service.py", "service.py"),
        (root / "test_service.py", "test_service.py"),
        (root / "Makefile", "Makefile"),
    ]
    parts = []
    for path, name in files:
        if path.exists():
            parts.append(f"===== {name} =====\n{path.read_text()}\n")
    return "\n".join(parts)


def load_questions() -> list[str]:
    qpath = Path(__file__).resolve().parents[1] / "QUESTIONS.md"
    text = qpath.read_text(encoding="utf-8")
    lines = [l.strip() for l in text.splitlines()]
    qs = []
    for l in lines:
        if l and l[0].isdigit() and "." in l:
            # line like "1. question"
            q = l.split(".", 1)[1].strip()
            qs.append(q)
    return qs[:5]


def ask(model: str, system_prompt: str, user_content: str) -> dict:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.2,
            "seed": 42,
            "num_ctx": 8192,
            "num_predict": 512,
        },
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        answer = json.load(resp)
    # attach payload for reproducibility
    return {"request": payload, "response": answer}


def main():
    root = Path(__file__).resolve().parent
    system_prompt = (root / "repo-system.txt").read_text(encoding="utf-8")
    context = load_context()
    questions = load_questions()

    models = [
        ("itmo-agent:latest", "agent"),
        ("itmo-chat:latest", "chat"),
    ]
    results_dir = root / "results"
    results_dir.mkdir(exist_ok=True)

    for model, label in models:
        for idx, q in enumerate(questions, start=1):
            user = context + "\n\nВопрос: " + q
            record = ask(model, system_prompt, user)
            out = results_dir / f"{label}_q{idx}.json"
            # ensure we don't overwrite inadvertently
            with out.open("w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            msg = record.get("response", {}).get("message", {}).get("content", "")
            print(f"[{label}] Q{idx}: {msg[:120].replace('\n',' ')}...")
            time.sleep(0.2)  # small gap to keep server happy


if __name__ == "__main__":
    main()
