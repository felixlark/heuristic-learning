#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/code-tour.json"
SCHEMA_PATH = ROOT / "docs/public/code-tour.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/code-tour.md"

EXPECTED_IDS = {
    "gridworld-code-tour",
    "robot-soccer-code-tour",
    "vizdoom-code-tour",
    "traffic-grid-code-tour",
    "breakout-code-tour",
    "ant-gait-code-tour",
    "constraint-audit-code-tour",
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
    require(schema.get("title") == "Heuristic Learning Code Tour Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "scope", "tours"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/code-tour.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require(registry.get("scope") == "runnable-example-code-reading-order", "registry scope mismatch")

    page = PAGE_PATH.read_text(encoding="utf-8")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    example_ids = {item.get("id") for item in examples.get("examples", []) if isinstance(item, dict)}
    tours = registry.get("tours")
    require(isinstance(tours, list) and tours, "tours must be non-empty")
    ids: set[str] = set()
    covered_examples: set[str] = set()
    for index, tour in enumerate(tours):
        context = f"tours[{index}]"
        require(isinstance(tour, dict), f"{context}: must be object")
        require(
            set(tour)
            == {
                "id",
                "example_id",
                "title",
                "reading_order",
                "key_question",
                "run_commands",
                "expected_observation",
                "edit_target",
                "test_path",
                "boundary",
            },
            f"{context}: unexpected keys",
        )
        tour_id = tour.get("id")
        require(isinstance(tour_id, str), f"{context}: id must be string")
        require(tour_id not in ids, f"duplicate tour id: {tour_id}")
        ids.add(tour_id)
        title = tour.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        example_id = tour.get("example_id")
        require(example_id in example_ids, f"{context}: unknown example id {example_id}")
        covered_examples.add(example_id)
        reading_order = tour.get("reading_order")
        require(isinstance(reading_order, list) and len(reading_order) >= 3, f"{context}: reading_order too short")
        for item in reading_order:
            require(isinstance(item, str) and (ROOT / item).exists(), f"{context}: reading file missing: {item}")
        edit_target = tour.get("edit_target")
        test_path = tour.get("test_path")
        require(isinstance(edit_target, str) and (ROOT / edit_target).exists(), f"{context}: edit target missing")
        require(isinstance(test_path, str) and (ROOT / test_path).exists(), f"{context}: test path missing")
        for command in tour.get("run_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page, f"{context}: command not documented: {command}")
        for field in ["key_question", "expected_observation", "boundary"]:
            require(isinstance(tour.get(field), str) and tour[field], f"{context}: {field} missing")

    require(ids == EXPECTED_IDS, f"code tour ids mismatch: {sorted(ids)}")
    require(covered_examples == example_ids, "code tour must cover all runnable examples")
    page_ids = {item.get("id") for item in manifest.get("core_pages", []) if isinstance(item, dict)}
    resource_ids = {item.get("id") for item in manifest.get("public_resources", []) if isinstance(item, dict)}
    require("code-tour" in page_ids, "course manifest missing code tour page")
    require("code-tour" in resource_ids, "course manifest missing code tour registry")
    require("code-tour-schema" in resource_ids, "course manifest missing code tour schema")
    for required in [
        "/code-tour.json",
        "/code-tour.schema.json",
        "npm run code:tour:check",
        "reading_order",
        "edit_target",
    ]:
        require(required in page, f"code tour page missing {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked code tour with {len(registry['tours'])} tours")


if __name__ == "__main__":
    main()
