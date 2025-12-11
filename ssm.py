#!/usr/bin/env python3
"""
Shadow Student Mode (SSM) logging utilities.

Design:
- Advisor posture: capture guidance steps, not force outcomes.
- Data minimization: only store task/hint metadata, no raw PII.
- Security: caller provides output dir; defaults to `output/ssm_logs`.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


ALLOWED_MODES = {"guided", "reveal"}


def log_ssm_session(
    task_id: str,
    attempts: List[Dict[str, Any]],
    mode: str = "guided",
    reveal_reason: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> str:
    """
    Persist an SSM session log.

    Args:
        task_id: unique task identifier (non-PII).
        attempts: list of dicts with keys step:int, input:str, hint:str, complete:bool.
        mode: "guided" or "reveal".
        reveal_reason: optional reason when mode == "reveal".
        output_dir: directory to write logs (default: output/ssm_logs).

    Returns:
        Path to the written JSON file.
    """
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Unsupported SSM mode: {mode}")

    base_dir = Path(output_dir or os.environ.get("SSM_LOG_DIR", "output/ssm_logs"))
    base_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "task_id": task_id,
        "mode": mode,
        "attempts": attempts,
    }
    if mode == "reveal":
        payload["reveal_reason"] = reveal_reason or "requested"

    log_path = base_dir / f"{task_id}.json"
    with log_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return str(log_path)
