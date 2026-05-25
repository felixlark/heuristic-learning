#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/evaluation-metrics.json"
SCHEMA_PATH = ROOT / "docs/public/evaluation-metrics.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/evaluation-metrics.md"
EXPECTED_IDS = {
    "task-outcome",
    "failure-isolation",
    "update-cost",
    "regression-risk",
    "source-boundary",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing JSON file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"JSON root must be object: {path.relative_to(ROOT)}")
    return data


def path_exists(path: str) -> bool:
    if path.endswith("/"):
        return (ROOT / path).is_dir()
    return (ROOT / path).exists()


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Evaluation Metrics Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "metrics"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/evaluation-metrics.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    claims = load_json(ROOT / "docs/public/claims-registry.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    framework = (ROOT / "docs/zh-cn/theory/research-framework.md").read_text(encoding="utf-8")
    propositions = (ROOT / "docs/zh-cn/theory/research-propositions.md").read_text(encoding="utf-8")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    example_ids = {example.get("id") for example in examples.get("examples", []) if isinstance(example, dict)}
    claim_ids = {claim.get("id") for claim in claims.get("claims", []) if isinstance(claim, dict)}

    metrics = registry.get("metrics")
    require(isinstance(metrics, list) and metrics, "metrics must be non-empty")
    ids: set[str] = set()
    covered_examples: set[str] = set()
    covered_claims: set[str] = set()
    for index, metric in enumerate(metrics):
        context = f"metrics[{index}]"
        require(isinstance(metric, dict), f"{context}: must be object")
        require(
            set(metric)
            == {
                "id",
                "title",
                "research_question",
                "definition",
                "example_ids",
                "claim_ids",
                "evidence",
                "verification_commands",
                "failure_mode",
                "course_use",
            },
            f"{context}: unexpected keys",
        )
        metric_id = metric.get("id")
        require(isinstance(metric_id, str), f"{context}: id must be string")
        require(metric_id not in ids, f"duplicate metric id: {metric_id}")
        ids.add(metric_id)
        title = metric.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        require(isinstance(metric.get("research_question"), str) and metric["research_question"], f"{context}: research_question missing")
        require(isinstance(metric.get("definition"), str) and metric["definition"], f"{context}: definition missing")
        require(isinstance(metric.get("failure_mode"), str) and metric["failure_mode"], f"{context}: failure_mode missing")
        require(isinstance(metric.get("course_use"), str) and metric["course_use"], f"{context}: course_use missing")
        for example_id in metric.get("example_ids", []):
            require(example_id in example_ids or example_id == "x-signal", f"{context}: unknown example id {example_id}")
            covered_examples.add(example_id)
        for claim_id in metric.get("claim_ids", []):
            require(claim_id in claim_ids, f"{context}: unknown claim id {claim_id}")
            covered_claims.add(claim_id)
        for evidence in metric.get("evidence", []):
            require(isinstance(evidence, str) and path_exists(evidence), f"{context}: evidence missing: {evidence}")
        for command in metric.get("verification_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command in audit, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"metric ids mismatch: {sorted(ids)}")
    require(example_ids.issubset(covered_examples), "metrics must cover all runnable examples")
    require(claim_ids.issubset(covered_claims), "metrics must cover core claims")

    page_ids = {page.get("id") for page in manifest.get("core_pages", []) if isinstance(page, dict)}
    resource_ids = {resource.get("id") for resource in manifest.get("public_resources", []) if isinstance(resource, dict)}
    require("evaluation-metrics" in page_ids, "course manifest missing evaluation metrics page")
    require("evaluation-metrics" in resource_ids, "course manifest missing evaluation metrics registry")
    require("evaluation-metrics-schema" in resource_ids, "course manifest missing evaluation metrics schema")
    for required in [
        "/evaluation-metrics.json",
        "/evaluation-metrics.schema.json",
        "npm run metrics:check",
    ]:
        require(required in page, f"evaluation metrics page missing {required}")
    for required in [
        "评估指标矩阵",
        "evaluation-metrics.json",
        "npm run metrics:check",
    ]:
        require(
            required in framework
            or required in propositions
            or required in appendix
            or required in audit
            or required in llms
            or required in public_llms,
            f"evaluation metrics not linked: {required}",
        )


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked evaluation metrics registry with {len(registry['metrics'])} metrics")


if __name__ == "__main__":
    main()
