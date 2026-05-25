#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/slide-deck.json"
SCHEMA_PATH = ROOT / "docs/public/slide-deck.schema.json"
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


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Slide Deck Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "materials"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "material" in defs, "schema must define material")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/slide-deck.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "materials"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    teaching = load_json(ROOT / "docs/public/teaching-registry.json")
    example_registry = load_json(ROOT / "docs/public/example-registry.json")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    teaching_ids = {
        material.get("id")
        for material in teaching.get("materials", [])
        if isinstance(material, dict) and isinstance(material.get("id"), str)
    }
    example_ids = {
        example.get("id")
        for example in example_registry.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    slides_index = (ROOT / "docs/zh-cn/slides/index.md").read_text(encoding="utf-8")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")
    verify = (ROOT / "scripts/verify.sh").read_text(encoding="utf-8")

    materials = registry.get("materials")
    require(isinstance(materials, list) and materials, "materials must be a non-empty list")
    ids: set[str] = set()
    allowed = {
        "id",
        "path",
        "route",
        "format",
        "required_headings",
        "example_ids",
        "commands",
        "deliverable_template",
    }
    for index, material in enumerate(materials):
        context = f"materials[{index}]"
        require(isinstance(material, dict), f"{context}: must be object")
        require_no_extra_keys(material, allowed, context)
        material_id = material.get("id")
        require(isinstance(material_id, str) and re.match(r"^(lecture|lab)-[0-9]+$", material_id), f"{context}: invalid id")
        require(material_id not in ids, f"duplicate material id: {material_id}")
        ids.add(material_id)
        require(material_id in teaching_ids, f"{context}: missing from teaching registry: {material_id}")
        require(material.get("format") in {"lecture", "lab"}, f"{context}: invalid format")

        path = ROOT / str(material.get("path"))
        require(path.exists(), f"{context}: material path missing: {material.get('path')}")
        text = path.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"{context}: material page missing frontmatter")
        require(material.get("route") in slides_index or path.name == "index.md", f"{context}: route not linked")

        headings = material.get("required_headings")
        require(isinstance(headings, list) and headings, f"{context}: required_headings must be non-empty")
        for heading in headings:
            require(isinstance(heading, str) and heading in text, f"{context}: heading missing: {heading}")

        material_examples = material.get("example_ids")
        require(isinstance(material_examples, list) and material_examples, f"{context}: example_ids must be non-empty")
        for example_id in material_examples:
            require(example_id in example_ids, f"{context}: unknown example id: {example_id}")

        commands = material.get("commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command: {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in text, f"{context}: command not documented in material: {command}")

        template = material.get("deliverable_template")
        require(isinstance(template, str) and (ROOT / template).exists(), f"{context}: deliverable template missing: {template}")

    require(ids == EXPECTED_IDS, f"slide deck ids mismatch: {sorted(ids)}")
    for required in [
        "/slide-deck.json",
        "/slide-deck.schema.json",
        "npm run slides:check",
    ]:
        require(required in slides_index or required in appendix or required in verify, f"slide deck surface missing: {required}")
    require("docs/public/slide-deck.json" in llms, "root llms.txt missing slide-deck.json")
    require("/slide-deck.json" in public_llms, "public llms.txt missing slide-deck route")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked slide deck with {len(registry['materials'])} materials")


if __name__ == "__main__":
    main()
