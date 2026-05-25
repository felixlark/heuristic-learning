#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/concept-graph.json"
SCHEMA_PATH = ROOT / "docs/public/concept-graph.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/concept-graph.md"
EXPECTED_CONCEPT_IDS = {
    "heuristic-learning",
    "signal",
    "probe",
    "baseline",
    "heuristic-patch",
    "feedback-report",
    "regression",
    "source-status",
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
    require(schema.get("title") == "Heuristic Learning Concept Graph", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "concepts"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "concept" in defs, "schema must define concept")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/concept-graph.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "concepts"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    glossary = (ROOT / "docs/zh-cn/appendix/glossary.md").read_text(encoding="utf-8")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    claims = load_json(ROOT / "docs/public/claims-registry.json")
    claim_ids = {
        claim.get("id")
        for claim in claims.get("claims", [])
        if isinstance(claim, dict) and isinstance(claim.get("id"), str)
    }
    examples = load_json(ROOT / "docs/public/example-registry.json")
    example_ids = {
        example.get("id")
        for example in examples.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    teaching = load_json(ROOT / "docs/public/teaching-registry.json")
    material_ids = {
        material.get("id")
        for material in teaching.get("materials", [])
        if isinstance(material, dict) and isinstance(material.get("id"), str)
    }
    manifest = load_json(ROOT / "docs/public/course-manifest.json")

    concepts = registry.get("concepts")
    require(isinstance(concepts, list) and concepts, "concepts must be a non-empty list")
    concept_ids: set[str] = set()
    covered_examples: set[str] = set()
    covered_claims: set[str] = set()
    allowed = {
        "id",
        "term",
        "definition",
        "claim_ids",
        "example_ids",
        "material_ids",
        "pages",
        "commands",
    }
    for index, concept in enumerate(concepts):
        context = f"concepts[{index}]"
        require(isinstance(concept, dict), f"{context}: must be object")
        require_no_extra_keys(concept, allowed, context)
        concept_id = concept.get("id")
        require(isinstance(concept_id, str) and concept_id, f"{context}: id must be string")
        require(concept_id not in concept_ids, f"duplicate concept id: {concept_id}")
        concept_ids.add(concept_id)

        term = concept.get("term")
        require(isinstance(term, str) and term in page, f"{context}: term not documented on concept page")
        require(term in glossary, f"{context}: term not documented in glossary")
        definition = concept.get("definition")
        require(isinstance(definition, str) and definition, f"{context}: definition must be non-empty")

        for key, known, covered in [
            ("claim_ids", claim_ids, covered_claims),
            ("example_ids", example_ids, covered_examples),
            ("material_ids", material_ids, set()),
        ]:
            values = concept.get(key)
            require(isinstance(values, list) and values, f"{context}: {key} must be non-empty")
            for value in values:
                require(value in known, f"{context}: unknown {key} value: {value}")
                covered.add(value)

        pages = concept.get("pages")
        require(isinstance(pages, list) and pages, f"{context}: pages must be non-empty")
        for path in pages:
            require(isinstance(path, str), f"{context}: page path must be string")
            require((ROOT / path).exists(), f"{context}: page path missing: {path}")

        commands = concept.get("commands")
        require(isinstance(commands, list) and commands, f"{context}: commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page, f"{context}: command not documented on concept page: {command}")

    require(concept_ids == EXPECTED_CONCEPT_IDS, f"concept ids mismatch: {sorted(concept_ids)}")
    require(covered_examples == example_ids, "concept graph must cover every runnable example")
    require(covered_claims == claim_ids, "concept graph must cover every research claim")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("concept-graph" in resource_ids, "course manifest missing concept-graph resource")
    require("concept-graph-schema" in resource_ids, "course manifest missing concept-graph schema resource")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked concept graph with {len(registry['concepts'])} concepts")


if __name__ == "__main__":
    main()
