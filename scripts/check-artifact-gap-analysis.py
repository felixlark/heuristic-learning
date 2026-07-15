#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/artifact-gap-analysis.json"
SCHEMA_PATH = ROOT / "docs/public/artifact-gap-analysis.schema.json"
PAGE_PATH = ROOT / "docs/zh-cn/appendix/artifact-gap-analysis.md"

EXPECTED_IDS = {
    "ant-gait-artifact-gap",
    "breakout-artifact-gap",
    "vizdoom-artifact-gap",
    "robot-soccer-artifact-gap",
    "traffic-grid-artifact-gap",
    "gridworld-teaching-gap",
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
    require(schema.get("title") == "Heuristic Learning Artifact Gap Analysis", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "scope", "artifacts"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/artifact-gap-analysis.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")
    require(registry.get("scope") == "lightweight-replay-to-source-artifact-gap", "registry scope mismatch")

    page = PAGE_PATH.read_text(encoding="utf-8")
    source_registry = (ROOT / "docs/zh-cn/appendix/source-registry.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs/zh-cn/appendix/research-roadmap.md").read_text(encoding="utf-8")
    benchmark = load_json(ROOT / "docs/public/benchmark-summary.json")
    ablation = load_json(ROOT / "docs/public/ablation-plan.json")
    examples = load_json(ROOT / "docs/public/example-registry.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    example_ids = {item.get("id") for item in examples.get("examples", []) if isinstance(item, dict)}
    benchmark_examples = {item.get("id") for item in benchmark.get("summary", []) if isinstance(item, dict)}
    ablation_examples = {item.get("example_id") for item in ablation.get("ablations", []) if isinstance(item, dict)}

    artifacts = registry.get("artifacts")
    require(isinstance(artifacts, list) and artifacts, "artifacts must be non-empty")
    ids: set[str] = set()
    covered_examples: set[str] = set()
    source_refs: set[str] = set()
    for index, artifact in enumerate(artifacts):
        context = f"artifacts[{index}]"
        require(isinstance(artifact, dict), f"{context}: must be object")
        require(
            set(artifact)
            == {
                "id",
                "title",
                "source_status",
                "source_reference",
                "example_id",
                "current_replay",
                "missing_fidelity",
                "next_experiment",
                "verification_commands",
                "boundary",
            },
            f"{context}: unexpected keys",
        )
        artifact_id = artifact.get("id")
        require(isinstance(artifact_id, str), f"{context}: id must be string")
        require(artifact_id not in ids, f"duplicate artifact id: {artifact_id}")
        ids.add(artifact_id)
        title = artifact.get("title")
        require(isinstance(title, str) and title in page, f"{context}: title not documented")
        example_id = artifact.get("example_id")
        require(example_id in example_ids, f"{context}: unknown example id {example_id}")
        require(example_id in benchmark_examples, f"{context}: benchmark missing example {example_id}")
        require(example_id in ablation_examples, f"{context}: ablation plan missing example {example_id}")
        covered_examples.add(example_id)
        source_reference = artifact.get("source_reference")
        require(isinstance(source_reference, str) and source_reference, f"{context}: source_reference missing")
        source_refs.add(source_reference)
        if "Repository-local" not in source_reference:
            require(source_reference in source_registry or source_reference in roadmap, f"{context}: source reference not traceable")
        for field in ["source_status", "current_replay", "next_experiment", "boundary"]:
            require(isinstance(artifact.get(field), str) and artifact[field], f"{context}: {field} missing")
        missing = artifact.get("missing_fidelity")
        require(isinstance(missing, list) and len(missing) >= 2, f"{context}: missing_fidelity too thin")
        for item in missing:
            require(isinstance(item, str) and item, f"{context}: invalid missing_fidelity item")
        for command in artifact.get("verification_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in page, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"artifact gap ids mismatch: {sorted(ids)}")
    require(covered_examples == example_ids, "artifact gap analysis must cover all runnable examples")
    require("mujoco/ant/heuristic_ant.py" in source_refs, "missing Ant source reference")
    require("atari/breakout/heuristic_breakout.py" in source_refs, "missing Breakout source reference")
    require("vizdoom/heuristic_vizdoom_d1_cv.py" in source_refs, "missing VizDoom source reference")

    page_ids = {item.get("id") for item in manifest.get("core_pages", []) if isinstance(item, dict)}
    resource_ids = {item.get("id") for item in manifest.get("public_resources", []) if isinstance(item, dict)}
    require("artifact-gap-analysis" in page_ids, "course manifest missing artifact gap page")
    require("artifact-gap-analysis" in resource_ids, "course manifest missing artifact gap registry")
    require("artifact-gap-analysis-schema" in resource_ids, "course manifest missing artifact gap schema")
    for required in [
        "/artifact-gap-analysis.json",
        "/artifact-gap-analysis.schema.json",
        "npm run artifact:gap:check",
        "轻量 replay",
        "真实 artifact",
    ]:
        require(required in page, f"artifact gap page missing {required}")
    for required in [
        "Artifact 差距分析",
        "artifact-gap-analysis.json",
        "npm run artifact:gap:check",
    ]:
        require(required in roadmap or required in source_registry or required in page, f"artifact gap not linked: {required}")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked artifact gap analysis with {len(registry['artifacts'])} artifacts")


if __name__ == "__main__":
    main()
