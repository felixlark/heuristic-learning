#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/contribution-contract.json"
SCHEMA_PATH = ROOT / "docs/public/contribution-contract.schema.json"
EXPECTED_IDS = {
    "theory-page",
    "case-card",
    "runnable-example",
    "experiment-record",
    "claim-review",
    "reproduction-note",
    "anti-forgetting-review",
    "course-material",
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


def path_exists(path: str) -> bool:
    if path.endswith("/"):
        return (ROOT / path).is_dir()
    return (ROOT / path).exists()


def check_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "Heuristic Learning Contribution Contract", "schema title mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    required = schema.get("required")
    require(isinstance(required, list), "schema required keys must be a list")
    for field in ["schema_version", "contribution_types", "required_commands", "forbidden_materials"]:
        require(field in required, f"schema missing required field {field}")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/contribution-contract.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "contribution_types", "required_commands", "forbidden_materials"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    protocol = (ROOT / "docs/zh-cn/appendix/contribution-protocol.md").read_text(encoding="utf-8")
    pr_template = (ROOT / ".github/pull_request_template.md").read_text(encoding="utf-8")
    appendix = (ROOT / "docs/zh-cn/appendix/index.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")
    reproduction_note = (ROOT / "templates/reproduction-note.md").read_text(encoding="utf-8")
    experiment_record = (ROOT / "templates/experiment-record.md").read_text(encoding="utf-8")

    items = registry.get("contribution_types")
    require(isinstance(items, list) and items, "contribution_types must be non-empty")
    ids: set[str] = set()
    for index, item in enumerate(items):
        context = f"contribution_types[{index}]"
        require(isinstance(item, dict), f"{context}: must be object")
        require_no_extra_keys(
            item,
            {"id", "title", "description", "evidence_fields", "required_paths", "verification_commands"},
            context,
        )
        item_id = item.get("id")
        require(isinstance(item_id, str) and re.match(r"^[a-z0-9-]+$", item_id), f"{context}: invalid id")
        require(item_id not in ids, f"duplicate contribution type id: {item_id}")
        ids.add(item_id)
        title = item.get("title")
        require(isinstance(title, str) and title in contributing, f"{context}: title not documented in CONTRIBUTING")
        require(isinstance(item.get("description"), str) and item["description"], f"{context}: missing description")
        evidence_fields = item.get("evidence_fields")
        require(isinstance(evidence_fields, list) and evidence_fields, f"{context}: evidence_fields must be non-empty")
        for field in evidence_fields:
            require(isinstance(field, str) and field, f"{context}: evidence field must be string")
        required_paths = item.get("required_paths")
        require(isinstance(required_paths, list) and required_paths, f"{context}: required_paths must be non-empty")
        for path in required_paths:
            require(isinstance(path, str) and path_exists(path), f"{context}: required path missing: {path}")
        commands = item.get("verification_commands")
        require(isinstance(commands, list) and commands, f"{context}: verification_commands must be non-empty")
        for command in commands:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command {command}")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for command {command}")
            require(command in contributing or command in protocol or command in pr_template, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"contribution type ids mismatch: {sorted(ids)}")

    required_commands = registry.get("required_commands")
    require(isinstance(required_commands, list) and required_commands, "required_commands must be non-empty")
    for command in required_commands:
        require(isinstance(command, str) and command.startswith("npm run "), f"invalid required command: {command}")
        script = command.removeprefix("npm run ").split()[0]
        require(script in scripts, f"package script missing for required command {command}")
        require(command in contributing or command in protocol or command in pr_template or command in audit, f"required command not documented: {command}")

    forbidden = registry.get("forbidden_materials")
    require(isinstance(forbidden, list) and forbidden, "forbidden_materials must be non-empty")
    for item in forbidden:
        require(isinstance(item, str) and item, "forbidden item must be string")
    for required in [
        "secrets",
        "Feishu/Lark raw content",
        "X cookies/API credentials",
        "private logs",
        "unverified X/Feishu signals",
    ]:
        require(required in contributing or required in protocol or required in pr_template, f"forbidden material not documented: {required}")

    for required in [
        "/contribution-contract.json",
        "/contribution-contract.schema.json",
        "npm run contribution:contract:check",
    ]:
        require(required in protocol, f"contribution protocol missing public surface: {required}")
    for required in [
        "contribution-contract.json",
        "贡献与研究协议",
        "npm run contribution:contract:check",
    ]:
        require(required in appendix or required in audit or required in llms or required in public_llms, f"contribution contract not linked: {required}")

    for item in registry.get("contribution_types", []):
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        require(isinstance(title, str) and title in pr_template, f"PR template missing contribution type: {title}")
    for required in [
        "Result summary",
        "Candidate update",
        "Falsification path",
        "Reproduction scope / missing fidelity",
    ]:
        require(required in pr_template, f"PR template missing evidence field: {required}")

    reproduction_item = next(
        item
        for item in registry.get("contribution_types", [])
        if isinstance(item, dict) and item.get("id") == "reproduction-note"
    )
    for required in [
        "templates/reproduction-note.md",
        "Reproduction note",
        "source status",
        "reproduction scope",
        "missing fidelity",
        "falsification path",
        "next experiment",
    ]:
        require(
            required in contributing or required in protocol or required in pr_template or required in llms or required in public_llms,
            f"reproduction note not linked: {required}",
        )
    for required in [
        "Source",
        "Cache status",
        "What would falsify it",
        "Reproduction Scope",
        "Missing fidelity",
        "Next experiment",
        "What must not be overclaimed",
    ]:
        require(required in reproduction_note, f"reproduction note template missing {required}")
    for command in reproduction_item.get("verification_commands", []):
        require(command in reproduction_note, f"reproduction note template missing command {command}")

    experiment_item = next(
        item
        for item in registry.get("contribution_types", [])
        if isinstance(item, dict) and item.get("id") == "experiment-record"
    )
    for required in [
        "templates/experiment-record.md",
        "Experiment record",
        "run command",
        "source status",
        "result summary",
        "feedback",
        "candidate update",
    ]:
        require(
            required in contributing or required in protocol or required in pr_template or required in llms or required in public_llms,
            f"experiment record not linked: {required}",
        )
    for required in ["Command", "Environment", "Source status", "Result", "Feedback", "Candidate Update"]:
        require(required in experiment_record, f"experiment record template missing {required}")
    for command in experiment_item.get("verification_commands", []):
        require(command in contributing or command in protocol or command in pr_template, f"experiment record command not documented {command}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked contribution contract with {len(registry['contribution_types'])} contribution types")


if __name__ == "__main__":
    main()
