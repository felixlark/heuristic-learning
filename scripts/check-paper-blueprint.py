#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/paper-blueprint.json"
SCHEMA_PATH = ROOT / "docs/public/paper-blueprint.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/paper-blueprint.md"
EXPECTED_IDS = {
    "abstract-and-positioning",
    "problem-and-related-work",
    "method-learning-loop",
    "experiments-and-results",
    "discussion-and-threats",
    "course-and-reuse",
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
    if "*" in path:
        return bool(list(ROOT.glob(path)))
    if path.endswith("/"):
        return (ROOT / path).is_dir()
    return (ROOT / path).exists()


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Paper Blueprint Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "sections"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/paper-blueprint.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    claims = load_json(ROOT / "docs/public/claims-registry.json")
    metrics = load_json(ROOT / "docs/public/evaluation-metrics.json")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    reading_guide = (ROOT / "docs/zh-cn/appendix/reading-guide.md").read_text(encoding="utf-8")
    propositions = (ROOT / "docs/zh-cn/theory/research-propositions.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs/zh-cn/appendix/research-roadmap.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    claim_ids = {claim.get("id") for claim in claims.get("claims", []) if isinstance(claim, dict)}
    metric_ids = {metric.get("id") for metric in metrics.get("metrics", []) if isinstance(metric, dict)}
    example_ids = {example.get("id") for example in examples.get("examples", []) if isinstance(example, dict)}

    sections = registry.get("sections")
    require(isinstance(sections, list) and sections, "sections must be non-empty")
    ids: set[str] = set()
    covered_claims: set[str] = set()
    covered_metrics: set[str] = set()
    covered_examples: set[str] = set()
    for index, section in enumerate(sections):
        context = f"sections[{index}]"
        require(isinstance(section, dict), f"{context}: must be object")
        require(
            set(section)
            == {
                "id",
                "title",
                "purpose",
                "claim_ids",
                "metric_ids",
                "example_ids",
                "evidence",
                "verification_commands",
                "writing_prompt",
                "boundary",
            },
            f"{context}: unexpected keys",
        )
        section_id = section.get("id")
        require(isinstance(section_id, str), f"{context}: id must be string")
        require(section_id not in ids, f"duplicate section id: {section_id}")
        ids.add(section_id)
        title = section.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        require(isinstance(section.get("purpose"), str) and section["purpose"], f"{context}: purpose missing")
        require(isinstance(section.get("writing_prompt"), str) and section["writing_prompt"], f"{context}: writing_prompt missing")
        require(isinstance(section.get("boundary"), str) and section["boundary"], f"{context}: boundary missing")
        for claim_id in section.get("claim_ids", []):
            require(claim_id in claim_ids, f"{context}: unknown claim id {claim_id}")
            covered_claims.add(claim_id)
        for metric_id in section.get("metric_ids", []):
            require(metric_id in metric_ids, f"{context}: unknown metric id {metric_id}")
            covered_metrics.add(metric_id)
        for example_id in section.get("example_ids", []):
            require(example_id in example_ids, f"{context}: unknown example id {example_id}")
            covered_examples.add(example_id)
        for evidence in section.get("evidence", []):
            require(isinstance(evidence, str) and path_exists(evidence), f"{context}: evidence missing: {evidence}")
        for command in section.get("verification_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command in audit, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"paper blueprint ids mismatch: {sorted(ids)}")
    require(claim_ids.issubset(covered_claims), "paper blueprint must cover all claims")
    require(metric_ids.issubset(covered_metrics), "paper blueprint must cover all evaluation metrics")
    require(example_ids.issubset(covered_examples), "paper blueprint must cover all runnable examples")

    page_ids = {page.get("id") for page in manifest.get("core_pages", []) if isinstance(page, dict)}
    resource_ids = {resource.get("id") for resource in manifest.get("public_resources", []) if isinstance(resource, dict)}
    require("paper-blueprint" in page_ids, "course manifest missing paper blueprint page")
    require("paper-blueprint" in resource_ids, "course manifest missing paper blueprint registry")
    require("paper-blueprint-schema" in resource_ids, "course manifest missing paper blueprint schema")
    for required in [
        "/paper-blueprint.json",
        "/paper-blueprint.schema.json",
        "npm run paper:blueprint:check",
    ]:
        require(required in page, f"paper blueprint page missing {required}")
    for required in [
        "论文蓝图",
        "paper-blueprint.json",
        "npm run paper:blueprint:check",
    ]:
        require(
            required in reading_guide
            or required in propositions
            or required in roadmap
            or required in audit
            or required in llms
            or required in public_llms,
            f"paper blueprint not linked: {required}",
        )


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked paper blueprint with {len(registry['sections'])} sections")


if __name__ == "__main__":
    main()
