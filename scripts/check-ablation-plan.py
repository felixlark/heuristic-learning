#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/ablation-plan.json"
SCHEMA_PATH = ROOT / "docs/public/ablation-plan.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/ablation-plan.md"
EXPECTED_IDS = {
    "gridworld-trap-avoidance",
    "robot-soccer-shot-lane",
    "vizdoom-medikit-threshold",
    "traffic-downstream-capacity",
    "breakout-reflection-prediction",
    "ant-gait-yaw-feedback",
    "constraint-audit-evidence-escalation",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing JSON file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"JSON root must be object: {path.relative_to(ROOT)}")
    return data


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Ablation Plan Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "ablations"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/ablation-plan.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    metrics = load_json(ROOT / "docs/public/evaluation-metrics.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    benchmark_protocol = (ROOT / "docs/zh-cn/appendix/benchmark-protocol.md").read_text(encoding="utf-8")
    benchmark_results = (ROOT / "docs/zh-cn/appendix/benchmark-results.md").read_text(encoding="utf-8")
    paper_blueprint = (ROOT / "docs/zh-cn/appendix/paper-blueprint.md").read_text(encoding="utf-8")
    research_projects = (ROOT / "docs/zh-cn/appendix/research-projects.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    example_ids = {example.get("id") for example in examples.get("examples", []) if isinstance(example, dict)}
    metric_ids = {metric.get("id") for metric in metrics.get("metrics", []) if isinstance(metric, dict)}

    ablations = registry.get("ablations")
    require(isinstance(ablations, list) and ablations, "ablations must be non-empty")
    ids: set[str] = set()
    covered_examples: set[str] = set()
    covered_metrics: set[str] = set()
    for index, ablation in enumerate(ablations):
        context = f"ablations[{index}]"
        require(isinstance(ablation, dict), f"{context}: must be object")
        require(
            set(ablation)
            == {
                "id",
                "title",
                "example_id",
                "metric_ids",
                "variable_under_test",
                "baseline_condition",
                "heuristic_condition",
                "expected_invariant",
                "evidence",
                "verification_commands",
                "research_use",
                "boundary",
            },
            f"{context}: unexpected keys",
        )
        ablation_id = ablation.get("id")
        require(isinstance(ablation_id, str), f"{context}: id must be string")
        require(ablation_id not in ids, f"duplicate ablation id: {ablation_id}")
        ids.add(ablation_id)
        title = ablation.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        example_id = ablation.get("example_id")
        require(example_id in example_ids, f"{context}: unknown example id {example_id}")
        covered_examples.add(example_id)
        for metric_id in ablation.get("metric_ids", []):
            require(metric_id in metric_ids, f"{context}: unknown metric id {metric_id}")
            covered_metrics.add(metric_id)
        for field in ["variable_under_test", "baseline_condition", "heuristic_condition", "expected_invariant", "research_use", "boundary"]:
            require(isinstance(ablation.get(field), str) and ablation[field], f"{context}: {field} missing")
        for evidence in ablation.get("evidence", []):
            require(isinstance(evidence, str) and (ROOT / evidence).exists(), f"{context}: evidence missing: {evidence}")
        for command in ablation.get("verification_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command in audit, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"ablation ids mismatch: {sorted(ids)}")
    require(covered_examples == example_ids, "ablation plan must cover all runnable examples")
    require({"task-outcome", "failure-isolation", "update-cost", "regression-risk", "source-boundary"}.issubset(covered_metrics), "ablation plan must cover all evaluation metrics")

    page_ids = {page.get("id") for page in manifest.get("core_pages", []) if isinstance(page, dict)}
    resource_ids = {resource.get("id") for resource in manifest.get("public_resources", []) if isinstance(resource, dict)}
    require("ablation-plan" in page_ids, "course manifest missing ablation plan page")
    require("ablation-plan" in resource_ids, "course manifest missing ablation plan registry")
    require("ablation-plan-schema" in resource_ids, "course manifest missing ablation plan schema")
    for required in [
        "/ablation-plan.json",
        "/ablation-plan.schema.json",
        "npm run ablation:plan:check",
    ]:
        require(required in page, f"ablation plan page missing {required}")
    for required in [
        "消融计划",
        "ablation-plan.json",
        "npm run ablation:plan:check",
    ]:
        require(
            required in benchmark_protocol
            or required in benchmark_results
            or required in paper_blueprint
            or required in research_projects
            or required in audit
            or required in llms
            or required in public_llms,
            f"ablation plan not linked: {required}",
        )


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked ablation plan with {len(registry['ablations'])} ablations")


if __name__ == "__main__":
    main()
