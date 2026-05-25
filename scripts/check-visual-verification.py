#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/visual-verification.json"
SCHEMA_PATH = ROOT / "docs/public/visual-verification.schema.json"
LOG_PATH = ROOT / "docs/public/visual-acceptance-log.json"
LOG_SCHEMA_PATH = ROOT / "docs/public/visual-acceptance-log.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/visual-verification.md"
EXPECTED_CHECK_IDS = {
    "home-course-entry",
    "course-map-mobile",
    "examples-run-loop",
    "slide-deck-scan",
    "public-registry-entrypoints",
    "completion-audit-page",
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
    require(schema.get("title") == "Heuristic Learning Visual Verification Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    required = schema.get("required")
    require(isinstance(required, list), "schema required keys must be a list")
    for field in ["schema_version", "scope", "tooling", "checks", "evidence_log"]:
        require(field in required, f"schema missing required field {field}")


def check_log_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "log schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Visual Acceptance Log", "log schema title mismatch")
    require(schema.get("type") == "object", "log schema root type mismatch")
    require(schema.get("additionalProperties") is False, "log schema must disallow additional root properties")
    required = schema.get("required")
    require(isinstance(required, list), "log schema required keys must be a list")
    for field in ["schema_version", "scope", "status", "entries"]:
        require(field in required, f"log schema missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    page = PAGE_PATH.read_text(encoding="utf-8")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    completion = load_json(ROOT / "docs/public/completion-audit.json")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    require(registry.get("$schema") == "/visual-verification.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "scope", "tooling", "checks", "evidence_log"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require(registry.get("scope") == "official-browser-visual-acceptance", "scope mismatch")

    tooling = registry.get("tooling")
    require(isinstance(tooling, dict), "tooling must be an object")
    require_no_extra_keys(tooling, {"primary", "authenticated", "forbidden_substitutes"}, "tooling")
    for required in ["Codex Browser plugin", "in-app browser"]:
        require(required in tooling.get("primary", ""), f"tooling primary missing {required}")
        require(required in page, f"visual page missing tooling term {required}")
    require("Official Chrome plugin" in tooling.get("authenticated", ""), "tooling authenticated surface mismatch")
    forbidden = tooling.get("forbidden_substitutes")
    require(isinstance(forbidden, list), "forbidden_substitutes must be a list")
    for item in ["Playwright", "Chrome for Testing", "Computer Use for Codex in-app browser"]:
        require(item in forbidden, f"missing forbidden substitute: {item}")
        require(item in page, f"visual page missing forbidden substitute: {item}")

    checks = registry.get("checks")
    require(isinstance(checks, list), "checks must be a list")
    check_ids: set[str] = set()
    for index, check in enumerate(checks):
        context = f"checks[{index}]"
        require(isinstance(check, dict), f"{context}: must be object")
        require_no_extra_keys(
            check,
            {"id", "title", "route", "surface", "viewport", "acceptance", "precheck", "status"},
            context,
        )
        check_id = check.get("id")
        require(isinstance(check_id, str), f"{context}: id must be string")
        check_ids.add(check_id)
        route = check.get("route")
        require(isinstance(route, str) and route.startswith("/heuristic-learning/"), f"{context}: invalid route")
        require(route in page, f"{context}: route not documented")
        require(check.get("surface") in {"in-app browser", "Chrome plugin"}, f"{context}: invalid surface")
        require(check.get("viewport") in {"desktop", "mobile"}, f"{context}: invalid viewport")
        acceptance = check.get("acceptance")
        require(isinstance(acceptance, list) and acceptance, f"{context}: acceptance must be non-empty")
        precheck = check.get("precheck")
        require(isinstance(precheck, str) and precheck.startswith("npm run "), f"{context}: invalid precheck")
        script = precheck.removeprefix("npm run ").split()[0]
        require(script in scripts, f"{context}: package script missing for {precheck}")
        require(precheck in page, f"{context}: precheck not documented")
        require(check.get("status") == "required-before-release", f"{context}: status must stay required-before-release until live evidence exists")
    require(check_ids == EXPECTED_CHECK_IDS, f"visual check ids mismatch: {sorted(check_ids)}")

    evidence_log = registry.get("evidence_log")
    require(isinstance(evidence_log, dict), "evidence_log must be an object")
    require_no_extra_keys(
        evidence_log,
        {"path", "artifact_path", "artifact_schema", "required_fields", "current_run_status"},
        "evidence_log",
    )
    require(evidence_log.get("path") == str(PAGE_PATH.relative_to(ROOT)), "evidence log path mismatch")
    require(evidence_log.get("artifact_path") == str(LOG_PATH.relative_to(ROOT)), "visual log artifact path mismatch")
    require(evidence_log.get("artifact_schema") == "/visual-acceptance-log.schema.json", "visual log schema pointer mismatch")
    fields = evidence_log.get("required_fields")
    require(isinstance(fields, list), "required_fields must be a list")
    for field in ["date", "surface", "route", "viewport", "observed_outcome", "remaining_issue"]:
        require(field in fields, f"evidence log missing field {field}")
        require(field in page, f"visual page missing evidence field {field}")
    current_run_status = evidence_log.get("current_run_status")
    require(isinstance(current_run_status, str), "current run status must be a string")
    require(
        current_run_status == "not-run-in-this-repository-state"
        or current_run_status.startswith("partial-")
        or current_run_status.startswith("blocked-")
        or current_run_status.startswith("passed-"),
        "current run status must be not-run, partial, blocked, or passed evidence",
    )

    log = load_json(LOG_PATH)
    log_schema = load_json(LOG_SCHEMA_PATH)
    check_log_schema(log_schema)
    require(log.get("$schema") == "/visual-acceptance-log.schema.json", "visual acceptance log schema pointer mismatch")
    require(log.get("schema_version") == 1, "visual acceptance log schema_version must be 1")
    require(log.get("scope") == "official-browser-visual-acceptance-log", "visual acceptance log scope mismatch")
    require(log.get("status") in {"not-run", "blocked", "passed"}, "visual acceptance log status mismatch")
    entries = log.get("entries")
    require(isinstance(entries, list), "visual acceptance log entries must be a list")
    entry_ids: set[str] = set()
    checks_by_id = {
        check["id"]: check
        for check in checks
        if isinstance(check, dict) and isinstance(check.get("id"), str)
    }
    for index, entry in enumerate(entries):
        context = f"visual_log.entries[{index}]"
        require(isinstance(entry, dict), f"{context}: must be object")
        require_no_extra_keys(
            entry,
            {"check_id", "date", "surface", "route", "viewport", "observed_outcome", "remaining_issue", "status"},
            context,
        )
        check_id = entry.get("check_id")
        require(check_id in checks_by_id, f"{context}: unknown check_id {check_id}")
        entry_ids.add(check_id)
        check = checks_by_id[check_id]
        surface_matches = entry.get("surface") == check.get("surface")
        chrome_fallback = check.get("surface") == "in-app browser" and entry.get("surface") == "Chrome plugin"
        require(surface_matches or chrome_fallback, f"{context}: surface mismatch")
        require(entry.get("route") == check.get("route"), f"{context}: route mismatch")
        require(entry.get("viewport") == check.get("viewport"), f"{context}: viewport mismatch")
        require(entry.get("status") in {"not-run", "blocked", "passed"}, f"{context}: status mismatch")
        for field in ["date", "observed_outcome", "remaining_issue"]:
            require(isinstance(entry.get(field), str) and entry[field], f"{context}: {field} missing")
        if entry.get("status") == "blocked":
            require(
                entry["observed_outcome"] != "not-run" and entry["remaining_issue"] != "not-run",
                f"{context}: blocked entry must record the blocking observation and next issue",
            )
    require(entry_ids == EXPECTED_CHECK_IDS, f"visual acceptance log ids mismatch: {sorted(entry_ids)}")
    entry_statuses = {entry.get("status") for entry in entries}
    if log.get("status") == "passed":
        require(all(entry.get("status") == "passed" for entry in entries), "passed visual log requires all entries passed")
    elif "blocked" in entry_statuses:
        require(log.get("status") == "blocked", "blocked visual entries require top-level blocked status")
    else:
        require(log.get("status") == "not-run", "non-passed visual log without blockers must stay not-run")

    resource_ids = {
        resource.get("id")
        for resource in manifest.get("public_resources", [])
        if isinstance(resource, dict)
    }
    require("visual-verification" in resource_ids, "course manifest missing visual-verification resource")
    require("visual-verification-schema" in resource_ids, "course manifest missing visual-verification schema resource")
    require("visual-acceptance-log" in resource_ids, "course manifest missing visual-acceptance-log resource")
    require("visual-acceptance-log-schema" in resource_ids, "course manifest missing visual-acceptance-log schema resource")

    final_checks = completion.get("final_checks")
    require(isinstance(final_checks, list), "completion final_checks must be a list")
    require(
        any("visual-verification" in check for check in final_checks if isinstance(check, str)),
        "completion audit final checks must mention visual-verification",
    )


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked visual verification with {len(registry['checks'])} checks")


if __name__ == "__main__":
    main()
