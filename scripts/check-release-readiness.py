#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VISUAL_PATH = ROOT / "docs/public/visual-verification.json"
VISUAL_LOG_PATH = ROOT / "docs/public/visual-acceptance-log.json"
COMPLETION_PATH = ROOT / "docs/public/completion-audit.json"
COMPLETION_PAGE_PATH = ROOT / "docs/zh-cn/appendix/completion-audit.md"
PACKAGE_PATH = ROOT / "package.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing JSON file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"JSON root must be object: {path.relative_to(ROOT)}")
    return data


def main() -> int:
    package = load_json(PACKAGE_PATH)
    visual = load_json(VISUAL_PATH)
    visual_log = load_json(VISUAL_LOG_PATH)
    completion = load_json(COMPLETION_PATH)

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    for script in ["verify", "visual:verification:check", "completion:audit:check"]:
        require(script in scripts, f"missing package script: {script}")

    required_commands = completion.get("required_commands")
    require(isinstance(required_commands, list), "completion required_commands must be a list")
    completion_page = COMPLETION_PAGE_PATH.read_text(encoding="utf-8")
    require("npm run verify" in completion_page, "completion audit page must require npm run verify")

    final_checks = completion.get("final_checks")
    require(isinstance(final_checks, list), "completion final_checks must be a list")
    require(
        any("Browser/IAB" in check for check in final_checks if isinstance(check, str)),
        "completion final checks must mention Browser/IAB",
    )

    checks = visual.get("checks")
    require(isinstance(checks, list) and checks, "visual checks must be a non-empty list")
    log_entries = visual_log.get("entries")
    require(isinstance(log_entries, list) and log_entries, "visual acceptance log entries must be a non-empty list")
    log_by_id = {
        entry.get("check_id"): entry
        for entry in log_entries
        if isinstance(entry, dict) and isinstance(entry.get("check_id"), str)
    }
    pending_log = [
        entry
        for entry in log_entries
        if isinstance(entry, dict) and entry.get("status") != "passed"
    ]
    evidence_log = visual.get("evidence_log")
    require(isinstance(evidence_log, dict), "visual evidence_log must be an object")
    current_run_status = evidence_log.get("current_run_status")
    require(isinstance(current_run_status, str), "visual current_run_status must be a string")

    if pending_log or not current_run_status.startswith("passed-") or visual_log.get("status") != "passed":
        print("release readiness blocked: official browser visual acceptance is not complete")
        print("run first: npm run verify")
        print("then use the official Browser/IAB or Chrome plugin for these routes:")
        for check in checks:
            if not isinstance(check, dict):
                continue
            entry = log_by_id.get(check.get("id"), {})
            if entry.get("status") == "passed":
                continue
            print(
                "- {id}: {route} [{surface}, {viewport}] status={status} log={log_status}".format(
                    id=check.get("id"),
                    route=check.get("route"),
                    surface=check.get("surface"),
                    viewport=check.get("viewport"),
                    status=check.get("status"),
                    log_status=entry.get("status", "missing"),
                )
            )
        print(f"visual evidence status: {current_run_status}")
        print(f"visual acceptance log status: {visual_log.get('status')}")
        return 2

    print(f"release readiness passed with {len(checks)} visual checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
