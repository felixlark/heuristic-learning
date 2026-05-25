#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/completion-audit.json"
SCHEMA_PATH = ROOT / "docs/public/completion-audit.schema.json"
EXPECTED_REQUIREMENTS = {
    "chinese-course-entry",
    "theory-foundation",
    "runnable-examples",
    "case-library",
    "teaching-materials",
    "machine-readable-entrypoints",
    "contribution-and-release-governance",
    "source-and-security-boundaries",
    "documentation-build",
    "browser-visual-acceptance",
    "reproducibility",
}
EXPECTED_BOUNDARIES = {
    "jiayi-source-status",
    "x-fieldtheory-status",
    "feishu-sanitization",
    "lightweight-replay-boundary",
    "http-route-boundary",
    "browser-visual-boundary",
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
    require(schema.get("title") == "Heuristic Learning Completion Audit Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    required = schema.get("required")
    require(isinstance(required, list), "schema required keys must be a list")
    for field in ["schema_version", "objective", "requirements", "required_commands", "evidence_boundaries", "final_checks"]:
        require(field in required, f"schema missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/completion-audit.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(
        registry,
        {"$schema", "schema_version", "objective", "requirements", "required_commands", "evidence_boundaries", "final_checks"},
        "registry",
    )
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require("EasyVibe" in registry.get("objective", ""), "objective must preserve EasyVibe target")

    page = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    requirements = registry.get("requirements")
    require(isinstance(requirements, list), "requirements must be a list")
    requirement_ids: set[str] = set()
    allowed_requirement_keys = {"id", "title", "evidence", "verification"}
    for index, item in enumerate(requirements):
        context = f"requirements[{index}]"
        require(isinstance(item, dict), f"{context}: must be object")
        require_no_extra_keys(item, allowed_requirement_keys, context)
        requirement_id = item.get("id")
        require(isinstance(requirement_id, str), f"{context}: id must be string")
        requirement_ids.add(requirement_id)
        title = item.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        evidence = item.get("evidence")
        require(isinstance(evidence, list) and evidence, f"{context}: evidence must be non-empty")
        for evidence_path in evidence:
            require(isinstance(evidence_path, str), f"{context}: evidence must be string")
            if evidence_path.endswith("/"):
                require((ROOT / evidence_path).is_dir(), f"{context}: evidence dir missing: {evidence_path}")
            else:
                require((ROOT / evidence_path).exists(), f"{context}: evidence path missing: {evidence_path}")
        verification = item.get("verification")
        require(isinstance(verification, list) and verification, f"{context}: verification must be non-empty")
        for command in verification:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")

    require(requirement_ids == EXPECTED_REQUIREMENTS, f"completion requirements mismatch: {sorted(requirement_ids)}")

    required_commands = registry.get("required_commands")
    require(isinstance(required_commands, list), "required_commands must be a list")
    require("npm run release:readiness:check" in required_commands, "required_commands must include release readiness gate")
    verify = (ROOT / "scripts/verify.sh").read_text(encoding="utf-8")
    for command in required_commands:
        require(isinstance(command, str), "required command must be string")
        if command.startswith("npm run "):
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"package script missing for required command {command}")
            require(command in page or command in verify, f"required command not documented: {command}")
        else:
            require(command in page or command in verify, f"required shell command not documented: {command}")

    boundaries = registry.get("evidence_boundaries")
    require(isinstance(boundaries, list), "evidence_boundaries must be a list")
    boundary_ids: set[str] = set()
    for index, boundary in enumerate(boundaries):
        context = f"evidence_boundaries[{index}]"
        require(isinstance(boundary, dict), f"{context}: must be object")
        require_no_extra_keys(boundary, {"id", "topic", "boundary"}, context)
        boundary_id = boundary.get("id")
        boundary_ids.add(boundary_id)
        topic = boundary.get("topic")
        text = boundary.get("boundary")
        require(isinstance(topic, str) and topic in page, f"{context}: topic not documented")
        require(isinstance(text, str) and text in page, f"{context}: boundary not documented")
    require(boundary_ids == EXPECTED_BOUNDARIES, f"boundary ids mismatch: {sorted(boundary_ids)}")

    final_checks = registry.get("final_checks")
    require(isinstance(final_checks, list) and len(final_checks) == 9, "final_checks must list 9 checks")
    for check in final_checks:
        require(isinstance(check, str), "final check must be string")
    visual_final_checks = [
        check
        for check in final_checks
        if isinstance(check, str) and "visual-verification.json" in check and "visual-acceptance-log.json" in check
    ]
    require(visual_final_checks, "final_checks must include visual verification and acceptance log status rule")
    visual_rule = visual_final_checks[0]
    for required_term in ["required-before-release", "not-run", "blocked", "原因"]:
        require(required_term in visual_rule, f"visual final check must mention {required_term}")
    release_readiness_checks = [
        check
        for check in final_checks
        if isinstance(check, str) and "npm run release:readiness:check" in check
    ]
    require(release_readiness_checks, "final_checks must include release readiness gate")
    release_rule = release_readiness_checks[0]
    for required_term in ["官方 Browser/IAB", "blocked", "公开发布就绪"]:
        require(required_term in release_rule, f"release readiness final check must mention {required_term}")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("completion-audit" in resource_ids, "course manifest missing completion-audit resource")
    require("completion-audit-schema" in resource_ids, "course manifest missing completion-audit schema resource")
    require("visual-verification" in resource_ids, "course manifest missing visual-verification resource")
    require("visual-verification-schema" in resource_ids, "course manifest missing visual-verification schema resource")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked completion audit with {len(registry['requirements'])} requirements")


if __name__ == "__main__":
    main()
