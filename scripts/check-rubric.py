#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/rubric.json"
SCHEMA_PATH = ROOT / "docs/public/rubric.schema.json"
EXPECTED_IDS = {
    "source-and-problem",
    "probe-and-baseline",
    "heuristic-patch",
    "feedback-report",
    "regression-and-learning-review",
}
EXPECTED_SCORES = {0, 5, 10, 15, 20}


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


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Rubric Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    required = schema.get("required")
    require(isinstance(required, list), "schema required keys must be a list")
    for field in ["schema_version", "modules", "deliverables", "verification_commands"]:
        require(field in required, f"schema missing required field {field}")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "module" in defs and "score_level" in defs, "schema defs drifted")


def normalize_markdown(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("`", "").replace("“", "").replace("”", "").replace("，", "").replace(" ", "")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/rubric.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(
        registry,
        {
            "$schema",
            "schema_version",
            "title",
            "passing_score",
            "minimum_mainline_score",
            "modules",
            "deliverables",
            "verification_commands",
        },
        "registry",
    )
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require(registry.get("passing_score") == 80, "passing_score must stay aligned with rubric page")
    require(registry.get("minimum_mainline_score") == 60, "minimum_mainline_score must stay aligned with rubric page")

    page = (ROOT / "docs/zh-cn/appendix/rubric.md").read_text(encoding="utf-8")
    normalized_page = normalize_markdown(page)
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    instructor = (ROOT / "docs/zh-cn/appendix/instructor-guide.md").read_text(encoding="utf-8")
    course_map = (ROOT / "docs/zh-cn/course-map/index.md").read_text(encoding="utf-8")
    completion_audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    modules = registry.get("modules")
    require(isinstance(modules, list), "modules must be a list")
    ids: set[str] = set()
    total_weight = 0
    allowed_module_keys = {"id", "title", "weight", "minimum_standard", "evidence", "score_levels"}
    allowed_level_keys = {"score", "criterion"}
    for index, module in enumerate(modules):
        context = f"modules[{index}]"
        require(isinstance(module, dict), f"{context}: must be object")
        require_no_extra_keys(module, allowed_module_keys, context)
        module_id = module.get("id")
        require(isinstance(module_id, str) and re.match(r"^[a-z0-9-]+$", module_id), f"{context}: invalid id")
        require(module_id not in ids, f"duplicate module id: {module_id}")
        ids.add(module_id)
        title = module.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        minimum_standard = module.get("minimum_standard")
        require(
            isinstance(minimum_standard, str) and minimum_standard in page,
            f"{context}: minimum standard not documented",
        )
        weight = module.get("weight")
        require(isinstance(weight, int) and weight > 0, f"{context}: invalid weight")
        total_weight += weight
        evidence = module.get("evidence")
        require(isinstance(evidence, list) and evidence, f"{context}: evidence must be non-empty")
        for item in evidence:
            require(isinstance(item, str) and item, f"{context}: evidence item must be string")
            if "*" not in item and item != "tests/":
                require((ROOT / item).exists(), f"{context}: evidence path missing: {item}")
        score_levels = module.get("score_levels")
        require(isinstance(score_levels, list), f"{context}: score_levels must be list")
        scores: set[int] = set()
        for level_index, level in enumerate(score_levels):
            level_context = f"{context}.score_levels[{level_index}]"
            require(isinstance(level, dict), f"{level_context}: must be object")
            require_no_extra_keys(level, allowed_level_keys, level_context)
            score = level.get("score")
            criterion = level.get("criterion")
            require(isinstance(score, int), f"{level_context}: score must be integer")
            require(
                isinstance(criterion, str) and normalize_markdown(criterion) in normalized_page,
                f"{level_context}: criterion not documented",
            )
            scores.add(score)
        require(scores == EXPECTED_SCORES, f"{context}: score levels mismatch {sorted(scores)}")

    require(ids == EXPECTED_IDS, f"rubric module ids mismatch: {sorted(ids)}")
    require(total_weight == 100, f"rubric weights must sum to 100, got {total_weight}")

    deliverables = registry.get("deliverables")
    require(isinstance(deliverables, list) and deliverables, "deliverables must be non-empty")
    for deliverable in deliverables:
        require(isinstance(deliverable, str) and deliverable in page, f"deliverable not documented: {deliverable}")

    commands = registry.get("verification_commands")
    require(isinstance(commands, list) and commands, "verification_commands must be non-empty")
    for command in commands:
        require(isinstance(command, str) and command.startswith("npm run "), f"invalid command: {command}")
        script = command.removeprefix("npm run ").split()[0]
        require(script in scripts, f"package script missing for command {command}")
        require(command in page or command in completion_audit, f"command not documented: {command}")

    for required in [
        "/rubric.json",
        "/rubric.schema.json",
        "npm run rubric:check",
    ]:
        require(required in page, f"rubric page missing public surface: {required}")
    require("rubric.json" in appendix, "appendix must link rubric.json")
    require("rubric.json" in instructor or "rubric.json" in course_map, "teaching docs must link rubric.json")
    require("rubric.json" in completion_audit, "completion audit must include rubric.json")
    require("docs/public/rubric.json" in llms, "root llms.txt missing rubric.json")
    require("/rubric.json" in public_llms, "public llms.txt missing rubric route")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked rubric with {len(registry['modules'])} modules")


if __name__ == "__main__":
    main()
