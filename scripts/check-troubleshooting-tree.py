#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/troubleshooting-tree.json"
SCHEMA_PATH = ROOT / "docs/public/troubleshooting-tree.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/troubleshooting-tree.md"

EXPECTED_IDS = {
    "install-or-runtime",
    "example-behavior",
    "report-or-benchmark",
    "source-or-claim",
    "course-or-public-routes",
    "release-visual-acceptance",
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
    require(schema.get("title") == "Heuristic Learning Troubleshooting Tree", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "scope", "nodes"], "schema required keys drifted")


def command_known(command: str, scripts: dict[str, Any]) -> bool:
    if command.startswith("npm run "):
        script = command.removeprefix("npm run ").split()[0]
        return script in scripts
    return command in {"node --version", "npm --version"}


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/troubleshooting-tree.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require(registry.get("scope") == "course-repository-failure-diagnosis", "registry scope mismatch")

    page = PAGE_PATH.read_text(encoding="utf-8")
    local_setup = (ROOT / "docs/zh-cn/appendix/local-setup.md").read_text(encoding="utf-8")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")

    nodes = registry.get("nodes")
    require(isinstance(nodes, list) and nodes, "nodes must be non-empty")
    ids: set[str] = set()
    for index, node in enumerate(nodes):
        context = f"nodes[{index}]"
        require(isinstance(node, dict), f"{context}: must be object")
        require(
            set(node)
            == {
                "id",
                "failure_surface",
                "symptom",
                "diagnostic_commands",
                "likely_causes",
                "fix_actions",
                "verification_commands",
                "related_pages",
            },
            f"{context}: unexpected keys",
        )
        node_id = node.get("id")
        require(isinstance(node_id, str), f"{context}: id must be string")
        ids.add(node_id)
        surface = node.get("failure_surface")
        require(isinstance(surface, str) and surface in page, f"{context}: failure surface not documented")
        for field in ["symptom", "diagnostic_commands", "likely_causes", "fix_actions", "verification_commands", "related_pages"]:
            require(node.get(field), f"{context}: {field} missing")
        for command in node.get("diagnostic_commands", []) + node.get("verification_commands", []):
            require(isinstance(command, str) and command_known(command, scripts), f"{context}: unknown command {command}")
            require(command in page or command in local_setup, f"{context}: command not documented: {command}")
        for related_page in node.get("related_pages", []):
            require(isinstance(related_page, str) and (ROOT / related_page).exists(), f"{context}: related page missing {related_page}")

    require(ids == EXPECTED_IDS, f"troubleshooting ids mismatch: {sorted(ids)}")
    page_ids = {item.get("id") for item in manifest.get("core_pages", []) if isinstance(item, dict)}
    resource_ids = {item.get("id") for item in manifest.get("public_resources", []) if isinstance(item, dict)}
    require("troubleshooting-tree" in page_ids, "course manifest missing troubleshooting page")
    require("troubleshooting-tree" in resource_ids, "course manifest missing troubleshooting registry")
    require("troubleshooting-tree-schema" in resource_ids, "course manifest missing troubleshooting schema")
    for required in [
        "/troubleshooting-tree.json",
        "/troubleshooting-tree.schema.json",
        "npm run troubleshooting:tree:check",
        "diagnostic_commands",
        "fix_actions",
        "verification_commands",
    ]:
        require(required in page, f"troubleshooting page missing {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked troubleshooting tree with {len(registry['nodes'])} nodes")


if __name__ == "__main__":
    main()
