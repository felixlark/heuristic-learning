#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/research-projects.json"
SCHEMA_PATH = ROOT / "docs/public/research-projects.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/research-projects.md"
EXPECTED_PROJECT_IDS = {
    "gridworld-new-probe",
    "robot-soccer-lane-check",
    "traffic-grid-safety-constraint",
    "breakout-reflection-prediction",
    "vizdoom-medikit-staging",
    "ant-gait-stability",
    "feedback-format-comparison",
    "anti-forgetting-test-set",
}
EXPECTED_EXAMPLE_IDS = {
    "gridworld",
    "robot-soccer",
    "vizdoom-replay",
    "traffic-grid",
    "breakout-replay",
    "ant-gait-replay",
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
    require(schema.get("title") == "Heuristic Learning Research Projects Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    required = schema.get("required")
    require(isinstance(required, list), "schema required keys must be a list")
    require(required == ["schema_version", "projects"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "project" in defs, "schema must define project")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/research-projects.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "projects"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    page = PAGE_PATH.read_text(encoding="utf-8")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    example_registry = load_json(ROOT / "docs/public/example-registry.json")
    example_ids = {
        example.get("id")
        for example in example_registry.get("examples", [])
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    require(example_ids == EXPECTED_EXAMPLE_IDS, "example registry ids changed")

    projects = registry.get("projects")
    require(isinstance(projects, list) and projects, "projects must be a non-empty list")
    project_ids: set[str] = set()
    categories: set[str] = set()
    all_examples: set[str] = set()
    allowed = {
        "id",
        "category",
        "title",
        "source",
        "research_question",
        "failure_mode",
        "examples",
        "deliverables",
        "verification",
        "course_outputs",
    }
    for index, project in enumerate(projects):
        context = f"projects[{index}]"
        require(isinstance(project, dict), f"{context}: must be object")
        require_no_extra_keys(project, allowed, context)
        project_id = project.get("id")
        require(isinstance(project_id, str) and project_id, f"{context}: id must be string")
        require(project_id not in project_ids, f"duplicate project id: {project_id}")
        project_ids.add(project_id)

        title = project.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        category = project.get("category")
        require(category in {"intro", "public-artifact", "research"}, f"{context}: invalid category")
        categories.add(category)

        source = project.get("source")
        require(isinstance(source, str) and source, f"{context}: source must be non-empty")
        if source.startswith(("docs/", "examples/", "experiments/", "tests/", "templates/")):
            require((ROOT / source).exists(), f"{context}: source missing: {source}")

        question = project.get("research_question")
        require(isinstance(question, str) and question in page, f"{context}: research question not documented")
        failure_mode = project.get("failure_mode")
        require(isinstance(failure_mode, str) and failure_mode, f"{context}: failure_mode must be non-empty")

        examples = project.get("examples")
        require(isinstance(examples, list) and examples, f"{context}: examples must be non-empty")
        for example in examples:
            require(example in example_ids, f"{context}: unknown example id: {example}")
            all_examples.add(example)

        deliverables = project.get("deliverables")
        require(isinstance(deliverables, list) and deliverables, f"{context}: deliverables must be non-empty")
        verification = project.get("verification")
        require(isinstance(verification, list) and verification, f"{context}: verification must be non-empty")
        for command in verification:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page or command == "npm run verify", f"{context}: command not documented: {command}")

        outputs = project.get("course_outputs")
        require(isinstance(outputs, list) and outputs, f"{context}: course_outputs must be non-empty")
        for output in outputs:
            require(isinstance(output, str) and output, f"{context}: output must be string")
            if output.startswith(("docs/", "templates/")):
                require((ROOT / output).exists(), f"{context}: course output missing: {output}")

    require(project_ids == EXPECTED_PROJECT_IDS, f"research project ids mismatch: {sorted(project_ids)}")
    require(categories == {"intro", "public-artifact", "research"}, "project categories must cover intro, public-artifact, and research")
    require(all_examples == EXPECTED_EXAMPLE_IDS, "research projects must cover all runnable examples")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("research-projects" in resource_ids, "course manifest missing research-projects resource")
    require("research-projects-schema" in resource_ids, "course manifest missing research-projects schema resource")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked research projects with {len(registry['projects'])} projects")


if __name__ == "__main__":
    main()
