#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/source-to-case-playbook.json"
SCHEMA_PATH = ROOT / "docs/public/source-to-case-playbook.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/source-to-case-playbook.md"

EXPECTED_IDS = {
    "x-thread-to-case-card",
    "public-artifact-to-replay",
    "internal-signal-to-minimal-env",
    "hypothesis-to-research-project",
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
    require(schema.get("title") == "Heuristic Learning Source-to-Case Playbook", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "scope", "workflows"], "schema required keys drifted")


def command_known(command: str, scripts: dict[str, Any]) -> bool:
    if not command.startswith("npm run "):
        return False
    script = command.removeprefix("npm run ").split()[0]
    return script in scripts


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/source-to-case-playbook.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require(registry.get("scope") == "turning-source-signals-into-course-cases", "registry scope mismatch")

    page = PAGE_PATH.read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    x_sources = load_json(ROOT / "docs/public/x-sources.json")
    contribution_contract = load_json(ROOT / "docs/public/contribution-contract.json")
    exercise_registry = load_json(ROOT / "docs/public/exercise-registry.json")

    workflows = registry.get("workflows")
    require(isinstance(workflows, list) and workflows, "workflows must be a non-empty list")
    ids: set[str] = set()
    required_keys = {
        "id",
        "signal_type",
        "source_checks",
        "required_artifacts",
        "status_gate",
        "verification_commands",
        "course_landing",
        "forbidden_claims",
    }
    for index, workflow in enumerate(workflows):
        context = f"workflows[{index}]"
        require(isinstance(workflow, dict), f"{context}: must be object")
        require(set(workflow) == required_keys, f"{context}: unexpected keys")
        workflow_id = workflow.get("id")
        require(isinstance(workflow_id, str), f"{context}: id must be string")
        ids.add(workflow_id)
        signal_type = workflow.get("signal_type")
        require(isinstance(signal_type, str) and signal_type in page, f"{context}: signal type not documented")
        for field in ["source_checks", "required_artifacts", "forbidden_claims"]:
            values = workflow.get(field)
            require(isinstance(values, list) and values, f"{context}: {field} must be non-empty")
            for value in values:
                require(isinstance(value, str) and value, f"{context}: {field} item must be non-empty")
        for artifact in workflow.get("required_artifacts", []):
            if artifact.startswith(("docs/", "templates/", "examples/", "SECURITY.md")):
                require((ROOT / artifact).exists(), f"{context}: required artifact missing: {artifact}")
        gate = workflow.get("status_gate")
        require(isinstance(gate, str) and gate, f"{context}: status_gate must be non-empty")
        commands = workflow.get("verification_commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command_known(command, scripts), f"{context}: unknown command {command}")
            require(command in page or command in json.dumps(x_sources, ensure_ascii=False), f"{context}: command not documented {command}")
        landings = workflow.get("course_landing")
        require(isinstance(landings, list) and landings, f"{context}: course_landing must be non-empty")
        for landing in landings:
            require(isinstance(landing, str) and (ROOT / landing).exists(), f"{context}: landing page missing: {landing}")

    require(ids == EXPECTED_IDS, f"source-to-case workflow ids mismatch: {sorted(ids)}")

    page_ids = {item.get("id") for item in manifest.get("core_pages", []) if isinstance(item, dict)}
    resource_ids = {item.get("id") for item in manifest.get("public_resources", []) if isinstance(item, dict)}
    require("source-to-case-playbook" in page_ids, "course manifest missing source-to-case page")
    require("source-to-case-playbook" in resource_ids, "course manifest missing source-to-case registry")
    require("source-to-case-playbook-schema" in resource_ids, "course manifest missing source-to-case schema")
    require("case-card" in json.dumps(contribution_contract, ensure_ascii=False), "contribution contract must keep case-card path")
    require("D1" in json.dumps(exercise_registry, ensure_ascii=False), "exercise registry must keep X case card exercise")
    for required in [
        "/source-to-case-playbook.json",
        "/source-to-case-playbook.schema.json",
        "npm run source:case:check",
        "templates/case-card.md",
        "templates/reproduction-note.md",
        "待直接复核",
    ]:
        require(required in page, f"source-to-case page missing {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked source-to-case playbook with {len(registry['workflows'])} workflows")


if __name__ == "__main__":
    main()
