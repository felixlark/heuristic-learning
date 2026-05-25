#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/checkpoint-registry.json"
SCHEMA_PATH = ROOT / "docs/public/checkpoint-registry.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/checkpoints.md"
EXPECTED_IDS = {"cp-0", "cp-1", "cp-2", "cp-3", "cp-4", "cp-5"}


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
    require(schema.get("title") == "Heuristic Learning Checkpoint Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "checkpoints"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/checkpoint-registry.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    units = load_json(ROOT / "docs/public/learning-units.json")
    outcomes = load_json(ROOT / "docs/public/learning-outcomes.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    syllabus = (ROOT / "docs/zh-cn/syllabus/index.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    unit_ids = {unit.get("id") for unit in units.get("units", []) if isinstance(unit, dict)}
    outcome_ids = {outcome.get("id") for outcome in outcomes.get("outcomes", []) if isinstance(outcome, dict)}

    checkpoints = registry.get("checkpoints")
    require(isinstance(checkpoints, list) and checkpoints, "checkpoints must be non-empty")
    ids: set[str] = set()
    covered_units: set[str] = set()
    covered_outcomes: set[str] = set()
    for index, checkpoint in enumerate(checkpoints):
        context = f"checkpoints[{index}]"
        require(isinstance(checkpoint, dict), f"{context}: must be object")
        require(
            set(checkpoint)
            == {
                "id",
                "title",
                "learning_unit_id",
                "learning_outcome_ids",
                "prompt",
                "evidence",
                "verification_commands",
                "pass_condition",
                "common_failure",
            },
            f"{context}: unexpected keys",
        )
        checkpoint_id = checkpoint.get("id")
        require(isinstance(checkpoint_id, str), f"{context}: id must be string")
        require(checkpoint_id not in ids, f"duplicate checkpoint id: {checkpoint_id}")
        ids.add(checkpoint_id)
        title = checkpoint.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        unit_id = checkpoint.get("learning_unit_id")
        require(unit_id in unit_ids, f"{context}: unknown learning unit {unit_id}")
        covered_units.add(unit_id)
        for outcome_id in checkpoint.get("learning_outcome_ids", []):
            require(outcome_id in outcome_ids, f"{context}: unknown learning outcome {outcome_id}")
            covered_outcomes.add(outcome_id)
        prompt = checkpoint.get("prompt")
        require(isinstance(prompt, str) and prompt, f"{context}: prompt must be non-empty")
        for evidence in checkpoint.get("evidence", []):
            require(isinstance(evidence, str) and path_exists(evidence), f"{context}: evidence missing: {evidence}")
        for command in checkpoint.get("verification_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command in audit, f"{context}: command not documented: {command}")
        require(isinstance(checkpoint.get("pass_condition"), str) and checkpoint["pass_condition"], f"{context}: pass_condition missing")
        require(isinstance(checkpoint.get("common_failure"), str) and checkpoint["common_failure"], f"{context}: common_failure missing")

    require(ids == EXPECTED_IDS, f"checkpoint ids mismatch: {sorted(ids)}")
    require(covered_units == unit_ids, "checkpoints must cover all learning units")
    require({"lo-1", "lo-2", "lo-3", "lo-4", "lo-5"}.issubset(covered_outcomes), "checkpoints must cover all learning outcomes")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("checkpoint-registry" in resource_ids, "course manifest missing checkpoint registry")
    require("checkpoint-registry-schema" in resource_ids, "course manifest missing checkpoint schema")
    for required in [
        "/checkpoint-registry.json",
        "/checkpoint-registry.schema.json",
        "npm run checkpoints:check",
    ]:
        require(required in page, f"checkpoint page missing {required}")
    for required in [
        "阶段检查点",
        "checkpoint-registry.json",
        "npm run checkpoints:check",
    ]:
        require(
            required in appendix or required in syllabus or required in audit or required in llms or required in public_llms,
            f"checkpoint registry not linked: {required}",
        )


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked checkpoint registry with {len(registry['checkpoints'])} checkpoints")


if __name__ == "__main__":
    main()
