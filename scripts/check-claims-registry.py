#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/claims-registry.json"
SCHEMA_PATH = ROOT / "docs/public/claims-registry.schema.json"
EXAMPLE_REGISTRY_PATH = ROOT / "docs/public/example-registry.json"

EXPECTED_IDS = {
    "software-structure-learning",
    "feedback-report-as-agent-input",
    "failure-modes-over-average-score",
    "hl-rl-dl-division-of-labor",
    "source-status-is-course-structure",
    "constraint-audit-is-not-general-fact-checking",
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
    require(schema.get("title") == "Heuristic Learning Claims Registry", "schema title mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "claims"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "claim" in defs, "schema must define claim")
    required = defs["claim"].get("required")
    require(isinstance(required, list), "schema claim required must be a list")
    for field in [
        "id",
        "title",
        "status",
        "claim_page",
        "evidence_pages",
        "example_ids",
        "verification_commands",
        "falsification_note",
    ]:
        require(field in required, f"schema claim missing required field {field}")


def check_registry(registry: dict[str, Any], example_registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/claims-registry.schema.json", "claims registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "claims"}, "claims registry")
    require(registry.get("schema_version") == 1, "claims registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    examples = example_registry.get("examples")
    require(isinstance(examples, list), "example registry examples must be a list")
    example_ids = {
        example.get("id")
        for example in examples
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }

    framework = (ROOT / "docs/zh-cn/theory/research-framework.md").read_text(encoding="utf-8")
    claims = registry.get("claims")
    require(isinstance(claims, list) and claims, "claims must be a non-empty list")
    ids: set[str] = set()
    allowed = {
        "id",
        "title",
        "status",
        "claim_page",
        "evidence_pages",
        "example_ids",
        "verification_commands",
        "falsification_note",
    }
    allowed_statuses = {
        "research-hypothesis",
        "working-hypothesis-with-lightweight-evidence",
        "implemented-course-invariant",
    }

    for index, claim in enumerate(claims):
        context = f"claims[{index}]"
        require(isinstance(claim, dict), f"{context}: must be object")
        require_no_extra_keys(claim, allowed, context)
        require_pattern(claim.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        claim_id = claim["id"]
        require(claim_id not in ids, f"duplicate claim id: {claim_id}")
        ids.add(claim_id)
        require(claim.get("status") in allowed_statuses, f"{context}: invalid status")
        require(isinstance(claim.get("title"), str) and claim["title"], f"{context}: missing title")
        require(claim["title"] in framework, f"{context}: title missing from research framework")

        claim_page = claim.get("claim_page")
        require(isinstance(claim_page, str), f"{context}: claim_page must be string")
        require((ROOT / claim_page).exists(), f"{context}: claim page missing: {claim_page}")

        evidence_pages = claim.get("evidence_pages")
        require(isinstance(evidence_pages, list) and evidence_pages, f"{context}: evidence_pages must be non-empty")
        evidence_text = ""
        for page in evidence_pages:
            require(isinstance(page, str), f"{context}: evidence page must be string")
            require((ROOT / page).exists(), f"{context}: evidence page missing: {page}")
            evidence_text += "\n" + (ROOT / page).read_text(encoding="utf-8")

        linked_examples = claim.get("example_ids")
        require(isinstance(linked_examples, list) and linked_examples, f"{context}: example_ids must be non-empty")
        for example_id in linked_examples:
            require(example_id in example_ids, f"{context}: unknown example id: {example_id}")

        commands = claim.get("verification_commands")
        require(isinstance(commands, list) and commands, f"{context}: verification_commands must be non-empty")
        for command in commands:
            require(isinstance(command, str), f"{context}: command must be string")
            require(command.startswith("npm run "), f"{context}: command must be npm script: {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(
                command in framework or command in evidence_text or command in json.dumps(example_registry),
                f"{context}: command not documented: {command}",
            )

        note = claim.get("falsification_note")
        require(isinstance(note, str) and len(note) >= 20, f"{context}: falsification_note too short")

    require(ids == EXPECTED_IDS, f"claims registry ids mismatch: {sorted(ids)}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    example_registry = load_json(EXAMPLE_REGISTRY_PATH)
    check_schema(schema)
    check_registry(registry, example_registry)
    print(f"checked claims registry with {len(registry['claims'])} claims")


if __name__ == "__main__":
    main()
