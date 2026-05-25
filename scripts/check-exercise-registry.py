#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/exercise-registry.json"
SCHEMA_PATH = ROOT / "docs/public/exercise-registry.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/exercises.md"
EXPECTED_SET_IDS = {
    "concept-exercises",
    "code-exercises",
    "experiment-exercises",
    "capstone-exercises",
}
EXPECTED_EXERCISE_IDS = {
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
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


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Exercise Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "exercise_sets"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "exercise_set" in defs and "exercise" in defs, "schema defs drifted")


def path_exists(path: str) -> bool:
    if path.endswith("/"):
        return (ROOT / path).is_dir()
    return (ROOT / path).exists()


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/exercise-registry.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "exercise_sets"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    learning_units = load_json(ROOT / "docs/public/learning-units.json")
    rubric = load_json(ROOT / "docs/public/rubric.json")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    course_map = (ROOT / "docs/zh-cn/course-map/index.md").read_text(encoding="utf-8")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    unit_ids = {
        unit.get("id")
        for unit in learning_units.get("units", [])
        if isinstance(unit, dict) and isinstance(unit.get("id"), str)
    }
    rubric_ids = {
        module.get("id")
        for module in rubric.get("modules", [])
        if isinstance(module, dict) and isinstance(module.get("id"), str)
    }
    example_ids = {
        example.get("id")
        for example in examples.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }

    sets = registry.get("exercise_sets")
    require(isinstance(sets, list) and sets, "exercise_sets must be non-empty")
    set_ids: set[str] = set()
    exercise_ids: set[str] = set()
    for set_index, exercise_set in enumerate(sets):
        context = f"exercise_sets[{set_index}]"
        require(isinstance(exercise_set, dict), f"{context}: must be object")
        require_no_extra_keys(
            exercise_set,
            {"id", "title", "difficulty", "learning_unit_ids", "rubric_module_ids", "exercises"},
            context,
        )
        set_id = exercise_set.get("id")
        require(isinstance(set_id, str) and re.match(r"^[a-z0-9-]+$", set_id), f"{context}: invalid id")
        require(set_id not in set_ids, f"duplicate exercise set id: {set_id}")
        set_ids.add(set_id)
        title = exercise_set.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        require(exercise_set.get("difficulty") in {"concept", "code", "experiment", "capstone"}, f"{context}: invalid difficulty")

        for unit_id in exercise_set.get("learning_unit_ids", []):
            require(unit_id in unit_ids, f"{context}: unknown learning unit id {unit_id}")
        for rubric_id in exercise_set.get("rubric_module_ids", []):
            require(rubric_id in rubric_ids, f"{context}: unknown rubric module id {rubric_id}")

        exercises = exercise_set.get("exercises")
        require(isinstance(exercises, list) and exercises, f"{context}: exercises must be non-empty")
        for exercise_index, exercise in enumerate(exercises):
            item_context = f"{context}.exercises[{exercise_index}]"
            require(isinstance(exercise, dict), f"{item_context}: must be object")
            require_no_extra_keys(
                exercise,
                {"id", "title", "prompt", "input_paths", "example_ids", "deliverable", "verification_commands", "acceptance"},
                item_context,
            )
            exercise_id = exercise.get("id")
            require(isinstance(exercise_id, str) and re.match(r"^[A-D][0-9]+$", exercise_id), f"{item_context}: invalid id")
            require(exercise_id not in exercise_ids, f"duplicate exercise id: {exercise_id}")
            exercise_ids.add(exercise_id)
            title = exercise.get("title")
            require(isinstance(title, str) and title in page, f"{item_context}: title not documented")
            require(exercise_id in page, f"{item_context}: id not documented")
            require(isinstance(exercise.get("prompt"), str) and exercise["prompt"], f"{item_context}: missing prompt")
            require(isinstance(exercise.get("deliverable"), str) and exercise["deliverable"], f"{item_context}: missing deliverable")
            for path in exercise.get("input_paths", []):
                require(isinstance(path, str) and path_exists(path), f"{item_context}: input path missing: {path}")
            for example_id in exercise.get("example_ids", []):
                require(example_id in example_ids, f"{item_context}: unknown example id {example_id}")
            commands = exercise.get("verification_commands")
            require(isinstance(commands, list) and commands, f"{item_context}: commands must be non-empty")
            for command in commands:
                require(isinstance(command, str) and command.startswith("npm run "), f"{item_context}: invalid command {command}")
                script = command.removeprefix("npm run ").split()[0]
                require(script in scripts, f"{item_context}: package script missing for command {command}")
                require(command in page or command in audit, f"{item_context}: command not documented: {command}")
            acceptance = exercise.get("acceptance")
            require(isinstance(acceptance, list) and acceptance, f"{item_context}: acceptance must be non-empty")
            for item in acceptance:
                require(isinstance(item, str) and item, f"{item_context}: acceptance item must be string")

    require(set_ids == EXPECTED_SET_IDS, f"exercise set ids mismatch: {sorted(set_ids)}")
    require(exercise_ids == EXPECTED_EXERCISE_IDS, f"exercise ids mismatch: {sorted(exercise_ids)}")

    for required in [
        "/exercise-registry.json",
        "/exercise-registry.schema.json",
        "npm run exercises:check",
    ]:
        require(required in page, f"exercise page missing public surface: {required}")
    for required in [
        "exercise-registry.json",
        "练习集",
        "npm run exercises:check",
    ]:
        require(required in course_map or required in appendix or required in audit or required in llms or required in public_llms, f"exercise registry not linked: {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    total = sum(len(exercise_set["exercises"]) for exercise_set in registry["exercise_sets"])
    print(f"checked exercise registry with {total} exercises")


if __name__ == "__main__":
    main()
