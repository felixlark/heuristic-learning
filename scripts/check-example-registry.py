#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/example-registry.json"
SCHEMA_PATH = ROOT / "docs/public/example-registry.schema.json"
COURSE_MANIFEST_PATH = ROOT / "docs/public/course-manifest.json"


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
    require(schema.get("title") == "Heuristic Learning Example Registry", "schema title mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "examples"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "example" in defs, "schema must define example")
    required = defs["example"].get("required")
    require(isinstance(required, list), "schema example required must be a list")
    for field in [
        "id",
        "title",
        "failure_mode",
        "source_status",
        "example_dir",
        "run_script",
        "feedback_script",
        "report",
        "test",
        "policy_target",
        "course_links",
    ]:
        require(field in required, f"schema example missing required field {field}")


def check_registry(registry: dict[str, Any], manifest: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/example-registry.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "examples"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    manifest_examples = manifest.get("examples")
    require(isinstance(manifest_examples, list), "course manifest examples must be a list")
    manifest_by_id = {
        example.get("id"): example
        for example in manifest_examples
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }

    examples = registry.get("examples")
    require(isinstance(examples, list) and examples, "registry examples must be a non-empty list")
    ids: set[str] = set()
    allowed = {
        "id",
        "title",
        "failure_mode",
        "source_status",
        "example_dir",
        "run_script",
        "feedback_script",
        "report",
        "test",
        "policy_target",
        "course_links",
    }
    for index, example in enumerate(examples):
        context = f"examples[{index}]"
        require(isinstance(example, dict), f"{context}: must be object")
        require_no_extra_keys(example, allowed, context)
        require_pattern(example.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        example_id = example["id"]
        require(example_id not in ids, f"duplicate example id: {example_id}")
        ids.add(example_id)
        require(example_id in manifest_by_id, f"{context}: id missing from course manifest")

        manifest_example = manifest_by_id[example_id]
        for field in [
            "title",
            "failure_mode",
            "source_status",
            "example_dir",
            "run_script",
            "feedback_script",
            "report",
            "test",
        ]:
            require(example.get(field) == manifest_example.get(field), f"{context}: {field} does not match course manifest")

        for field in ["example_dir", "report", "test", "policy_target"]:
            path = ROOT / example[field]
            require(path.exists(), f"{context}: missing {field}: {example[field]}")
        for script in [example["run_script"], example["feedback_script"]]:
            require(script in scripts, f"{context}: package script missing {script}")

        readme_path = ROOT / example["example_dir"] / "README.md"
        require(readme_path.exists(), f"{context}: example README missing")
        readme = readme_path.read_text(encoding="utf-8")
        for token in [example["failure_mode"], example["run_script"], example["feedback_script"], example["report"], example["test"]]:
            require(token in readme, f"{context}: README missing {token}")

        course_links = example.get("course_links")
        require(isinstance(course_links, list) and course_links, f"{context}: course_links must be non-empty")
        for link in course_links:
            require(isinstance(link, str), f"{context}: course link must be string")
            require((ROOT / link).exists(), f"{context}: course link missing: {link}")
            require((ROOT / link).exists(), f"{context}: course link does not exist: {link}")

    require(ids == set(manifest_by_id), "example registry ids must match course manifest ids")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    manifest = load_json(COURSE_MANIFEST_PATH)
    check_schema(schema)
    check_registry(registry, manifest)
    print(f"checked example registry with {len(registry['examples'])} examples")


if __name__ == "__main__":
    main()
