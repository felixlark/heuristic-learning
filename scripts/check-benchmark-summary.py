#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "docs/public/benchmark-summary.json"
SCHEMA_PATH = ROOT / "docs/public/benchmark-summary.schema.json"
EXPECTED_IDS = {
    "gridworld",
    "robot-soccer",
    "vizdoom-replay",
    "traffic-grid",
    "breakout-replay",
    "ant-gait-replay",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing JSON file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"JSON root must be object: {path.relative_to(ROOT)}")
    return data


def require_no_extra_keys(data: dict[str, Any], allowed: set[str], context: str) -> None:
    extra = set(data) - allowed
    require(not extra, f"{context}: unexpected keys {sorted(extra)}")


def find_policy(report: dict[str, Any], name: str) -> dict[str, Any]:
    policies = report.get("policies")
    require(isinstance(policies, list), "report policies must be list")
    for policy in policies:
        if isinstance(policy, dict) and policy.get("policy") == name:
            return policy
    raise AssertionError(f"report missing policy: {name}")


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Benchmark Summary", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "summary"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "result" in defs, "schema must define result")


def check_summary(summary: dict[str, Any]) -> None:
    require(summary.get("$schema") == "/benchmark-summary.schema.json", "summary schema pointer mismatch")
    require_no_extra_keys(summary, {"$schema", "schema_version", "summary"}, "summary")
    require(summary.get("schema_version") == 1, "summary schema_version must be 1")

    example_registry = load_json(ROOT / "docs/public/example-registry.json")
    registry_examples = {
        example.get("id"): example
        for example in example_registry.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    rows = summary.get("summary")
    require(isinstance(rows, list) and rows, "summary must be a non-empty list")
    ids: set[str] = set()
    allowed = {
        "id",
        "title",
        "source_status",
        "failure_mode",
        "baseline_outcome",
        "heuristic_outcome",
        "primary_metric",
        "report",
        "test",
        "policy_target",
        "course_page",
        "boundary",
    }
    page = (ROOT / "docs/zh-cn/appendix/benchmark-results.md").read_text(encoding="utf-8")
    manifest = (ROOT / "docs/public/course-manifest.json").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    for index, row in enumerate(rows):
        context = f"summary[{index}]"
        require(isinstance(row, dict), f"{context}: must be object")
        require_no_extra_keys(row, allowed, context)
        example_id = row.get("id")
        require(isinstance(example_id, str), f"{context}: id must be string")
        require(example_id not in ids, f"duplicate example id: {example_id}")
        ids.add(example_id)
        require(example_id in registry_examples, f"{context}: unknown example id")
        registry_example = registry_examples[example_id]
        for key in ["title", "source_status", "failure_mode", "report", "test", "policy_target"]:
            require(row.get(key) == registry_example.get(key), f"{context}: {key} does not match example registry")
        for path_key in ["report", "test", "policy_target", "course_page"]:
            path = ROOT / row[path_key]
            require(path.exists(), f"{context}: path missing: {row[path_key]}")

        report = load_json(ROOT / row["report"])
        baseline = find_policy(report, "baseline")
        heuristic = find_policy(report, "heuristic")
        if row["primary_metric"] == "reason_and_reward":
            require(baseline.get("reason") == row["baseline_outcome"], f"{context}: baseline reason mismatch")
            require(heuristic.get("reason") == row["heuristic_outcome"], f"{context}: heuristic reason mismatch")
            require(isinstance(baseline.get("reward"), (int, float)), f"{context}: baseline reward missing")
            require(isinstance(heuristic.get("reward"), (int, float)), f"{context}: heuristic reward missing")
        elif row["primary_metric"] == "probe_action":
            probes = report.get("probes")
            require(isinstance(probes, list) and probes, f"{context}: probe metric requires probes")
            require(any(probe.get("name") == row["failure_mode"] for probe in probes if isinstance(probe, dict)), f"{context}: failure probe missing")
            require(row["baseline_outcome"] == row["failure_mode"], f"{context}: gridworld baseline outcome should match failure mode")
            require(row["heuristic_outcome"] in page, f"{context}: heuristic outcome not documented")
        else:
            raise AssertionError(f"{context}: unknown primary_metric {row['primary_metric']}")

        candidate = report.get("candidate_update")
        require(isinstance(candidate, dict), f"{context}: report missing candidate_update")
        require(candidate.get("target") == row["policy_target"], f"{context}: candidate target mismatch")
        require(row["failure_mode"] in page, f"{context}: failure mode not documented on benchmark page")

    require(ids == EXPECTED_IDS, f"benchmark summary ids mismatch: {sorted(ids)}")
    require("docs/zh-cn/appendix/benchmark-results.md" in manifest, "course manifest must include benchmark results page")
    require("docs/public/benchmark-summary.json" in llms, "root llms.txt missing benchmark-summary.json")
    require("/benchmark-summary.json" in public_llms, "public llms.txt missing benchmark-summary route")


def main() -> None:
    summary = load_json(SUMMARY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_summary(summary)
    print(f"checked benchmark summary with {len(summary['summary'])} results")


if __name__ == "__main__":
    main()
