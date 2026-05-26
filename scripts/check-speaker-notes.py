#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/public/speaker-notes.json"
SCHEMA_PATH = ROOT / "docs/public/speaker-notes.schema.json"
EXPECTED_IDS = {
    "note-lecture-1",
    "note-lecture-2",
    "note-lecture-3",
    "note-lab-1",
    "note-lab-2",
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
    require(schema.get("title") == "Heuristic Learning Speaker Notes Registry", "schema title mismatch")
    require(schema.get("type") == "object", "schema root type mismatch")
    require(schema.get("additionalProperties") is False, "schema must disallow additional root properties")
    require(schema.get("required") == ["schema_version", "notes"], "schema required keys drifted")


def check_registry(registry: dict[str, Any]) -> None:
    require(registry.get("$schema") == "/speaker-notes.schema.json", "registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "registry schema_version must be 1")

    teaching = load_json(ROOT / "docs/public/teaching-registry.json")
    slide_deck = load_json(ROOT / "docs/public/slide-deck.json")
    manifest = load_json(ROOT / "docs/public/course-manifest.json")
    package = load_json(ROOT / "package.json")
    slides_index = (ROOT / "docs/zh-cn/slides/index.md").read_text(encoding="utf-8")
    teaching_pack = (ROOT / "docs/zh-cn/appendix/teaching-pack.md").read_text(encoding="utf-8")
    audit = (ROOT / "docs/zh-cn/appendix/completion-audit.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    public_llms = (ROOT / "docs/public/llms.txt").read_text(encoding="utf-8")

    scripts = package.get("scripts")
    require(isinstance(scripts, dict), "package scripts must be an object")
    teaching_by_id = {
        material.get("id"): material
        for material in teaching.get("materials", [])
        if isinstance(material, dict) and isinstance(material.get("id"), str)
    }
    slide_ids = {
        material.get("id")
        for material in slide_deck.get("materials", [])
        if isinstance(material, dict) and isinstance(material.get("id"), str)
    }

    notes = registry.get("notes")
    require(isinstance(notes, list) and notes, "notes must be non-empty")
    ids: set[str] = set()
    material_ids: set[str] = set()
    for index, note in enumerate(notes):
        context = f"notes[{index}]"
        require(isinstance(note, dict), f"{context}: must be object")
        require(
            set(note)
            == {
                "id",
                "material_id",
                "title",
                "slide_path",
                "opening_question",
                "demo_checkpoints",
                "discussion_prompts",
                "common_confusions",
                "exit_ticket",
                "verification_commands",
            },
            f"{context}: unexpected keys",
        )
        note_id = note.get("id")
        require(isinstance(note_id, str), f"{context}: id must be string")
        require(note_id not in ids, f"duplicate note id: {note_id}")
        ids.add(note_id)
        material_id = note.get("material_id")
        require(material_id in teaching_by_id, f"{context}: unknown material_id {material_id}")
        require(material_id in slide_ids, f"{context}: material missing from slide deck {material_id}")
        material_ids.add(material_id)
        title = note.get("title")
        require(isinstance(title, str) and title, f"{context}: title missing")
        slide_path = note.get("slide_path")
        require(slide_path == teaching_by_id[material_id]["path"], f"{context}: slide_path does not match teaching registry")
        require((ROOT / slide_path).exists(), f"{context}: slide path missing: {slide_path}")
        slide_text = (ROOT / slide_path).read_text(encoding="utf-8")
        require(teaching_by_id[material_id]["title"] in slide_text, f"{context}: slide title missing")
        require(isinstance(note.get("opening_question"), str) and note["opening_question"], f"{context}: opening_question missing")
        for key in ["demo_checkpoints", "discussion_prompts", "common_confusions"]:
            values = note.get(key)
            require(isinstance(values, list) and values, f"{context}: {key} must be non-empty")
            for value in values:
                require(isinstance(value, str) and value, f"{context}: empty {key} item")
        require(isinstance(note.get("exit_ticket"), str) and note["exit_ticket"], f"{context}: exit_ticket missing")
        for command in note.get("verification_commands", []):
            require(isinstance(command, str) and command.startswith("npm run "), f"{context}: invalid command")
            script = command.removeprefix("npm run ").split()[0]
            require(script in scripts, f"{context}: package script missing for {command}")
            require(command in slide_text or command in audit, f"{context}: command not documented: {command}")

    require(ids == EXPECTED_IDS, f"speaker note ids mismatch: {sorted(ids)}")
    require(material_ids == set(teaching_by_id), "speaker notes must cover every teaching material")

    page_ids = {page.get("id") for page in manifest.get("core_pages", []) if isinstance(page, dict)}
    resource_ids = {resource.get("id") for resource in manifest.get("public_resources", []) if isinstance(resource, dict)}
    require("speaker-notes" not in page_ids, "course manifest should not expose speaker notes as a page")
    require("speaker-notes" in resource_ids, "course manifest missing speaker notes registry")
    require("speaker-notes-schema" in resource_ids, "course manifest missing speaker notes schema")
    for required in [
        "讲者备注",
        "speaker-notes.json",
        "npm run speaker:notes:check",
    ]:
        require(
            required in slides_index
            or required in teaching_pack
            or required in audit
            or required in llms
            or required in public_llms,
            f"speaker notes not linked: {required}",
        )


def main() -> None:
    registry = load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    check_schema(schema)
    check_registry(registry)
    print(f"checked speaker notes with {len(registry['notes'])} notes")


if __name__ == "__main__":
    main()
