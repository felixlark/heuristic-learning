#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/public/course-manifest.json"
SCHEMA_PATH = ROOT / "docs/public/course-manifest.schema.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing JSON file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"JSON root must be object: {path.relative_to(ROOT)}")
    return data


def require_keys(data: dict[str, Any], required: list[str], context: str) -> None:
    for key in required:
        require(key in data, f"{context}: missing required key {key}")


def require_no_extra_keys(data: dict[str, Any], allowed: set[str], context: str) -> None:
    extra = set(data) - allowed
    require(not extra, f"{context}: unexpected keys {sorted(extra)}")


def require_pattern(value: Any, pattern: str, context: str) -> None:
    require(isinstance(value, str), f"{context}: expected string")
    require(re.match(pattern, value), f"{context}: does not match {pattern}: {value}")


def check_schema_shape(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Course Manifest", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(
        schema.get("required") == ["schema_version", "course", "core_pages", "examples", "public_resources", "ci"],
        "schema required keys drifted",
    )
    defs = schema.get("$defs")
    require(isinstance(defs, dict), "schema must define $defs")
    require("page" in defs and "example" in defs and "public_resource" in defs, "schema must define page, example, and public_resource")
    example_required = defs["example"].get("required")
    require(isinstance(example_required, list), "schema example required must be a list")
    for field in ["id", "title", "source_status", "failure_mode", "example_dir", "run_script", "feedback_script", "report", "test", "readme"]:
        require(field in example_required, f"schema example missing required field {field}")
    resource_required = defs["public_resource"].get("required")
    require(isinstance(resource_required, list), "schema public_resource required must be a list")
    for field in ["id", "title", "path", "route", "type", "check_script"]:
        require(field in resource_required, f"schema public_resource missing required field {field}")


def check_manifest_shape(manifest: dict[str, Any]) -> None:
    require(manifest.get("$schema") == "/course-manifest.schema.json", "manifest schema pointer mismatch")
    require_keys(manifest, ["$schema", "schema_version", "course", "core_pages", "examples", "public_resources", "ci"], "manifest")
    require_no_extra_keys(manifest, {"$schema", "schema_version", "course", "core_pages", "examples", "public_resources", "ci"}, "manifest")
    require(manifest["schema_version"] == 1, "manifest schema_version must be 1")

    course = manifest["course"]
    require(isinstance(course, dict), "course must be an object")
    require_no_extra_keys(course, {"name", "language", "verification_command", "structure_check_command"}, "course")
    require(course.get("name") == "Heuristic Learning", "course name mismatch")
    require(course.get("language") == "zh-CN", "course language mismatch")
    require(course.get("verification_command") == "npm run verify", "course verification command mismatch")
    require(course.get("structure_check_command") == "npm run course:structure:check", "course structure command mismatch")

    ci = manifest["ci"]
    require(isinstance(ci, dict), "ci must be an object")
    require_no_extra_keys(ci, {"verify_workflow", "deploy_workflow", "required_command"}, "ci")
    require((ROOT / ci["verify_workflow"]).exists(), "ci verify workflow path missing")
    require((ROOT / ci["deploy_workflow"]).exists(), "ci deploy workflow path missing")
    require(ci["required_command"] == "npm run verify", "ci required command mismatch")


def check_pages(manifest: dict[str, Any]) -> None:
    pages = manifest["core_pages"]
    require(isinstance(pages, list) and pages, "core_pages must be a non-empty list")
    ids: set[str] = set()
    routes: set[str] = set()
    for index, page in enumerate(pages):
        context = f"core_pages[{index}]"
        require(isinstance(page, dict), f"{context}: must be object")
        require_no_extra_keys(page, {"id", "title", "path", "route"}, context)
        require_pattern(page.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        require(isinstance(page.get("title"), str) and page["title"], f"{context}.title must be non-empty")
        require_pattern(page.get("path"), r"^docs/zh-cn/.+\.md$", f"{context}.path")
        require_pattern(page.get("route"), r"^/zh-cn/.+", f"{context}.route")
        require(page["id"] not in ids, f"duplicate page id: {page['id']}")
        require(page["route"] not in routes, f"duplicate page route: {page['route']}")
        ids.add(page["id"])
        routes.add(page["route"])
        path = ROOT / page["path"]
        require(path.exists(), f"{context}: page path missing: {page['path']}")
        text = path.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"{context}: page missing frontmatter")


