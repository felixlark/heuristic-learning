#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs" / "public" / "experiment-report.schema.json"
REPORTS = {
    "gridworld": {
        "path": ROOT / "experiments" / "gridworld" / "latest.json",
        "readme": ROOT / "experiments" / "gridworld" / "README.md",
        "target": "examples/heuristic-gridworld/policies.py",
        "failure_mode": "local_greedy_trap",
        "feedback_script": "npm run examples:gridworld:feedback",
    },
    "robot-soccer": {
        "path": ROOT / "experiments" / "robot-soccer" / "latest.json",
        "readme": ROOT / "experiments" / "robot-soccer" / "README.md",
        "target": "examples/robot-soccer/policies.py",
        "failure_mode": "blocked_shot",
        "feedback_script": "npm run examples:robot-soccer:feedback",
    },
    "vizdoom-replay": {
        "path": ROOT / "experiments" / "vizdoom-replay" / "latest.json",
        "readme": ROOT / "experiments" / "vizdoom-replay" / "README.md",
        "target": "examples/vizdoom-replay/vizdoom_policies.py",
        "failure_mode": "wasted_pickup",
        "feedback_script": "npm run examples:vizdoom-replay:feedback",
    },
    "traffic-grid": {
        "path": ROOT / "experiments" / "traffic-grid" / "latest.json",
        "readme": ROOT / "experiments" / "traffic-grid" / "README.md",
        "target": "examples/traffic-grid/policies.py",
        "failure_mode": "spillback",
        "feedback_script": "npm run examples:traffic-grid:feedback",
    },
    "breakout-replay": {
        "path": ROOT / "experiments" / "breakout-replay" / "latest.json",
        "readme": ROOT / "experiments" / "breakout-replay" / "README.md",
        "target": "examples/breakout-replay/policies.py",
        "failure_mode": "missed_after_wall_reflection",
        "feedback_script": "npm run examples:breakout-replay:feedback",
    },
    "ant-gait-replay": {
        "path": ROOT / "experiments" / "ant-gait-replay" / "latest.json",
        "readme": ROOT / "experiments" / "ant-gait-replay" / "README.md",
        "target": "examples/ant-gait-replay/policies.py",
        "failure_mode": "yaw_drift",
        "feedback_script": "npm run examples:ant-gait-replay:feedback",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_report(name: str, path: Path) -> dict[str, object]:
    require(path.exists(), f"{name}: missing report {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as file:
        report = json.load(file)
    require(isinstance(report, dict), f"{name}: report must be a JSON object")
    return report


def check_schema() -> None:
    require(SCHEMA.exists(), "missing experiment report schema")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    require(schema.get("title") == "Heuristic Learning Experiment Report", "experiment report schema title mismatch")
    require(schema.get("type") == "object", "experiment report schema root must be object")
    required = schema.get("required")
    require(isinstance(required, list), "experiment report schema required must be a list")
    for key in ["policies", "feedback", "candidate_update"]:
        require(key in required, f"experiment report schema missing required key {key}")
    candidate = schema.get("properties", {}).get("candidate_update", {})
    candidate_required = candidate.get("required")
    require(isinstance(candidate_required, list), "candidate_update schema required must be a list")
    for key in ["target", "rule", "verification"]:
        require(key in candidate_required, f"candidate_update schema missing required key {key}")


def check_report(name: str, spec: dict[str, object]) -> None:
    path = spec["path"]
    readme_path = spec["readme"]
    target = spec["target"]
    failure_mode = spec["failure_mode"]
    feedback_script = spec["feedback_script"]
    require(isinstance(path, Path), f"{name}: invalid path spec")
    require(isinstance(readme_path, Path), f"{name}: invalid readme spec")
    require(isinstance(target, str), f"{name}: invalid target spec")
    require(isinstance(failure_mode, str), f"{name}: invalid failure_mode spec")
    require(isinstance(feedback_script, str), f"{name}: invalid feedback_script spec")

    report = load_report(name, path)
    report_text = json.dumps(report, ensure_ascii=False)
    policies = report.get("policies")
    feedback = report.get("feedback")
    candidate_update = report.get("candidate_update")

    require(isinstance(policies, list), f"{name}: policies must be a list")
    require(len(policies) >= 2, f"{name}: policies must compare at least two policies")
    policy_names = {
        policy.get("policy")
        for policy in policies
        if isinstance(policy, dict) and isinstance(policy.get("policy"), str)
    }
    require("baseline" in policy_names, f"{name}: missing baseline policy")
    require("heuristic" in policy_names, f"{name}: missing heuristic policy")
    require(failure_mode in report_text, f"{name}: report missing failure mode {failure_mode}")

    require(isinstance(feedback, list), f"{name}: feedback must be a list")
    require(all(isinstance(item, str) and item for item in feedback), f"{name}: feedback entries must be non-empty strings")

    require(isinstance(candidate_update, dict), f"{name}: candidate_update must be an object")
    require(candidate_update.get("target") == target, f"{name}: candidate_update.target mismatch")
    require(isinstance(candidate_update.get("rule"), str) and candidate_update["rule"], f"{name}: missing candidate_update.rule")
    require(
        candidate_update.get("verification") == "python3 -m unittest discover -s tests",
        f"{name}: verification must point to the test suite",
    )
    require((ROOT / target).exists(), f"{name}: candidate_update.target file missing")

    require(readme_path.exists(), f"{name}: missing experiment README")
    readme = readme_path.read_text(encoding="utf-8")
    require(feedback_script in readme, f"{name}: README missing feedback script")
    require(failure_mode in readme or failure_mode in report_text, f"{name}: failure mode missing from README/report")


def main() -> None:
    check_schema()
    for name, spec in REPORTS.items():
        check_report(name, spec)
    print(f"checked {len(REPORTS)} experiment reports")


if __name__ == "__main__":
    main()
