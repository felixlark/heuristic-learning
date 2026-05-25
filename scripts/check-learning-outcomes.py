#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/learning-outcomes.json"
SCHEMA_PATH = ROOT / "docs/public/learning-outcomes.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/learning-outcomes.md"
EXPECTED_IDS = {"lo-1", "lo-2", "lo-3", "lo-4", "lo-5"}


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
    require(schema.get("title") == "Heuristic Learning Outcomes Registry", "schema title mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "outcomes"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/learning-outcomes.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    page = PAGE_PATH.read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    units = load_json(ROOT / "docs/public/learning-units.json")
    exercises = load_json(ROOT / "docs/public/exercise-registry.json")
    rubric = load_json(ROOT / "docs/public/rubric.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    syllabus = (ROOT / "docs/zh-cn/syllabus/index.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    unit_ids = {unit["id"] for unit in units.get("units", []) if isinstance(unit, dict) and "id" in unit}
    exercise_ids = {
        exercise["id"]
        for exercise_set in exercises.get("exercise_sets", [])
        if isinstance(exercise_set, dict)
        for exercise in exercise_set.get("exercises", [])
        if isinstance(exercise, dict) and "id" in exercise
    }
    rubric_ids = {module["id"] for module in rubric.get("modules", []) if isinstance(module, dict) and "id" in module}

    outcomes = registry.get("outcomes")
    require(isinstance(outcomes, list) and outcomes, "outcomes must be non-empty")
    ids: set[str] = set()
    for index, outcome in enumerate(outcomes):
        context = f"outcomes[{index}]"
        require(isinstance(outcome, dict), f"{context}: must be object")
        require(
            set(outcome)
            == {
                "id",
                "title",
                "competency",
                "learning_unit_ids",
                "exercise_ids",
                "rubric_module_ids",
                "evidence",
                "assessment",
                "verification_commands",
            },
            f"{context}: unexpected keys",
        )
        outcome_id = outcome.get("id")
        require(isinstance(outcome_id, str) and re.match(r"^lo-[0-9]+$", outcome_id), f"{context}: invalid id")
        require(outcome_id not in ids, f"duplicate outcome id: {outcome_id}")
        ids.add(outcome_id)
        title = outcome.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        require(isinstance(outcome.get("competency"), str) and outcome["competency"], f"{context}: missing competency")
        for unit_id in outcome.get("learning_unit_ids", []):
            require(unit_id in unit_ids, f"{context}: unknown learning unit id {unit_id}")
        for exercise_id in outcome.get("exercise_ids", []):
            require(exercise_id in exercise_ids, f"{context}: unknown exercise id {exercise_id}")
            require(exercise_id in page, f"{context}: exercise id not documented: {exercise_id}")
        for rubric_id in outcome.get("rubric_module_ids", []):
            require(rubric_id in rubric_ids, f"{context}: unknown rubric module id {rubric_id}")
        for evidence in outcome.get("evidence", []):
            require(isinstance(evidence, str) and path_exists(evidence), f"{context}: evidence path missing: {evidence}")
        require(isinstance(outcome.get("assessment"), str) and outcome["assessment"], f"{context}: missing assessment")
        commands = outcome.get("verification_commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in page or command in audit, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"learning outcome ids mismatch: {sorted(ids)}")
    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("learning-outcomes" in resource_ids, "course manifest missing learning-outcomes resource")
    require("learning-outcomes-schema" in resource_ids, "course manifest missing learning-outcomes schema resource")

    for required in [
        "/learning-outcomes.json",
        "/learning-outcomes.schema.json",
        "npm run learning:outcomes:check",
    ]:
        require(required in page, f"learning outcomes page missing public surface: {required}")
    for required in [
        "learning-outcomes.json",
        "学习成果矩阵",
        "npm run learning:outcomes:check",
    ]:
        require(required in appendix or required in syllabus or required in audit or required in llms or required in public_llms, f"learning outcomes not linked: {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked learning outcomes with {len(registry['outcomes'])} outcomes")


if __name__ == "__main__":
    main()
