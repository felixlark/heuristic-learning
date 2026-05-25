#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/learning-units.json"
SCHEMA_PATH = ROOT / "docs/public/learning-units.schema.json"
EXPECTED_IDS = {
    "u0-context",
    "u1-minimal-loop",
    "u2-public-artifacts",
    "u3-control-and-systems",
    "u4-research-claims",
    "u5-anti-forgetting-project",
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


def require_pattern(value: Any, pattern: str, context: str) -> None:
    require(isinstance(value, str), f"{context}: expected string")
    require(re.match(pattern, value), f"{context}: does not match {pattern}: {value}")


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Units Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "units"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "unit" in defs, "schema must define unit")
    required = defs["unit"].get("required")
    require(isinstance(required, list), "schema unit required must be a list")
    for field in ["id", "title", "core_question", "readings", "examples", "commands", "deliverable", "acceptance"]:
        require(field in required, f"schema unit missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/learning-units.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "units"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    example_registry = load_json(ROOT / "docs/public/example-registry.json")
    example_ids = {
        example.get("id")
        for example in example_registry.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    page = (ROOT / "docs/zh-cn/appendix/learning-units.md").read_text(encoding="utf-8")
    manifest = (ROOT / "docs/public/course-manifest.json").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    units = registry.get("units")
    require(isinstance(units, list) and units, "units must be a non-empty list")
    ids: set[str] = set()
    allowed = {"id", "title", "core_question", "readings", "examples", "commands", "deliverable", "acceptance"}
    for index, unit in enumerate(units):
        context = f"units[{index}]"
        require(isinstance(unit, dict), f"{context}: must be object")
        require_no_extra_keys(unit, allowed, context)
        require_pattern(unit.get("id"), r"^u[0-9]-[a-z0-9-]+$", f"{context}.id")
        unit_id = unit["id"]
        require(unit_id not in ids, f"duplicate unit id: {unit_id}")
        ids.add(unit_id)
        require(unit.get("title") in page, f"{context}: unit title not documented")
        require(isinstance(unit.get("core_question"), str) and unit["core_question"], f"{context}: missing core_question")
        require(isinstance(unit.get("deliverable"), str) and unit["deliverable"], f"{context}: missing deliverable")

        readings = unit.get("readings")
        require(isinstance(readings, list) and readings, f"{context}: readings must be non-empty")
        for item in readings:
            require(isinstance(item, str), f"{context}: reading item must be string")
            require((ROOT / item).exists(), f"{context}: reading path missing: {item}")

        examples = unit.get("examples")
        require(isinstance(examples, list), f"{context}: examples must be a list")
        for example_id in examples:
            require(example_id in example_ids, f"{context}: unknown example id: {example_id}")

        commands = unit.get("commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str), f"{context}: command must be string")
            require(command.startswith("npm run "), f"{context}: command must be npm script: {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in page, f"{context}: command not documented on learning units page: {command}")

        acceptance = unit.get("acceptance")
        require(isinstance(acceptance, list) and acceptance, f"{context}: acceptance must be non-empty")
        require(unit["deliverable"] in page, f"{context}: deliverable not documented")

    require(ids == EXPECTED_IDS, f"learning unit ids mismatch: {sorted(ids)}")
    require("docs/zh-cn/appendix/learning-units.md" in manifest, "course manifest must include learning units page")
    require("docs/public/learning-units.json" in llms, "root llms.txt missing learning-units.json")
    require("/learning-units.json" in public_llms, "public llms.txt missing learning-units route")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked learning units with {len(registry['units'])} units")


if __name__ == "__main__":
    main()