def check_examples(manifest: dict[str, Any]) -> None:
    examples = manifest["examples"]
    require(isinstance(examples, list) and examples, "examples must be a non-empty list")
    ids: set[str] = set()
    allowed_statuses = {
        "teaching-minimal",
        "reproduced-lightweight-artifact",
        "reproduced-minimal-internal-signal",
    }
    for index, example in enumerate(examples):
        context = f"examples[{index}]"
        require(isinstance(example, dict), f"{context}: must be object")
        require_no_extra_keys(
            example,
            {"id", "title", "source_status", "failure_mode", "example_dir", "run_script", "feedback_script", "report", "test", "readme"},
            context,
        )
        require_pattern(example.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        require(example["id"] not in ids, f"duplicate example id: {example['id']}")
        ids.add(example["id"])
        require(example.get("source_status") in allowed_statuses, f"{context}: unknown source_status")
        require_pattern(example.get("example_dir"), r"^examples/.+", f"{context}.example_dir")
        require_pattern(example.get("run_script"), r"^examples:[a-z0-9-]+$", f"{context}.run_script")
        require_pattern(example.get("feedback_script"), r"^examples:[a-z0-9-]+:feedback$", f"{context}.feedback_script")
        require_pattern(example.get("report"), r"^experiments/.+/latest\.json$", f"{context}.report")
        require_pattern(example.get("test"), r"^tests/test_.+\.py$", f"{context}.test")
        require_pattern(example.get("readme"), r"^examples/.+/README\.md$", f"{context}.readme")
        for path_key in ["example_dir", "report", "test", "readme"]:
            path = ROOT / example[path_key]
            require(path.exists(), f"{context}: {path_key} path missing: {example[path_key]}")


def check_public_resources(manifest: dict[str, Any]) -> None:
    resources = manifest["public_resources"]
    require(isinstance(resources, list) and resources, "public_resources must be a non-empty list")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    ids: set[str] = set()
    routes: set[str] = set()
    paths: set[str] = set()
    allowed_types = {"registry", "schema", "llm-entrypoint"}
    expected_ids = {
        "course-manifest",
        "course-manifest-schema",
        "example-registry",
        "example-registry-schema",
        "code-tour",
        "code-tour-schema",
        "benchmark-summary",
        "benchmark-summary-schema",
        "ablation-plan",
        "ablation-plan-schema",
        "artifact-gap-analysis",
        "artifact-gap-analysis-schema",
        "troubleshooting-tree",
        "troubleshooting-tree-schema",
        "claims-registry",
        "claims-registry-schema",
        "case-registry",
        "case-registry-schema",
        "rubric",
        "rubric-schema",
        "exercise-registry",
        "exercise-registry-schema",
        "contribution-contract",
        "contribution-contract-schema",
        "reproducibility-checklist",
        "reproducibility-checklist-schema",
        "learning-units",
        "learning-units-schema",
        "learning-outcomes",
        "learning-outcomes-schema",
        "checkpoint-registry",
        "checkpoint-registry-schema",
        "evaluation-metrics",
        "evaluation-metrics-schema",
        "paper-blueprint",
        "paper-blueprint-schema",
        "concept-graph",
        "concept-graph-schema",
        "teaching-pack",
        "teaching-pack-schema",
        "research-projects",
        "research-projects-schema",
        "research-logbook",
        "research-logbook-schema",
        "completion-audit",
        "completion-audit-schema",
        "visual-verification",
        "visual-verification-schema",
        "visual-acceptance-log",
        "visual-acceptance-log-schema",
        "x-sources",
        "x-sources-schema",
        "source-to-case-playbook",
        "source-to-case-playbook-schema",
        "experiment-report-schema",
        "llms",
    }
    for index, resource in enumerate(resources):
        context = f"public_resources[{index}]"
        require(isinstance(resource, dict), f"{context}: must be object")
        require_no_extra_keys(resource, {"id", "title", "path", "route", "type", "check_script"}, context)
        require_pattern(resource.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        require(isinstance(resource.get("title"), str) and resource["title"], f"{context}.title must be non-empty")
        require_pattern(resource.get("path"), r"^docs/public/.+", f"{context}.path")
        require_pattern(resource.get("route"), r"^/.+", f"{context}.route")
        require(resource.get("type") in allowed_types, f"{context}: invalid type")
        require(resource["id"] not in ids, f"duplicate public resource id: {resource['id']}")
        require(resource["route"] not in routes, f"duplicate public resource route: {resource['route']}")
        require(resource["path"] not in paths, f"duplicate public resource path: {resource['path']}")
        ids.add(resource["id"])
        routes.add(resource["route"])
        paths.add(resource["path"])
        require((ROOT / resource["path"]).exists(), f"{context}: public resource path missing: {resource['path']}")
        command = resource.get("check_script")
        require(isinstance(command, str) and command.startswith("npm run "), f"{context}: check_script must be npm script")
        script = command.removeprefix("npm run ").split()[0]
        require(script in scripts, f"{context}: package script missing for check_script {command}")

    require(ids == expected_ids, f"public resource ids mismatch: {sorted(ids)}")
    for registry_id in [
        "course-manifest",
        "example-registry",
        "code-tour",
        "benchmark-summary",
        "ablation-plan",
        "artifact-gap-analysis",
        "troubleshooting-tree",
        "claims-registry",
        "case-registry",
        "rubric",
        "exercise-registry",
        "contribution-contract",
        "reproducibility-checklist",
        "learning-units",
        "learning-outcomes",
        "checkpoint-registry",
        "evaluation-metrics",
        "paper-blueprint",
        "concept-graph",
        "teaching-pack",
        "research-projects",
        "research-logbook",
        "completion-audit",
        "visual-verification",
        "visual-acceptance-log",
        "x-sources",
        "source-to-case-playbook",
    ]:
        schema_id = f"{registry_id}-schema"
        if schema_id in expected_ids:
            require(schema_id in ids, f"missing schema resource for {registry_id}")


def main() -> None:
    manifest = load_json(MANIFEST_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema_shape(schema)
    check_manifest_shape(manifest)
    check_pages(manifest)
    check_examples(manifest)
    check_public_resources(manifest)
    print(
        "checked manifest with "
        f"{len(manifest['core_pages'])} pages, "
        f"{len(manifest['examples'])} examples, and "
        f"{len(manifest['public_resources'])} public resources"
    )


if __name__ == "__main__":
    main()
