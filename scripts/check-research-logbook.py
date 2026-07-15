#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/research-logbook.json"
SCHEMA_PATH = ROOT / "docs/public/research-logbook.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/research-logbook.md"
EXPECTED_IDS = {
    "lbg-core-loop-reading",
    "breakout-artifact-reading",
    "x-signal-case-reading",
    "robot-soccer-signal-reading",
    "cross-example-report-reading",
    "constraint-audit-related-work",
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


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Research Logbook", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "entries"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "entry" in defs, "schema must define entry")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/research-logbook.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "entries"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    example_registry = load_json(ROOT / "docs/public/example-registry.json")
    claims_registry = load_json(ROOT / "docs/public/claims-registry.json")
    metrics_registry = load_json(ROOT / "docs/public/evaluation-metrics.json")

    example_ids = {
        example.get("id")
        for example in example_registry.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    claim_ids = {
        claim.get("id")
        for claim in claims_registry.get("claims", [])
        if isinstance(claim, dict) and isinstance(claim.get("id"), str)
    }
    metric_ids = {
        metric.get("id")
        for metric in metrics_registry.get("metrics", [])
        if isinstance(metric, dict) and isinstance(metric.get("id"), str)
    }

    entries = registry.get("entries")
    require(isinstance(entries, list) and entries, "entries must be a non-empty list")
    ids: set[str] = set()
    source_types: set[str] = set()
    covered_examples: set[str] = set()
    covered_claims: set[str] = set()
    covered_metrics: set[str] = set()
    allowed = {
        "id",
        "status",
        "source_type",
        "source_ref",
        "reading_goal",
        "bound_examples",
        "bound_claims",
        "metrics",
        "commands",
        "deliverables",
        "next_action",
        "boundary",
    }
    for index, entry in enumerate(entries):
        context = f"entries[{index}]"
        require(isinstance(entry, dict), f"{context}: must be object")
        require_no_extra_keys(entry, allowed, context)

        entry_id = entry.get("id")
        require(isinstance(entry_id, str) and entry_id, f"{context}: id must be string")
        require(entry_id not in ids, f"duplicate entry id: {entry_id}")
        require(entry_id in page, f"{context}: id not documented")
        ids.add(entry_id)

        status = entry.get("status")
        require(status in {"seeded", "active", "needs-source-refresh"}, f"{context}: invalid status")
        source_type = entry.get("source_type")
        require(
            source_type
            in {
                "public-essay",
                "public-code-artifact",
                "x-source",
                "sanitized-application",
                "cross-example-analysis",
            },
            f"{context}: invalid source_type",
        )
        require(source_type in page, f"{context}: source_type not documented")
        source_types.add(source_type)

        source_ref = entry.get("source_ref")
        require(isinstance(source_ref, str) and source_ref, f"{context}: source_ref must be string")
        if source_ref.startswith(("docs/", "examples/", "experiments/", "templates/")):
            require((ROOT / source_ref).exists(), f"{context}: source_ref path missing: {source_ref}")

        reading_goal = entry.get("reading_goal")
        require(isinstance(reading_goal, str) and reading_goal in page, f"{context}: reading_goal not documented")
        next_action = entry.get("next_action")
        boundary = entry.get("boundary")
        require(isinstance(next_action, str) and next_action, f"{context}: next_action must be string")
        require(isinstance(boundary, str) and boundary, f"{context}: boundary must be string")

        for field, known_ids, covered in [
            ("bound_examples", example_ids, covered_examples),
            ("bound_claims", claim_ids, covered_claims),
            ("metrics", metric_ids, covered_metrics),
        ]:
            values = entry.get(field)
            require(isinstance(values, list) and values, f"{context}: {field} must be non-empty")
            for value in values:
                require(value in known_ids, f"{context}: unknown {field} id: {value}")
                covered.add(value)

        commands = entry.get("commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command == "npm run verify", f"{context}: command not documented: {command}")

        deliverables = entry.get("deliverables")
        require(isinstance(deliverables, list) and deliverables, f"{context}: deliverables must be non-empty")
        for deliverable in deliverables:
            require(isinstance(deliverable, str) and deliverable, f"{context}: deliverable must be string")
            if deliverable.startswith(("docs/", "experiments/", "templates/")):
                require((ROOT / deliverable).exists(), f"{context}: deliverable path missing: {deliverable}")

    require(ids == EXPECTED_IDS, f"research logbook ids mismatch: {sorted(ids)}")
    require(
        source_types
        == {
            "public-essay",
            "public-code-artifact",
            "x-source",
            "sanitized-application",
            "cross-example-analysis",
        },
        "research logbook must cover all source types",
    )
    require(covered_examples == example_ids, "research logbook must cover all runnable examples")
    require(claim_ids.issubset(covered_claims), "research logbook must cover all claims")
    require(metric_ids.issubset(covered_metrics), "research logbook must cover all metrics")

    page_ids = {
        item.get("id")
        for item in manifest.get("core_pages", [])
        if isinstance(item, dict)
    }
    resource_ids = {
        item.get("id")
        for item in manifest.get("public_resources", [])
        if isinstance(item, dict)
    }
    require("research-logbook" in page_ids, "course manifest missing research-logbook page")
    require("research-logbook" in resource_ids, "course manifest missing research-logbook resource")
    require("research-logbook-schema" in resource_ids, "course manifest missing research-logbook schema resource")

    for required in [
        "/research-logbook.json",
        "/research-logbook.schema.json",
        "npm run research:logbook:check",
        "待直接复核",
        "templates/claim-review.md",
        "templates/anti-forgetting-checklist.md",
    ]:
        require(required in page, f"research logbook page missing {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked research logbook with {len(registry['entries'])} entries")


if __name__ == "__main__":
    main()
