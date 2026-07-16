#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/x-sources.json"
SCHEMA_PATH = ROOT / "docs/public/x-sources.schema.json"
EXPECTED_IDS = {
    "aigclink-medgemma-1-5-2026-01-13",
    "ayinotes-hassabis-frontier-ai-2026-07-14",
    "deusyu-shape-from-shading-2025-11-07",
    "dotey-brain2qwerty-v2-2026-06-29",
    "logicrw-jiayi-hl-summary-2026-05-08",
    "jiayi-original-hl-post-2026-05-08",
    "logicrw-fluid-control-lead-2026-05-19",
    "phoenixyin-economic-connectedness-2026-07-01",
    "phoenixyin-language-models-need-sleep-2026-07-14",
    "safaricheung-android-earthquake-2026-06-26",
    "yatingzhao-machine-age-2026-06-29",
}
EXPECTED_EXTRACTION_IDS = {
    "android-crowdsourced-earthquake-alerts",
    "automation-organizational-consequences",
    "brain2qwerty-external-validity",
    "economic-connectedness-causal-boundary",
    "frontier-ai-standards-governance",
    "medgemma-clinical-deployment-boundary",
    "shape-from-shading-prior",
    "sleep-inspired-continual-learning",
    "breakout-code-as-memory",
    "ant-controller-as-readable-policy",
    "hybrid-perception-boundary",
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
    require(schema.get("title") == "Heuristic Learning X Sources Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "source_policy", "sources", "extraction_cards"], "schema required keys drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict) and "source" in defs, "schema must define source")
    require("extraction_card" in defs, "schema must define extraction_card")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/x-sources.schema.json", "registry schema pointer mismatch")
    require_no_extra_keys(registry, {"$schema", "schema_version", "source_policy", "sources", "extraction_cards"}, "registry")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    source_policy = registry.get("source_policy")
    require(isinstance(source_policy, dict), "source_policy must be object")
    require("Public X material" in source_policy.get("reader_rule", ""), "x sources must document reader-facing source policy")

    page = (ROOT / "docs/zh-cn/cases/x-signal/index.md").read_text(encoding="utf-8")
    source_registry = (ROOT / "docs/zh-cn/appendix/source-registry.md").read_text(encoding="utf-8")
    manifest = (ROOT / "docs/public/course-manifest.json").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    sources = registry.get("sources")
    require(isinstance(sources, list) and sources, "sources must be a non-empty list")
    ids: set[str] = set()
    evidence_statuses: set[str] = set()
    levels: set[str] = set()
    allowed = {
        "id",
        "url",
        "author",
        "date",
        "source_level",
        "evidence_status",
        "claims_to_extract",
        "repo_targets",
        "verification_status",
        "boundary",
    }
    for index, source in enumerate(sources):
        context = f"sources[{index}]"
        require(isinstance(source, dict), f"{context}: must be object")
        require_no_extra_keys(source, allowed, context)
        require_pattern(source.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        source_id = source["id"]
        require(source_id not in ids, f"duplicate source id: {source_id}")
        ids.add(source_id)
        require_pattern(source.get("url"), r"^https://x\.com/.+/status/[0-9]+$", f"{context}.url")
        require(source["url"] in page or source["url"] in source_registry, f"{context}: URL not documented")
        require_pattern(source.get("author"), r"^@.+", f"{context}.author")
        levels.add(source.get("source_level"))
        evidence_statuses.add(source.get("evidence_status"))

        for key in ["claims_to_extract", "repo_targets"]:
            items = source.get(key)
            require(isinstance(items, list) and items, f"{context}: {key} must be non-empty")
        for target in source["repo_targets"]:
            if target.startswith("docs/") or target.startswith("examples/"):
                require((ROOT / target).exists(), f"{context}: repo target missing: {target}")

        boundary = source.get("boundary")
        require(isinstance(boundary, str) and boundary, f"{context}: boundary must be non-empty")

    require(ids == EXPECTED_IDS, f"x source ids mismatch: {sorted(ids)}")
    require(
        {"reviewed-secondary-summary", "known-url-needs-direct-review", "to-collect"}.issubset(evidence_statuses),
        "x sources must preserve evidence status boundaries",
    )
    require({"primary-url-referenced", "secondary-summary", "secondary-lead"}.issubset(levels), "x sources must preserve source level boundaries")

    cards = registry.get("extraction_cards")
    require(isinstance(cards, list) and cards, "extraction_cards must be a non-empty list")
    card_ids: set[str] = set()
    source_ids = ids
    allowed_card_keys = {
        "id",
        "source_id",
        "concept",
        "course_claim",
        "evidence_status",
        "landing_pages",
        "runnable_example",
        "verification",
        "boundary",
    }
    for index, card in enumerate(cards):
        context = f"extraction_cards[{index}]"
        require(isinstance(card, dict), f"{context}: must be object")
        require_no_extra_keys(card, allowed_card_keys, context)
        require_pattern(card.get("id"), r"^[a-z0-9-]+$", f"{context}.id")
        card_id = card["id"]
        require(card_id not in card_ids, f"duplicate extraction card id: {card_id}")
        card_ids.add(card_id)
        require(card.get("source_id") in source_ids, f"{context}: source_id does not match source list")
        concept = card.get("concept")
        require(isinstance(concept, str) and concept in page, f"{context}: concept not documented on X page")
        claim = card.get("course_claim")
        require(isinstance(claim, str) and claim, f"{context}: course_claim must be non-empty")
        require(
            card.get("evidence_status")
            in {
                "secondary-source-plus-public-artifact",
                "secondary-source-summary",
                "x-lead-plus-primary-literature",
            },
            f"{context}: invalid evidence_status",
        )
        landing_pages = card.get("landing_pages")
        require(isinstance(landing_pages, list) and landing_pages, f"{context}: landing_pages must be non-empty")
        for landing_page in landing_pages:
            require(isinstance(landing_page, str), f"{context}: landing page must be string")
            require((ROOT / landing_page).exists(), f"{context}: landing page missing: {landing_page}")
        runnable_example = card.get("runnable_example")
        if runnable_example is not None:
            require(isinstance(runnable_example, str), f"{context}: runnable_example must be string or null")
            require((ROOT / runnable_example).is_dir(), f"{context}: runnable example missing: {runnable_example}")
            require(runnable_example in page, f"{context}: runnable example not documented on X page")
        verification = card.get("verification")
        require(isinstance(verification, list) and verification, f"{context}: verification must be non-empty")
        for command in verification:
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid verification command")
            require(command in page or command in source_registry, f"{context}: verification command not documented: {command}")
        boundary = card.get("boundary")
        require(isinstance(boundary, str) and boundary, f"{context}: boundary must be non-empty")

    require(card_ids == EXPECTED_EXTRACTION_IDS, f"x extraction card ids mismatch: {sorted(card_ids)}")
    require(
        any(card.get("runnable_example") is None for card in cards if isinstance(card, dict)),
        "x extraction cards must preserve non-runnable research-boundary card",
    )
    require("docs/public/x-sources.json" in llms, "root llms.txt missing x-sources.json")
    require("/x-sources.json" in public_llms, "public llms.txt missing x-sources route")
    require("docs/zh-cn/cases/x-signal/index.md" in manifest, "course manifest must include X signal case")


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked X sources with {len(registry['sources'])} sources")


if __name__ == "__main__":
    main()
