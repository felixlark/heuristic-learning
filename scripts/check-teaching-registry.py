#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/teaching-registry.json"
SCHEMA_PATH = ROOT / "docs/public/teaching-registry.schema.json"
EXPECTED_IDS = {"lecture-1", "lecture-2", "lecture-3", "lab-1", "lab-2"}


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
    require(schema.get("title") == "Heuristic Learning Teaching Registry", "schema title mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "materials"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "material" in defs, "schema must define material")
    required = defs["material"].get("required")
    require(isinstance(required, list), "schema material required must be a list")
    for field in ["id", "type", "title", "path", "route", "core_question", "reading", "commands", "deliverable"]:
        require(field in required, f"schema material missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/teaching-registry.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "materials"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    materials = registry.get("materials")
    require(isinstance(materials, list) and materials, "materials must be a non-empty list")
    ids: set[str] = set()
    allowed = {"id", "type", "title", "path", "route", "core_question", "reading", "commands", "deliverable"}
    slides_index = (ROOT / "docs/zh-cn/slides/index.md").read_text(encoding="utf-8")
    schedule = (ROOT / "docs/zh-cn/appendix/course-schedule.md").read_text(encoding="utf-8")

    for index, material in enumerate(materials):
        context = f"materials[{index}]"
        require(isinstance(material, dict), f"{context}: must be object")
        require_no_extra_keys(material, allowed, context)
        require_pattern(material.get("id"), r"^(lecture|lab)-[0-9]+$", f"{context}.id")
        material_id = material["id"]
        require(material_id not in ids, f"duplicate material id: {material_id}")
        ids.add(material_id)
        require(material.get("type") in {"lecture", "lab"}, f"{context}: invalid material type")
        require(isinstance(material.get("title"), str) and material["title"], f"{context}: missing title")
        require(isinstance(material.get("core_question"), str) and material["core_question"], f"{context}: missing core_question")
        require(isinstance(material.get("deliverable"), str) and material["deliverable"], f"{context}: missing deliverable")

        path = ROOT / material["path"]
        require(path.exists(), f"{context}: material path missing: {material['path']}")
        text = path.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"{context}: material page missing frontmatter")
        require(material["title"] in text, f"{context}: material title missing from page")
        require(material["route"] in slides_index or material["title"] in slides_index, f"{context}: missing from slides index")

        reading = material.get("reading")
        require(isinstance(reading, list) and reading, f"{context}: reading must be non-empty")
        for item in reading:
            require(isinstance(item, str), f"{context}: reading item must be string")
            require((ROOT / item).exists(), f"{context}: reading path missing: {item}")

        commands = material.get("commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str), f"{context}: command must be string")
            require(command.startswith("npm run "), f"{context}: command must be npm script: {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in text or command in schedule, f"{context}: command not documented in material or schedule: {command}")

    require(ids == EXPECTED_IDS, f"teaching registry ids mismatch: {sorted(ids)}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked teaching registry with {len(registry['materials'])} materials")


if __name__ == "__main__":
    main()
