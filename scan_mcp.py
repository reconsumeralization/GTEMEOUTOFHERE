#!/usr/bin/env python3
"""
Discovery helper for MCP server candidates.

Scans the repo for likely Node/Python services, guesses start commands and ports,
and emits a JSON list you can feed into Docker/Compose generation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parent


def find_node_projects() -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for pkg in ROOT.rglob("package.json"):
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except Exception:
            continue

        scripts = data.get("scripts", {}) or {}
        start = (
            scripts.get("start")
            or scripts.get("serve")
            or scripts.get("dev")
            or "npm start"
        )

        candidates.append(
            {
                "type": "node",
                "path": str(pkg.parent.relative_to(ROOT)),
                "name": data.get("name", pkg.parent.name),
                "start": start,
                "port_guess": 3000,
            }
        )
    return candidates


def find_python_projects() -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for marker in ["requirements.txt", "requirements-dev.txt", "pyproject.toml"]:
        for file in ROOT.rglob(marker):
            candidates.append(
                {
                    "type": "python",
                    "path": str(file.parent.relative_to(ROOT)),
                    "name": file.parent.name,
                    "start": "python main.py",
                    "port_guess": 3000,
                }
            )
    return candidates


def guess_port_from_code(path: Path) -> Optional[int]:
    """
    Heuristically scan source files for a port literal.
    """
    port_re = re.compile(r"(?:port|PORT|Port)\s*[:=]\s*['\"]?(\d{3,5})")
    for ext in ("*.js", "*.ts", "*.tsx", "*.py"):
        for file in path.glob(ext):
            try:
                text = file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            snippet = text[:8000]
            match = port_re.search(snippet)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
    return None


def dedupe_by_path(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique: List[Dict[str, Any]] = []
    for item in items:
        key = item["path"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def main() -> None:
    raw_candidates = find_node_projects() + find_python_projects()
    candidates: List[Dict[str, Any]] = []

    for item in dedupe_by_path(raw_candidates):
        port = guess_port_from_code(ROOT / item["path"]) or item.get("port_guess", 3000)
        item["port_guess"] = port
        candidates.append(item)

    print(json.dumps(candidates, indent=2))


if __name__ == "__main__":
    main()

