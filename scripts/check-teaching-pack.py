#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/teaching-pack.json"
SCHEMA_PATH = ROOT / "docs/public/teaching-pack.schema.json"
EXPECTED_IDS = {
    "tp0-quick-orientation",
    "tp1-hands-on-workshop",
    "tp2-research-seminar",
    "tp3-project-course",
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
    require(schema.get("title") == "Heuristic Learning Teaching Pack Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "packs"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "pack" in defs, "schema must define pack")
    required = defs["pack"].get("required")
    require(isinstance(required, list), "schema pack required must be a list")
    for field in ["id", "title", "duration", "audience", "slides", "readings", "demo_commands", "deliverable", "acceptance"]:
        require(field in required, f"schema pack missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/teaching-pack.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "packs"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    page = (ROOT / "docs/zh-cn/appendix/teaching-pack.md").read_text(encoding="utf-8")
    manifest = (ROOT / "docs/public/course-manifest.json").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    packs = registry.get("packs")
    require(isinstance(packs, list) and packs, "packs must be a non-empty list")
    ids: set[str] = set()
    allowed = {"id", "title", "duration", "audience", "slides", "readings", "demo_commands", "deliverable", "acceptance"}
    for index, pack in enumerate(packs):
        context = f"packs[{index}]"
        require(isinstance(pack, dict), f"{context}: must be object")
        require_no_extra_keys(pack, allowed, context)
        require_pattern(pack.get("id"), r"^tp[0-9]-[a-z0-9-]+$", f"{context}.id")
        pack_id = pack["id"]
        require(pack_id not in ids, f"duplicate pack id: {pack_id}")
        ids.add(pack_id)
        for key in ["title", "duration", "audience", "deliverable"]:
            require(isinstance(pack.get(key), str) and pack[key], f"{context}: missing {key}")
        require(pack["title"] in page, f"{context}: title not documented")
        require(pack["deliverable"] in page, f"{context}: deliverable not documented")

        for key in ["slides", "readings"]:
            items = pack.get(key)
            require(isinstance(items, list) and items, f"{context}: {key} must be non-empty")
            for item in items:
                require(isinstance(item, str), f"{context}: {key} item must be string")
                require((ROOT / item).exists(), f"{context}: {key} path missing: {item}")

        commands = pack.get("demo_commands")
        require(isinstance(commands, list) and commands, f"{context}: demo_commands must be non-empty")
        for command in commands:
            require(isinstance(command, str), f"{context}: command must be string")
            require(command.startswith("npm run "), f"{context}: command must be npm script: {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in page, f"{context}: command not documented: {command}")

        acceptance = pack.get("acceptance")
        require(isinstance(acceptance, list) and acceptance, f"{context}: acceptance must be non-empty")

    require(ids == EXPECTED_IDS, f"teaching pack ids mismatch: {sorted(ids)}")
    require("docs/zh-cn/appendix/teaching-pack.md" in manifest, "course manifest must include teaching pack page")
    require("docs/public/teaching-pack.json" in llms, "root llms.txt missing teaching-pack.json")
    require("/teaching-pack.json" in public_llms, "public llms.txt missing teaching-pack route")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked teaching pack with {len(registry['packs'])} packs")


if __name__ == "__main__":
    main()
