#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/case-registry.json"
SCHEMA_PATH = ROOT / "docs/public/case-registry.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/case-registry.md"
EXPECTED_CASE_IDS = {
    "ant-gait",
    "breakout",
    "vizdoom",
    "robot-soccer",
    "traffic-simulation",
    "x-signal",
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
    require(schema.get("title") == "Heuristic Learning Case Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "cases"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "case" in defs, "schema must define case")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/case-registry.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    case_index = (ROOT / "docs/zh-cn/cases/index.md").read_text(encoding="utf-8")
    source_registry = (ROOT / "docs/zh-cn/appendix/source-registry.md").read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    outcomes = load_json(ROOT / "docs/public/learning-outcomes.json")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    example_by_id = {
        example.get("id"): example
        for example in examples.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    outcome_ids = {
        outcome.get("id")
        for outcome in outcomes.get("outcomes", [])
        if isinstance(outcome, dict) and isinstance(outcome.get("id"), str)
    }

    cases = registry.get("cases")
    require(isinstance(cases, list) and cases, "cases must be a non-empty list")
    ids: set[str] = set()
    statuses: set[str] = set()
    source_kinds: set[str] = set()
    runnable_count = 0
    allowed_keys = {
        "id",
        "title",
        "case_page",
        "source_status",
        "source_kind",
        "source_refs",
        "example_id",
        "failure_mode",
        "learning_outcome_ids",
        "course_use",
        "verification_commands",
        "boundary",
    }
    for index, case in enumerate(cases):
        context = f"cases[{index}]"
        require(isinstance(case, dict), f"{context}: must be object")
        require(set(case) == allowed_keys, f"{context}: unexpected keys")
        case_id = case.get("id")
        require(isinstance(case_id, str) and re.match(r"^[a-z0-9-]+$", case_id), f"{context}: invalid id")
        require(case_id not in ids, f"duplicate case id: {case_id}")
        ids.add(case_id)

        title = case.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        case_page = case.get("case_page")
        require(isinstance(case_page, str) and (ROOT / case_page).exists(), f"{context}: case page missing")
        case_text = (ROOT / case_page).read_text(encoding="utf-8")
        require(case_text.startswith("---\n"), f"{context}: case page missing frontmatter")

        status = case.get("source_status")
        require(isinstance(status, str) and status in source_registry, f"{context}: source status not documented")
        statuses.add(status)
        source_kind = case.get("source_kind")
        require(source_kind in {"public-artifact", "internal-signal", "x-signal"}, f"{context}: invalid source_kind")
        source_kinds.add(source_kind)
        refs = case.get("source_refs")
        require(isinstance(refs, list) and refs, f"{context}: source_refs must be non-empty")
        for ref in refs:
            require(isinstance(ref, str) and ref, f"{context}: source ref must be string")
            if ref.startswith(("docs/", "examples/", "experiments/", "templates/")):
                require((ROOT / ref).exists(), f"{context}: source ref missing: {ref}")
            else:
                require(ref in source_registry or ref in case_text, f"{context}: source ref not documented: {ref}")

        example_id = case.get("example_id")
        failure_mode = case.get("failure_mode")
        if example_id is None:
            require(failure_mode is None, f"{context}: failure_mode must be null when example_id is null")
        else:
            require(example_id in example_by_id, f"{context}: unknown example id {example_id}")
            runnable_count += 1
            example = example_by_id[example_id]
            require(failure_mode == example.get("failure_mode"), f"{context}: failure_mode must match example registry")
            require(case_page in example.get("course_links", []), f"{context}: example registry must link case page")

        linked_outcomes = case.get("learning_outcome_ids")
        require(isinstance(linked_outcomes, list) and linked_outcomes, f"{context}: outcomes must be non-empty")
        for outcome_id in linked_outcomes:
            require(outcome_id in outcome_ids, f"{context}: unknown learning outcome {outcome_id}")

        course_use = case.get("course_use")
        require(isinstance(course_use, str) and course_use, f"{context}: course_use must be non-empty")
        commands = case.get("verification_commands")
        require(isinstance(commands, list) and commands, f"{context}: verification_commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command in case_text or command in source_registry, f"{context}: command not documented: {command}")
        boundary = case.get("boundary")
        require(isinstance(boundary, str) and boundary in page or isinstance(boundary, str) and boundary in case_text, f"{context}: boundary not documented")

    require(ids == EXPECTED_CASE_IDS, f"case ids mismatch: {sorted(ids)}")
    require(runnable_count == 5, "case registry must bind five runnable domain cases")
    require({"public-artifact", "internal-signal", "x-signal"} == source_kinds, "case registry must cover all source kinds")
    require("已结构化" in statuses, "case registry must preserve structured non-runnable case")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("case-registry" in resource_ids, "course manifest missing case-registry resource")
    require("case-registry-schema" in resource_ids, "course manifest missing case-registry schema resource")
    for required in [
        "/case-registry.json",
        "/case-registry.schema.json",
        "npm run cases:check",
    ]:
        require(required in page, f"case registry page missing {required}")
    for required in [
        "案例矩阵",
        "case-registry.json",
    ]:
        require(required in page or required in case_index or required in llms or required in public_llms, f"case registry not linked: {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked case registry with {len(registry['cases'])} cases")


if __name__ == "__main__":
    main()
