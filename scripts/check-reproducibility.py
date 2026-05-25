#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/reproducibility-checklist.json"
SCHEMA_PATH = ROOT / "docs/public/reproducibility-checklist.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/reproducibility.md"
EXPECTED_IDS = {
    "environment-and-install",
    "runnable-examples",
    "claims-and-sources",
    "teaching-artifacts",
    "contribution-and-release",
    "site-and-machine-entrypoints",
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
    require(schema.get("title") == "Heuristic Learning Reproducibility Checklist", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "checklists"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/reproducibility-checklist.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    page = PAGE_PATH.read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    checklists = registry.get("checklists")
    require(isinstance(checklists, list) and checklists, "checklists must be non-empty")
    ids: set[str] = set()
    for index, item in enumerate(checklists):
        context = f"checklists[{index}]"
        require(isinstance(item, dict), f"{context}: must be object")
        require(set(item) == {"id", "title", "scope", "evidence", "commands", "pass_condition", "known_boundary"}, f"{context}: unexpected keys")
        item_id = item.get("id")
        require(isinstance(item_id, str) and re.match(r"^[a-z0-9-]+$", item_id), f"{context}: invalid id")
        require(item_id not in ids, f"duplicate checklist id: {item_id}")
        ids.add(item_id)
        title = item.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        require(isinstance(item.get("scope"), str) and item["scope"], f"{context}: missing scope")
        for evidence in item.get("evidence", []):
            require(isinstance(evidence, str) and path_exists(evidence), f"{context}: evidence path missing: {evidence}")
        commands = item.get("commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str), f"{context}: command must be string")
            if command.startswith("npm run "):
                script = command.removeprefix("npm run ").split()[0]
                require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in page or command == "npm install", f"{context}: command not documented on page: {command}")
        require(isinstance(item.get("pass_condition"), str) and item["pass_condition"], f"{context}: missing pass_condition")
        boundary = item.get("known_boundary")
        require(isinstance(boundary, str) and boundary, f"{context}: missing known_boundary")
    require(ids == EXPECTED_IDS, f"reproducibility checklist ids mismatch: {sorted(ids)}")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("reproducibility-checklist" in resource_ids, "course manifest missing reproducibility checklist")
    require("reproducibility-checklist-schema" in resource_ids, "course manifest missing reproducibility schema")

    for required in [
        "/reproducibility-checklist.json",
        "/reproducibility-checklist.schema.json",
        "npm run reproducibility:check",
    ]:
        require(required in page, f"reproducibility page missing public surface: {required}")
    for required in [
        "reproducibility-checklist.json",
        "可复现性检查清单",
        "npm run reproducibility:check",
    ]:
        require(required in appendix or required in audit or required in llms or required in public_llms, f"reproducibility checklist not linked: {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked reproducibility checklist with {len(registry['checklists'])} checks")


if __name__ == "__main__":
    main()
