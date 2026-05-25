#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/course-patterns.json"
SCHEMA_PATH = ROOT / "docs/public/course-patterns.schema.json"
EXPECTED_IDS = {
    "easy-vibe-course-chassis",
    "d2l-theory-code-exercises",
    "llm-c-readable-research-code",
    "easy-rl-shared-vocabulary",
}
EXPECTED_REFERENCES = {
    "datawhalechina/easy-vibe",
    "d2l-ai/d2l-zh",
    "karpathy/llm.c",
    "datawhalechina/easy-rl",
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
    require(schema.get("title") == "Heuristic Learning Course Patterns Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "patterns"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "pattern" in defs, "schema must define pattern")
    required = defs["pattern"].get("required")
    require(isinstance(required, list), "schema pattern required must be a list")
    for field in ["id", "reference", "borrowed_pattern", "repo_evidence", "verification", "boundary"]:
        require(field in required, f"schema pattern missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/course-patterns.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "patterns"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    page = (ROOT / "docs/zh-cn/appendix/course-patterns.md").read_text(encoding="utf-8")
    manifest = (ROOT / "docs/public/course-manifest.json").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    patterns = registry.get("patterns")
    require(isinstance(patterns, list) and patterns, "patterns must be a non-empty list")
    ids: set[str] = set()
    references: set[str] = set()
    allowed = {"id", "reference", "borrowed_pattern", "repo_evidence", "verification", "boundary"}
    for index, pattern in enumerate(patterns):
        context = f"patterns[{index}]"
        require(isinstance(pattern, dict), f"{context}: must be object")
        require_no_extra_keys(pattern, allowed, context)
        require_pattern(pattern.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        pattern_id = pattern["id"]
        require(pattern_id not in ids, f"duplicate pattern id: {pattern_id}")
        ids.add(pattern_id)
        reference = pattern.get("reference")
        require(isinstance(reference, str) and reference, f"{context}: missing reference")
        references.add(reference)
        require(reference in page, f"{context}: reference not documented on course patterns page")
        require(isinstance(pattern.get("borrowed_pattern"), str) and pattern["borrowed_pattern"], f"{context}: missing borrowed_pattern")
        require(isinstance(pattern.get("boundary"), str) and pattern["boundary"], f"{context}: missing boundary")

        evidence = pattern.get("repo_evidence")
        require(isinstance(evidence, list) and evidence, f"{context}: repo_evidence must be non-empty")
        for item in evidence:
            require(isinstance(item, str), f"{context}: evidence item must be string")
            require((ROOT / item).exists(), f"{context}: evidence path missing: {item}")

        verification = pattern.get("verification")
        require(isinstance(verification, list) and verification, f"{context}: verification must be non-empty")
        for command in verification:
            require(isinstance(command, str), f"{context}: command must be string")
            require(command.startswith("npm run "), f"{context}: command must be npm script: {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in page, f"{context}: verification command not documented: {command}")

    require(ids == EXPECTED_IDS, f"course pattern ids mismatch: {sorted(ids)}")
    require(references == EXPECTED_REFERENCES, f"course pattern references mismatch: {sorted(references)}")
    require("docs/zh-cn/appendix/course-patterns.md" in manifest, "course manifest must include course patterns page")
    require("course-patterns.schema.json" in page, "course patterns page must link schema")
    require("docs/public/course-patterns.json" in llms, "root llms.txt missing course-patterns.json")
    require("/course-patterns.json" in public_llms, "public llms.txt missing course-patterns route")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked course patterns with {len(registry['patterns'])} patterns")


if __name__ == "__main__":
    main()
