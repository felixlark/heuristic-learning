#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "docs/zh-cn/index.md",
    "docs/zh-cn/course-map/index.md",
    "docs/zh-cn/syllabus/index.md",
    "docs/zh-cn/stage-1/index.md",
    "docs/zh-cn/stage-2/index.md",
    "docs/zh-cn/stage-3/index.md",
    "docs/zh-cn/theory/learning-loop.md",
    "docs/zh-cn/theory/research-framework.md",
    "docs/zh-cn/examples/index.md",
    "docs/zh-cn/cases/index.md",
    "docs/zh-cn/cases/ant-gait/index.md",
    "docs/zh-cn/cases/breakout/index.md",
    "docs/zh-cn/cases/robot-soccer/index.md",
    "docs/zh-cn/cases/vizdoom/index.md",
    "docs/zh-cn/cases/traffic-simulation/index.md",
    "docs/zh-cn/cases/x-signal/index.md",
    "docs/zh-cn/slides/index.md",
    "docs/zh-cn/slides/lecture-1/index.md",
    "docs/zh-cn/slides/lecture-2/index.md",
    "docs/zh-cn/slides/lecture-3/index.md",
    "docs/zh-cn/slides/lab-1/index.md",
    "docs/zh-cn/slides/lab-2/index.md",
    "docs/zh-cn/appendix/index.md",
    "docs/zh-cn/appendix/local-setup.md",
    "docs/zh-cn/appendix/troubleshooting-tree.md",
    "docs/zh-cn/appendix/glossary.md",
    "docs/zh-cn/appendix/references.md",
    "docs/zh-cn/appendix/reading-guide.md",
    "docs/zh-cn/appendix/case-registry.md",
    "docs/zh-cn/appendix/code-tour.md",
    "docs/zh-cn/appendix/learning-units.md",
    "docs/zh-cn/appendix/learning-outcomes.md",
    "docs/zh-cn/appendix/checkpoints.md",
    "docs/zh-cn/appendix/evaluation-metrics.md",
    "docs/zh-cn/appendix/paper-blueprint.md",
    "docs/zh-cn/appendix/speaker-notes.md",
    "docs/zh-cn/appendix/concept-graph.md",
    "docs/zh-cn/appendix/teaching-pack.md",
    "docs/zh-cn/appendix/citation.md",
    "docs/zh-cn/appendix/source-registry.md",
    "docs/zh-cn/appendix/source-to-case-playbook.md",
    "docs/zh-cn/appendix/release-checklist.md",
    "docs/zh-cn/appendix/rubric.md",
    "docs/zh-cn/appendix/instructor-guide.md",
    "docs/zh-cn/appendix/course-schedule.md",
    "docs/zh-cn/appendix/completion-audit.md",
    "docs/zh-cn/appendix/public-entrypoints.md",
    "docs/zh-cn/appendix/visual-verification.md",
    "docs/zh-cn/appendix/reproducibility.md",
    "docs/zh-cn/appendix/exercises.md",
    "docs/zh-cn/appendix/research-projects.md",
    "docs/zh-cn/appendix/research-logbook.md",
    "docs/zh-cn/appendix/ablation-plan.md",
    "docs/zh-cn/appendix/artifact-gap-analysis.md",
    "docs/zh-cn/appendix/benchmark-protocol.md",
    "docs/zh-cn/appendix/benchmark-results.md",
    "docs/zh-cn/appendix/research-roadmap.md",
    "docs/zh-cn/appendix/contribution-protocol.md",
]

EXAMPLES = {
    "gridworld": {
        "dir": "examples/heuristic-gridworld",
        "run_script": "examples:gridworld",
        "feedback_script": "examples:gridworld:feedback",
        "report": "experiments/gridworld/latest.json",
        "test": "tests/test_gridworld.py",
        "readme": "examples/heuristic-gridworld/README.md",
        "syllabus_terms": ["GridWorld", "local_greedy_trap"],
    },
    "robot-soccer": {
        "dir": "examples/robot-soccer",
        "run_script": "examples:robot-soccer",
        "feedback_script": "examples:robot-soccer:feedback",
        "report": "experiments/robot-soccer/latest.json",
        "test": "tests/test_robot_soccer.py",
        "readme": "examples/robot-soccer/README.md",
        "syllabus_terms": ["Robot Soccer", "blocked_shot"],
    },
    "vizdoom-replay": {
        "dir": "examples/vizdoom-replay",
        "run_script": "examples:vizdoom-replay",
        "feedback_script": "examples:vizdoom-replay:feedback",
        "report": "experiments/vizdoom-replay/latest.json",
        "test": "tests/test_vizdoom_replay.py",
        "readme": "examples/vizdoom-replay/README.md",
        "syllabus_terms": ["VizDoom Replay", "wasted_pickup"],
    },
    "traffic-grid": {
        "dir": "examples/traffic-grid",
        "run_script": "examples:traffic-grid",
        "feedback_script": "examples:traffic-grid:feedback",
        "report": "experiments/traffic-grid/latest.json",
        "test": "tests/test_traffic_grid.py",
        "readme": "examples/traffic-grid/README.md",
        "syllabus_terms": ["Traffic Grid", "spillback"],
    },
    "breakout-replay": {
        "dir": "examples/breakout-replay",
        "run_script": "examples:breakout-replay",
        "feedback_script": "examples:breakout-replay:feedback",
        "report": "experiments/breakout-replay/latest.json",
        "test": "tests/test_breakout_replay.py",
        "readme": "examples/breakout-replay/README.md",
        "syllabus_terms": ["Breakout Replay", "missed_after_wall_reflection"],
    },
    "ant-gait-replay": {
        "dir": "examples/ant-gait-replay",
        "run_script": "examples:ant-gait-replay",
        "feedback_script": "examples:ant-gait-replay:feedback",
        "report": "experiments/ant-gait-replay/latest.json",
        "test": "tests/test_ant_gait_replay.py",
        "readme": "examples/ant-gait-replay/README.md",
        "syllabus_terms": ["Ant Gait Replay", "yaw_drift"],
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_pages() -> None:
    for page in PAGES:
        path = ROOT / page
        require(path.exists(), f"missing course page: {page}")
        text = path.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"page missing frontmatter: {page}")


def split_markdown_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_markdown_table_separator(line: str) -> bool:
    cells = split_markdown_table_row(line)
    return bool(cells) and all(cell and set(cell) <= {"-", ":"} for cell in cells)


def check_markdown_tables() -> None:
    for page in PAGES:
        lines = (ROOT / page).read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines[:-1]):
            if not (line.lstrip().startswith("|") and lines[index + 1].lstrip().startswith("|")):
                continue
            if not is_markdown_table_separator(lines[index + 1]):
                continue
            header_cells = split_markdown_table_row(line)
            separator_cells = split_markdown_table_row(lines[index + 1])
            require(
                len(header_cells) == len(separator_cells),
                f"{page}:{index + 1}: markdown table header has {len(header_cells)} columns but separator has {len(separator_cells)}",
            )
            row_index = index + 2
            while row_index < len(lines) and lines[row_index].lstrip().startswith("|"):
                row_cells = split_markdown_table_row(lines[row_index])
                require(
                    len(row_cells) == len(header_cells),
                    f"{page}:{row_index + 1}: markdown table row has {len(row_cells)} columns but header has {len(header_cells)}",
                )
                row_index += 1


def check_no_raw_mermaid_blocks() -> None:
    for page in PAGES:
        text = (ROOT / page).read_text(encoding="utf-8")
        require(
            "```mermaid" not in text,
            f"{page}: raw Mermaid block renders as code in the current VitePress setup",
        )


def check_package_scripts() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package.get("scripts", {})
    require(isinstance(scripts, dict), "package.json scripts must be an object")
    for script in [
        "verify",
        "examples:test",
        "examples:feedback",
        "examples:reports:check",
        "examples:registry:check",
        "code:tour:check",
        "benchmark:summary:check",
        "ablation:plan:check",
        "artifact:gap:check",
        "source:registry:check",
        "cases:check",
        "x:sources:check",
        "source:case:check",
        "claims:registry:check",
        "teaching:registry:check",
        "slides:check",
        "speaker:notes:check",
        "rubric:check",
        "exercises:check",
        "contribution:contract:check",
        "reproducibility:check",
        "troubleshooting:tree:check",
        "concept:graph:check",
        "learning:units:check",
        "learning:outcomes:check",
        "checkpoints:check",
        "metrics:check",
        "paper:blueprint:check",
        "teaching:pack:check",
        "research:projects:check",
        "research:logbook:check",
        "visual:verification:check",
        "completion:audit:check",
        "release:readiness:check",
        "docs:routes:check",
        "course:manifest:check",
    ]:
        require(script in scripts, f"missing package script: {script}")
    for name, spec in EXAMPLES.items():
        require(spec["run_script"] in scripts, f"{name}: missing run script")
        require(spec["feedback_script"] in scripts, f"{name}: missing feedback script")


def check_examples() -> None:
    for name, spec in EXAMPLES.items():
        example_dir = ROOT / spec["dir"]
        require(example_dir.is_dir(), f"{name}: missing example directory")
        require((example_dir / "run.py").exists(), f"{name}: missing run.py")
        require((example_dir / "feedback_loop.py").exists(), f"{name}: missing feedback_loop.py")
        require((ROOT / spec["report"]).exists(), f"{name}: missing latest report")
        require((ROOT / spec["test"]).exists(), f"{name}: missing test file")
        readme_path = ROOT / spec["readme"]
        require(readme_path.exists(), f"{name}: missing example README")
        readme = readme_path.read_text(encoding="utf-8")
        for expected in [
            spec["run_script"],
            spec["feedback_script"],
            spec["report"],
            spec["test"],
            *spec["syllabus_terms"][1:],
        ]:
            require(expected in readme, f"{name}: README missing {expected}")


def check_syllabus_alignment() -> None:
    syllabus = read_text("docs/zh-cn/syllabus/index.md")
    readme = read_text("README.md")
    for name, spec in EXAMPLES.items():
        require(spec["run_script"] in syllabus, f"{name}: syllabus missing run command")
        require(spec["report"] in syllabus, f"{name}: syllabus missing report path")
        require(spec["run_script"] in readme, f"{name}: README missing run command")
        require(spec["feedback_script"] in readme, f"{name}: README missing feedback command")
        for term in spec["syllabus_terms"]:
            require(term in syllabus, f"{name}: syllabus missing term {term}")
            require(term in readme, f"{name}: README missing term {term}")
    for command in [
        "npm run examples:test",
        "npm run examples:feedback",
        "npm run examples:reports:check",
        "npm run benchmark:summary:check",
        "npm run verify",
    ]:
        require(command in readme, f"README missing command {command}")
    for required in [
        "benchmark-summary.json",
        "x-sources.json",
        "source-to-case-playbook.json",
        "artifact-gap-analysis.json",
        "troubleshooting-tree.json",
        "code-tour.json",
        "learning-units.md",
        "teaching-pack.md",
        "research-logbook.json",
        "completion-audit.json",
        "public-entrypoints.md",
        "visual-verification.json",
        "visual-acceptance-log.json",
        "Benchmark 结果摘要",
    ]:
        require(required in readme, f"README missing public surface: {required}")


def check_llm_pointers() -> None:
    llms = read_text("llms.txt")
    public_llms = read_text("docs/public/llms.txt")
    for pointer in [
        "docs/zh-cn/syllabus/index.md",
        "docs/zh-cn/course-map/index.md",
        "docs/zh-cn/appendix/source-registry.md",
        "docs/zh-cn/appendix/source-to-case-playbook.md",
        "docs/zh-cn/appendix/local-setup.md",
        "docs/zh-cn/appendix/troubleshooting-tree.md",
        "docs/zh-cn/appendix/glossary.md",
        "docs/zh-cn/appendix/references.md",
        "docs/zh-cn/appendix/reading-guide.md",
            "docs/zh-cn/appendix/case-registry.md",
        "docs/zh-cn/appendix/learning-units.md",
        "docs/zh-cn/appendix/learning-outcomes.md",
        "docs/zh-cn/appendix/checkpoints.md",
        "docs/zh-cn/appendix/concept-graph.md",
        "docs/zh-cn/appendix/teaching-pack.md",
        "docs/zh-cn/appendix/citation.md",
        "docs/zh-cn/appendix/release-checklist.md",
        "docs/zh-cn/appendix/instructor-guide.md",
        "docs/zh-cn/appendix/course-schedule.md",
        "docs/zh-cn/appendix/completion-audit.md",
        "docs/zh-cn/appendix/public-entrypoints.md",
        "docs/zh-cn/appendix/visual-verification.md",
        "docs/zh-cn/appendix/reproducibility.md",
        "docs/zh-cn/appendix/exercises.md",
        "docs/zh-cn/appendix/research-projects.md",
        "docs/zh-cn/appendix/research-logbook.md",
        "docs/zh-cn/appendix/benchmark-protocol.md",
        "docs/zh-cn/appendix/benchmark-results.md",
        "scripts/check-experiment-reports.py",
        "docs/public/experiment-report.schema.json",
        "scripts/check-example-registry.py",
        "docs/public/example-registry.json",
        "docs/public/example-registry.schema.json",
        "scripts/check-code-tour.py",
        "docs/public/code-tour.json",
        "docs/public/code-tour.schema.json",
        "scripts/check-benchmark-summary.py",
        "docs/public/benchmark-summary.json",
        "docs/public/benchmark-summary.schema.json",
        "scripts/check-ablation-plan.py",
        "docs/public/ablation-plan.json",
        "docs/public/ablation-plan.schema.json",
        "scripts/check-artifact-gap-analysis.py",
        "docs/public/artifact-gap-analysis.json",
        "docs/public/artifact-gap-analysis.schema.json",
        "scripts/check-troubleshooting-tree.py",
        "docs/public/troubleshooting-tree.json",
        "docs/public/troubleshooting-tree.schema.json",
        "scripts/check-claims-registry.py",
        "docs/public/claims-registry.json",
        "docs/public/claims-registry.schema.json",
        "scripts/check-case-registry.py",
        "docs/public/case-registry.json",
        "docs/public/case-registry.schema.json",
        "scripts/check-teaching-registry.py",
        "docs/public/teaching-registry.json",
        "docs/public/teaching-registry.schema.json",
        "scripts/check-slide-deck.py",
        "docs/public/slide-deck.json",
        "docs/public/slide-deck.schema.json",
        "scripts/check-speaker-notes.py",
        "docs/public/speaker-notes.json",
        "docs/public/speaker-notes.schema.json",
        "scripts/check-rubric.py",
        "docs/public/rubric.json",
        "docs/public/rubric.schema.json",
        "scripts/check-exercise-registry.py",
        "docs/public/exercise-registry.json",
        "docs/public/exercise-registry.schema.json",
        "scripts/check-contribution-contract.py",
        "docs/public/contribution-contract.json",
        "docs/public/contribution-contract.schema.json",
        "scripts/check-reproducibility.py",
        "docs/public/reproducibility-checklist.json",
        "docs/public/reproducibility-checklist.schema.json",
        "scripts/check-learning-units.py",
        "docs/public/learning-units.json",
        "docs/public/learning-units.schema.json",
        "scripts/check-learning-outcomes.py",
        "docs/public/learning-outcomes.json",
        "docs/public/learning-outcomes.schema.json",
        "scripts/check-checkpoints.py",
        "docs/public/checkpoint-registry.json",
        "docs/public/checkpoint-registry.schema.json",
        "scripts/check-evaluation-metrics.py",
        "docs/public/evaluation-metrics.json",
        "docs/public/evaluation-metrics.schema.json",
        "scripts/check-paper-blueprint.py",
        "docs/public/paper-blueprint.json",
        "docs/public/paper-blueprint.schema.json",
        "scripts/check-concept-graph.py",
        "docs/public/concept-graph.json",
        "docs/public/concept-graph.schema.json",
        "scripts/check-teaching-pack.py",
        "docs/public/teaching-pack.json",
        "docs/public/teaching-pack.schema.json",
        "scripts/check-research-projects.py",
        "docs/public/research-projects.json",
        "docs/public/research-projects.schema.json",
        "scripts/check-research-logbook.py",
        "docs/public/research-logbook.json",
        "docs/public/research-logbook.schema.json",
        "scripts/check-completion-audit.py",
        "docs/public/completion-audit.json",
        "docs/public/completion-audit.schema.json",
        "scripts/check-visual-verification.py",
        "docs/public/visual-verification.json",
        "docs/public/visual-verification.schema.json",
        "docs/public/visual-acceptance-log.json",
        "docs/public/visual-acceptance-log.schema.json",
        "scripts/check-routes.sh",
        "scripts/check-source-registry.py",
        "scripts/check-x-sources.py",
        "scripts/check-source-to-case-playbook.py",
        "docs/public/source-to-case-playbook.json",
        "docs/public/source-to-case-playbook.schema.json",
        "scripts/check-course-manifest.py",
    ]:
        require(pointer in llms or pointer in public_llms, f"missing LLM pointer: {pointer}")


def check_ci_workflows() -> None:
    verify = read_text(".github/workflows/verify.yml")
    deploy = read_text(".github/workflows/deploy.yml")
    pr_template = read_text(".github/pull_request_template.md")
    contributing = read_text("CONTRIBUTING.md")
    source_issue = read_text(".github/ISSUE_TEMPLATE/source-signal.yml")
    example_issue = read_text(".github/ISSUE_TEMPLATE/runnable-example.yml")
    course_issue = read_text(".github/ISSUE_TEMPLATE/course-material.yml")
    reproduction_issue = read_text(".github/ISSUE_TEMPLATE/reproduction-note.yml")
    experiment_issue = read_text(".github/ISSUE_TEMPLATE/experiment-record.yml")
    claim_issue = read_text(".github/ISSUE_TEMPLATE/claim-review.yml")
    anti_forgetting_issue = read_text(".github/ISSUE_TEMPLATE/anti-forgetting-review.yml")
    security = read_text("SECURITY.md")

    require("name: Verify course repository" in verify, "verify workflow has unexpected name")
    require("pull_request:" in verify, "verify workflow must run on pull requests")
    require("push:" in verify and "- main" in verify, "verify workflow must run on main pushes")
    require("actions/setup-node@v4" in verify, "verify workflow must set up Node")
    require("actions/setup-python@v5" in verify, "verify workflow must set up Python")
    require("npm ci" in verify, "verify workflow must install dependencies with npm ci")
    require("npm run verify" in verify, "verify workflow must run npm run verify")

    require("actions/configure-pages@v4" in deploy, "deploy workflow must configure Pages")
    require("npm run verify" in deploy, "deploy workflow must verify before building")
    require("npm run build" in deploy, "deploy workflow must build the VitePress site")
    require("actions/upload-pages-artifact@v3" in deploy, "deploy workflow must upload Pages artifact")

    for required in [
        "npm run verify",
        "npm run examples:registry:check",
        "npm run benchmark:summary:check",
        "npm run source:registry:check",
        "npm run cases:check",
        "npm run x:sources:check",
        "npm run claims:registry:check",
        "npm run teaching:registry:check",
        "npm run slides:check",
        "npm run speaker:notes:check",
        "npm run rubric:check",
        "npm run learning:units:check",
        "npm run teaching:pack:check",
        "npm run course:manifest:check",
        "npm run course:structure:check",
        "npm run docs:routes:check",
        "Feedback report",
        "source registry",
        "secrets",
    ]:
        require(required in pr_template or required in contributing, f"missing contribution guard: {required}")

    require("Related Issue" in pr_template, "PR template must reference related issues")
    for required in [
        "name: Reproduction note",
        "Source status",
        "Reproduction scope",
        "Missing fidelity",
        "Falsification path",
        "Next experiment",
        "npm run research:logbook:check",
        "npm run source:case:check",
    ]:
        require(required in reproduction_issue or required in contributing, f"missing reproduction issue guard: {required}")

    for required in [
        "templates/case-card.md",
        "templates/experiment-record.md",
        "templates/claim-review.md",
        "templates/reproduction-note.md",
        "templates/anti-forgetting-checklist.md",
        "examples/*/README.md",
        "docs/zh-cn/appendix/rubric.md",
        "docs/zh-cn/appendix/contribution-protocol.md",
    ]:
        require(required in contributing, f"CONTRIBUTING missing {required}")

    for required in [
        "Source signal",
        "Source status",
        "Verification path",
        "to_collect",
        "reproduced",
        "Do not paste secrets",
    ]:
        require(required in source_issue, f"source issue template missing {required}")
    for required in [
        "Runnable example",
        "Failure mode",
        "Heuristic patch",
        "Expected artifacts",
        "npm run verify",
    ]:
        require(required in example_issue, f"example issue template missing {required}")
    for required in [
        "Course material",
        "Core question",
        "Evidence link",
        "Course alignment",
        "npm run course:structure:check",
    ]:
        require(required in course_issue, f"course issue template missing {required}")
    for required in [
        "Experiment record",
        "Run command",
        "Source status",
        "Result summary",
        "Candidate update",
        "npm run benchmark:summary:check",
    ]:
        require(required in experiment_issue, f"experiment issue template missing {required}")
    for required in [
        "Claim review",
        "Evidence pages",
        "Boundary",
        "Falsification path",
        "npm run claims:registry:check",
    ]:
        require(required in claim_issue, f"claim issue template missing {required}")
    for required in [
        "Anti-forgetting review",
        "Old behavior to preserve",
        "Risky update",
        "Regression guard",
        "npm run examples:test",
    ]:
        require(required in anti_forgetting_issue, f"anti-forgetting issue template missing {required}")
    for required in [
        "Source signal",
        "Runnable example",
        "Course material",
        "Experiment record",
        "Claim review",
        "Anti-forgetting review",
    ]:
        require(required in contributing, f"CONTRIBUTING missing issue template {required}")

    for required in [
        "Security and Sensitive Sources",
        "API keys",
        "Feishu/Lark",
        "X/Twitter cookies",
        ".env",
    ]:
        require(required in security, f"SECURITY.md missing {required}")


def check_templates() -> None:
    templates = {
        "templates/case-card.md": [
            "Source",
            "Environment",
            "Policy Surface",
            "Verification",
            "Course Link",
        ],
        "templates/experiment-record.md": [
            "Command",
            "Environment",
            "Result",
            "Feedback",
            "Candidate Update",
        ],
        "templates/claim-review.md": [
            "Claim",
            "Evidence",
            "Falsification Path",
            "Course Use",
            "Decision",
        ],
        "templates/anti-forgetting-checklist.md": [
            "Update Under Review",
            "Old Experience To Preserve",
            "Risky Update",
            "Regression Guard",
            "Review Result",
        ],
        "templates/reproduction-note.md": [
            "Source",
            "Research Question",
            "Reproduction Scope",
            "Commands",
            "Review Notes",
        ],
    }
    contributing = read_text("CONTRIBUTING.md")
    llms = read_text("llms.txt")
    lab2 = read_text("docs/zh-cn/slides/lab-2/index.md")
    teaching_pack = read_text("docs/zh-cn/appendix/teaching-pack.md")
    research_projects = read_text("docs/zh-cn/appendix/research-projects.md")
    exercises = read_text("docs/zh-cn/appendix/exercises.md")

    for template, headings in templates.items():
        path = ROOT / template
        require(path.exists(), f"missing template: {template}")
        text = path.read_text(encoding="utf-8")
        for heading in headings:
            require(heading in text, f"{template} missing section: {heading}")

    for required in [
        "templates/experiment-record.md",
        "templates/claim-review.md",
        "templates/reproduction-note.md",
        "templates/anti-forgetting-checklist.md",
    ]:
        require(required in contributing, f"CONTRIBUTING missing template pointer: {required}")
        require(required in llms, f"llms.txt missing template pointer: {required}")

    require("templates/claim-review.md" in teaching_pack, "teaching pack must link claim review template")
    require("templates/claim-review.md" in research_projects, "research projects must link claim review template")
    require(
        "templates/anti-forgetting-checklist.md" in lab2,
        "Lab 2 must link anti-forgetting checklist template",
    )
    require(
        "templates/anti-forgetting-checklist.md" in exercises
        or "templates/anti-forgetting-checklist.md" in research_projects,
        "course exercises or research projects must link anti-forgetting checklist template",
    )


def check_citation_metadata() -> None:
    citation = read_text("CITATION.cff")
    citation_page = read_text("docs/zh-cn/appendix/citation.md")
    license_text = read_text("LICENSE")
    readme = read_text("README.md")
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    for required in [
        "cff-version: 1.2.0",
        "Heuristic Learning: A Chinese Research and Hands-on Course",
        "https://github.com/longbiaochen/heuristic-learning",
        "CC-BY-NC-SA-4.0",
    ]:
        require(required in citation, f"CITATION.cff missing {required}")

    require(package.get("license") == "CC-BY-NC-SA-4.0", "package license must match citation metadata")
    for required in [
        "SPDX-License-Identifier: CC-BY-NC-SA-4.0",
        "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    ]:
        require(required in license_text, f"LICENSE missing {required}")
    for required in [
        "CITATION.cff",
        "LICENSE",
        "Learning Beyond Gradients",
        "轻量 replay",
        "来源登记",
    ]:
        require(required in citation_page, f"citation page missing {required}")
    require("CITATION.cff" in readme, "README must link to CITATION.cff")
    require("LICENSE" in readme, "README must link to LICENSE")
    require("SECURITY.md" in readme, "README must link to SECURITY.md")


def check_course_schedule() -> None:
    schedule = read_text("docs/zh-cn/appendix/course-schedule.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    readme = read_text("README.md")
    instructor = read_text("docs/zh-cn/appendix/instructor-guide.md")
    syllabus = read_text("docs/zh-cn/syllabus/index.md")
    slides = read_text("docs/zh-cn/slides/index.md")

    for required in [
        "6 周完整版",
        "4 周压缩版",
        "npm run verify",
        "npm run examples:gridworld:feedback",
        "npm run examples:reports:check",
        "npm run teaching:registry:check",
        "npm run docs:routes:check",
        "npm run course:structure:check",
        "研究问题",
        "SECURITY.md",
    ]:
        require(required in schedule, f"course schedule missing {required}")

    for required in [
        "course-schedule.md",
        "课程进度表",
    ]:
        require(required in readme or required in instructor or required in syllabus, f"course schedule not linked: {required}")
    for required in [
        "完成度审计",
        "npm run verify",
        "npm run docs:routes:check",
        "course-manifest.json",
        "example-registry.json",
        "claims-registry.json",
        "teaching-registry.json",
        "slide-deck.json",
        "speaker-notes.json",
        "rubric.json",
        "exercise-registry.json",
        "contribution-contract.json",
        "reproducibility-checklist.json",
        "case-registry.json",
        "concept-graph.json",
        "learning-units.json",
        "learning-outcomes.json",
        "checkpoint-registry.json",
        "teaching-pack.json",
        "research-projects.json",
        "research-logbook.json",
        "visual-verification.json",
        "visual-acceptance-log.json",
        "reproducibility-checklist.json",
        "x-sources.json",
        "benchmark-summary.json",
        "SECURITY.md",
        "官方 Browser/IAB",
        "GitHub Pages",
        "视觉与浏览器验收",
    ]:
        require(required in audit, f"completion audit missing {required}")
    for required in [
        "teaching-registry.json",
        "teaching-registry.schema.json",
        "speaker-notes.json",
        "speaker-notes.schema.json",
    ]:
        require(required in slides or required in syllabus, f"teaching registry not linked: {required}")


def check_reading_guide() -> None:
    guide = read_text("docs/zh-cn/appendix/reading-guide.md")
    references = read_text("docs/zh-cn/appendix/references.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")

    for required in [
        "Learning Beyond Gradients",
        "Trinkle23897/learning-beyond-gradients",
        "Jiayi Weng X 原帖",
        "Deep Learning",
        "Reinforcement Learning",
        "/claims-registry.json",
        "npm run claims:registry:check",
        "npm run source:registry:check",
        "npm run examples:feedback",
        "npm run examples:registry:check",
        "npm run verify",
    ]:
        require(required in guide, f"reading guide missing {required}")

    for required in [
        "reading-guide",
        "文献阅读指南",
    ]:
        require(
            required in references or required in course_map or required in appendix or required in audit,
            f"reading guide not linked: {required}",
        )



def check_case_registry() -> None:
    page = read_text("docs/zh-cn/appendix/case-registry.md")
    registry = json.loads(read_text("docs/public/case-registry.json"))
    schema = json.loads(read_text("docs/public/case-registry.schema.json"))
    cases_index = read_text("docs/zh-cn/cases/index.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/case-registry.json",
        "/case-registry.schema.json",
        "npm run cases:check",
        "Ant Gait",
        "Breakout",
        "VizDoom",
        "Robot Soccer",
        "Traffic Simulation",
        "X Public Discussion",
    ]:
        require(required in page, f"case registry page missing {required}")

    require(registry.get("$schema") == "/case-registry.schema.json", "case registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "case registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Case Registry", "case registry schema title mismatch")
    case_ids = {
        case.get("id")
        for case in registry.get("cases", [])
        if isinstance(case, dict) and isinstance(case.get("id"), str)
    }
    require(
        case_ids
        == {
            "ant-gait",
            "breakout",
            "vizdoom",
            "robot-soccer",
            "traffic-simulation",
            "x-signal",
        },
        "case registry ids mismatch",
    )

    for required in [
        "case-registry",
        "案例矩阵",
        "case-registry.json",
        "npm run cases:check",
    ]:
        require(
            required in cases_index or required in course_map or required in appendix or required in audit or required in verify,
            f"case registry not linked: {required}",
        )

    for required in [
        "示例负责动手，案例负责理解任务与证据边界",
        "公开 Artifact 案例",
        "应用场景案例",
        "来源线索案例",
        "GridWorld",
        "X 来源案例不是第六个 runnable case",
    ]:
        require(required in cases_index, f"cases index missing learner-facing organization: {required}")


def check_learning_units() -> None:
    page = read_text("docs/zh-cn/appendix/learning-units.md")
    registry = json.loads(read_text("docs/public/learning-units.json"))
    schema = json.loads(read_text("docs/public/learning-units.schema.json"))
    syllabus = read_text("docs/zh-cn/syllabus/index.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/learning-units.json",
        "/learning-units.schema.json",
        "npm run learning:units:check",
        "npm run verify",
        "先读后跑",
        "跑出失败",
        "修改有边界",
        "复盘可检查",
        "U0 建立语境",
        "U5 反遗忘项目",
    ]:
        require(required in page, f"learning units page missing {required}")

    require(registry.get("$schema") == "/learning-units.schema.json", "learning units registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "learning units registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Units Registry", "learning units schema title mismatch")
    unit_ids = {
        unit.get("id")
        for unit in registry.get("units", [])
        if isinstance(unit, dict) and isinstance(unit.get("id"), str)
    }
    require(
        unit_ids
        == {
            "u0-context",
            "u1-minimal-loop",
            "u2-public-artifacts",
            "u3-control-and-systems",
            "u4-research-claims",
            "u5-anti-forgetting-project",
        },
        "learning units registry ids mismatch",
    )

    for required in [
        "learning-units",
        "学习单元矩阵",
        "learning-units.json",
        "npm run learning:units:check",
    ]:
        require(
            required in syllabus or required in course_map or required in appendix or required in audit or required in verify,
            f"learning units not linked: {required}",
        )


def check_learning_outcomes() -> None:
    page = read_text("docs/zh-cn/appendix/learning-outcomes.md")
    registry = json.loads(read_text("docs/public/learning-outcomes.json"))
    schema = json.loads(read_text("docs/public/learning-outcomes.schema.json"))
    syllabus = read_text("docs/zh-cn/syllabus/index.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/learning-outcomes.json",
        "/learning-outcomes.schema.json",
        "npm run learning:outcomes:check",
        "解释 HL 问题边界",
        "运行并解释最小闭环",
        "把来源转成案例证据",
        "设计可维护 heuristic patch",
        "完成研究型课程交付",
    ]:
        require(required in page, f"learning outcomes page missing {required}")

    require(registry.get("$schema") == "/learning-outcomes.schema.json", "learning outcomes registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "learning outcomes registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Outcomes Registry", "learning outcomes schema title mismatch")
    outcome_ids = {
        outcome.get("id")
        for outcome in registry.get("outcomes", [])
        if isinstance(outcome, dict) and isinstance(outcome.get("id"), str)
    }
    require(outcome_ids == {"lo-1", "lo-2", "lo-3", "lo-4", "lo-5"}, "learning outcomes ids mismatch")

    for required in [
        "learning-outcomes",
        "学习成果矩阵",
        "learning-outcomes.json",
        "npm run learning:outcomes:check",
    ]:
        require(
            required in syllabus or required in course_map or required in appendix or required in audit or required in verify,
            f"learning outcomes not linked: {required}",
        )


def check_checkpoints() -> None:
    page = read_text("docs/zh-cn/appendix/checkpoints.md")
    registry = json.loads(read_text("docs/public/checkpoint-registry.json"))
    schema = json.loads(read_text("docs/public/checkpoint-registry.schema.json"))
    syllabus = read_text("docs/zh-cn/syllabus/index.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/checkpoint-registry.json",
        "/checkpoint-registry.schema.json",
        "npm run checkpoints:check",
        "建立语境自测",
        "最小闭环自测",
        "公开来源自测",
        "系统控制自测",
        "研究问题自测",
        "反遗忘项目自测",
    ]:
        require(required in page, f"checkpoint page missing {required}")

    require(registry.get("$schema") == "/checkpoint-registry.schema.json", "checkpoint registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "checkpoint registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Checkpoint Registry", "checkpoint schema title mismatch")
    checkpoint_ids = {
        checkpoint.get("id")
        for checkpoint in registry.get("checkpoints", [])
        if isinstance(checkpoint, dict) and isinstance(checkpoint.get("id"), str)
    }
    require(
        checkpoint_ids == {"cp-0", "cp-1", "cp-2", "cp-3", "cp-4", "cp-5"},
        "checkpoint ids mismatch",
    )

    for required in [
        "checkpoint-registry",
        "阶段检查点",
        "checkpoint-registry.json",
        "npm run checkpoints:check",
    ]:
        require(
            required in syllabus or required in course_map or required in appendix or required in audit or required in verify,
            f"checkpoint registry not linked: {required}",
        )


def check_evaluation_metrics() -> None:
    page = read_text("docs/zh-cn/appendix/evaluation-metrics.md")
    registry = json.loads(read_text("docs/public/evaluation-metrics.json"))
    schema = json.loads(read_text("docs/public/evaluation-metrics.schema.json"))
    framework = read_text("docs/zh-cn/theory/research-framework.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/evaluation-metrics.json",
        "/evaluation-metrics.schema.json",
        "npm run metrics:check",
        "任务结果",
        "失败隔离",
        "更新成本",
        "回归风险",
        "来源边界",
    ]:
        require(required in page, f"evaluation metrics page missing {required}")

    require(registry.get("$schema") == "/evaluation-metrics.schema.json", "evaluation metrics schema pointer mismatch")
    require(registry.get("schema_version") == 1, "evaluation metrics schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Evaluation Metrics Registry", "evaluation metrics schema title mismatch")
    metric_ids = {
        metric.get("id")
        for metric in registry.get("metrics", [])
        if isinstance(metric, dict) and isinstance(metric.get("id"), str)
    }
    require(
        metric_ids
        == {
            "task-outcome",
            "failure-isolation",
            "update-cost",
            "regression-risk",
            "source-boundary",
        },
        "evaluation metric ids mismatch",
    )

    for required in [
        "evaluation-metrics",
        "评估指标矩阵",
        "evaluation-metrics.json",
        "npm run metrics:check",
    ]:
        require(
            required in framework
            or required in course_map
            or required in appendix
            or required in audit
            or required in verify,
            f"evaluation metrics not linked: {required}",
        )


def check_paper_blueprint() -> None:
    page = read_text("docs/zh-cn/appendix/paper-blueprint.md")
    registry = json.loads(read_text("docs/public/paper-blueprint.json"))
    schema = json.loads(read_text("docs/public/paper-blueprint.schema.json"))
    reading_guide = read_text("docs/zh-cn/appendix/reading-guide.md")
    roadmap = read_text("docs/zh-cn/appendix/research-roadmap.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/paper-blueprint.json",
        "/paper-blueprint.schema.json",
        "npm run paper:blueprint:check",
        "摘要与定位",
        "问题定义与相关工作",
        "方法：学习闭环",
        "实验与结果",
        "讨论、局限与威胁",
        "教学使用与复现材料",
    ]:
        require(required in page, f"paper blueprint page missing {required}")

    require(registry.get("$schema") == "/paper-blueprint.schema.json", "paper blueprint schema pointer mismatch")
    require(registry.get("schema_version") == 1, "paper blueprint schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Paper Blueprint Registry", "paper blueprint schema title mismatch")
    section_ids = {
        section.get("id")
        for section in registry.get("sections", [])
        if isinstance(section, dict) and isinstance(section.get("id"), str)
    }
    require(
        section_ids
        == {
            "abstract-and-positioning",
            "problem-and-related-work",
            "method-learning-loop",
            "experiments-and-results",
            "discussion-and-threats",
            "course-and-reuse",
        },
        "paper blueprint ids mismatch",
    )

    for required in [
        "paper-blueprint",
        "论文蓝图",
        "paper-blueprint.json",
        "npm run paper:blueprint:check",
    ]:
        require(
            required in reading_guide
            or required in roadmap
            or required in appendix
            or required in audit
            or required in verify,
            f"paper blueprint not linked: {required}",
        )


def check_ablation_plan() -> None:
    page = read_text("docs/zh-cn/appendix/ablation-plan.md")
    registry = json.loads(read_text("docs/public/ablation-plan.json"))
    schema = json.loads(read_text("docs/public/ablation-plan.schema.json"))
    benchmark_protocol = read_text("docs/zh-cn/appendix/benchmark-protocol.md")
    benchmark_results = read_text("docs/zh-cn/appendix/benchmark-results.md")
    paper_blueprint = read_text("docs/zh-cn/appendix/paper-blueprint.md")
    research_projects = read_text("docs/zh-cn/appendix/research-projects.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/ablation-plan.json",
        "/ablation-plan.schema.json",
        "npm run ablation:plan:check",
        "GridWorld 陷阱规避消融",
        "Robot Soccer 射门通道消融",
        "VizDoom Medikit 阈值消融",
        "Traffic Grid 下游容量消融",
        "Breakout 反射预测消融",
        "Ant Gait 偏航反馈消融",
    ]:
        require(required in page, f"ablation plan page missing {required}")

    require(registry.get("$schema") == "/ablation-plan.schema.json", "ablation plan schema pointer mismatch")
    require(registry.get("schema_version") == 1, "ablation plan schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Ablation Plan Registry", "ablation plan schema title mismatch")
    ablation_ids = {
        ablation.get("id")
        for ablation in registry.get("ablations", [])
        if isinstance(ablation, dict) and isinstance(ablation.get("id"), str)
    }
    require(
        ablation_ids
        == {
            "gridworld-trap-avoidance",
            "robot-soccer-shot-lane",
            "vizdoom-medikit-threshold",
            "traffic-downstream-capacity",
            "breakout-reflection-prediction",
            "ant-gait-yaw-feedback",
        },
        "ablation plan ids mismatch",
    )

    for required in [
        "ablation-plan",
        "消融计划",
        "ablation-plan.json",
        "npm run ablation:plan:check",
    ]:
        require(
            required in benchmark_protocol
            or required in benchmark_results
            or required in paper_blueprint
            or required in research_projects
            or required in appendix
            or required in audit
            or required in verify,
            f"ablation plan not linked: {required}",
        )


def check_concept_graph() -> None:
    page = read_text("docs/zh-cn/appendix/concept-graph.md")
    registry = json.loads(read_text("docs/public/concept-graph.json"))
    schema = json.loads(read_text("docs/public/concept-graph.schema.json"))
    glossary = read_text("docs/zh-cn/appendix/glossary.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/concept-graph.json",
        "/concept-graph.schema.json",
        "npm run concept:graph:check",
        "Heuristic Learning",
        "Signal",
        "Probe",
        "Baseline",
        "Feedback report",
        "Regression",
    ]:
        require(required in page, f"concept graph page missing {required}")

    require(registry.get("$schema") == "/concept-graph.schema.json", "concept graph registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "concept graph registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Concept Graph", "concept graph schema title mismatch")
    concept_ids = {
        concept.get("id")
        for concept in registry.get("concepts", [])
        if isinstance(concept, dict) and isinstance(concept.get("id"), str)
    }
    require(
        concept_ids
        == {
            "heuristic-learning",
            "signal",
            "probe",
            "baseline",
            "heuristic-patch",
            "feedback-report",
            "regression",
            "source-status",
        },
        "concept graph registry ids mismatch",
    )

    for required in [
        "concept-graph",
        "概念图谱",
        "concept-graph.json",
        "npm run concept:graph:check",
    ]:
        require(
            required in glossary
            or required in course_map
            or required in appendix
            or required in audit
            or required in verify,
            f"concept graph not linked: {required}",
        )


def check_exercise_registry() -> None:
    page = read_text("docs/zh-cn/appendix/exercises.md")
    registry = json.loads(read_text("docs/public/exercise-registry.json"))
    schema = json.loads(read_text("docs/public/exercise-registry.schema.json"))
    course_map = read_text("docs/zh-cn/course-map/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/exercise-registry.json",
        "/exercise-registry.schema.json",
        "npm run exercises:check",
        "A1. 定义 HL",
        "B1. GridWorld 新陷阱",
        "C3. Report 是否足够给下一轮智能体使用",
        "D5. 课程讲义扩展",
    ]:
        require(required in page, f"exercise page missing {required}")

    require(registry.get("$schema") == "/exercise-registry.schema.json", "exercise registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "exercise registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Exercise Registry", "exercise registry schema title mismatch")
    set_ids = {
        exercise_set.get("id")
        for exercise_set in registry.get("exercise_sets", [])
        if isinstance(exercise_set, dict) and isinstance(exercise_set.get("id"), str)
    }
    require(
        set_ids
        == {
            "concept-exercises",
            "code-exercises",
            "experiment-exercises",
            "capstone-exercises",
        },
        "exercise registry set ids mismatch",
    )

    for required in [
        "exercise-registry",
        "练习集",
        "exercise-registry.json",
        "npm run exercises:check",
    ]:
        require(
            required in course_map or required in appendix or required in audit or required in verify,
            f"exercise registry not linked: {required}",
        )


def check_contribution_contract() -> None:
    protocol = read_text("docs/zh-cn/appendix/contribution-protocol.md")
    registry = json.loads(read_text("docs/public/contribution-contract.json"))
    schema = json.loads(read_text("docs/public/contribution-contract.schema.json"))
    contributing = read_text("CONTRIBUTING.md")
    pr_template = read_text(".github/pull_request_template.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/contribution-contract.json",
        "/contribution-contract.schema.json",
        "npm run contribution:contract:check",
        "CONTRIBUTING.md",
        ".github/pull_request_template.md",
        "来源、失败模式、运行命令、反馈报告、测试路径",
    ]:
        require(required in protocol, f"contribution protocol missing {required}")

    require(registry.get("$schema") == "/contribution-contract.schema.json", "contribution contract schema pointer mismatch")
    require(registry.get("schema_version") == 1, "contribution contract schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Contribution Contract", "contribution contract schema title mismatch")
    type_ids = {
        item.get("id")
        for item in registry.get("contribution_types", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    require(
        type_ids
        == {
            "theory-page",
            "case-card",
            "runnable-example",
            "experiment-record",
            "claim-review",
            "reproduction-note",
            "anti-forgetting-review",
            "course-material",
        },
        "contribution contract type ids mismatch",
    )

    for required in [
        "contribution-contract",
        "贡献与研究协议",
        "contribution-contract.json",
        "npm run contribution:contract:check",
    ]:
        require(
            required in contributing
            or required in pr_template
            or required in appendix
            or required in audit
            or required in verify,
            f"contribution contract not linked: {required}",
        )


def check_reproducibility() -> None:
    page = read_text("docs/zh-cn/appendix/reproducibility.md")
    registry = json.loads(read_text("docs/public/reproducibility-checklist.json"))
    schema = json.loads(read_text("docs/public/reproducibility-checklist.schema.json"))
    appendix = read_text("docs/zh-cn/appendix/index.md")
    course_map = read_text("docs/zh-cn/course-map/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/reproducibility-checklist.json",
        "/reproducibility-checklist.schema.json",
        "npm run reproducibility:check",
        "环境与安装",
        "可运行示例",
        "研究问题与来源",
        "教学产物",
        "贡献与发布",
        "站点与机器入口",
    ]:
        require(required in page, f"reproducibility page missing {required}")

    require(
        registry.get("$schema") == "/reproducibility-checklist.schema.json",
        "reproducibility registry schema pointer mismatch",
    )
    require(registry.get("schema_version") == 1, "reproducibility registry schema_version must be 1")
    require(
        schema.get("title") == "Heuristic Learning Reproducibility Checklist",
        "reproducibility schema title mismatch",
    )
    checklist_ids = {
        item.get("id")
        for item in registry.get("checklists", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    require(
        checklist_ids
        == {
            "environment-and-install",
            "runnable-examples",
            "claims-and-sources",
            "teaching-artifacts",
            "contribution-and-release",
            "site-and-machine-entrypoints",
        },
        "reproducibility checklist ids mismatch",
    )

    for required in [
        "reproducibility-checklist",
        "可复现性检查清单",
        "reproducibility-checklist.json",
        "npm run reproducibility:check",
    ]:
        require(
            required in appendix or required in course_map or required in audit or required in verify,
            f"reproducibility checklist not linked: {required}",
        )


def check_teaching_pack() -> None:
    page = read_text("docs/zh-cn/appendix/teaching-pack.md")
    registry = json.loads(read_text("docs/public/teaching-pack.json"))
    schema = json.loads(read_text("docs/public/teaching-pack.schema.json"))
    instructor = read_text("docs/zh-cn/appendix/instructor-guide.md")
    schedule = read_text("docs/zh-cn/appendix/course-schedule.md")
    slides = read_text("docs/zh-cn/slides/index.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    for required in [
        "/teaching-pack.json",
        "/teaching-pack.schema.json",
        "npm run teaching:pack:check",
        "npm run verify",
        "TP0 快速导读",
        "TP1 工作坊",
        "TP2 研究讨论",
        "TP3 期末项目",
        "Exit ticket",
        "课前总检查",
    ]:
        require(required in page, f"teaching pack page missing {required}")

    require(registry.get("$schema") == "/teaching-pack.schema.json", "teaching pack registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "teaching pack registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Teaching Pack Registry", "teaching pack schema title mismatch")
    pack_ids = {
        pack.get("id")
        for pack in registry.get("packs", [])
        if isinstance(pack, dict) and isinstance(pack.get("id"), str)
    }
    require(
        pack_ids
        == {
            "tp0-quick-orientation",
            "tp1-hands-on-workshop",
            "tp2-research-seminar",
            "tp3-project-course",
        },
        "teaching pack registry ids mismatch",
    )

    for required in [
        "teaching-pack",
        "授课包",
        "teaching-pack.json",
        "npm run teaching:pack:check",
    ]:
        require(
            required in instructor
            or required in schedule
            or required in slides
            or required in appendix
            or required in audit
            or required in verify,
            f"teaching pack not linked: {required}",
        )


def check_x_sources() -> None:
    registry = json.loads(read_text("docs/public/x-sources.json"))
    schema = json.loads(read_text("docs/public/x-sources.schema.json"))
    x_case = read_text("docs/zh-cn/cases/x-signal/index.md")
    source_registry = read_text("docs/zh-cn/appendix/source-registry.md")
    appendix = read_text("docs/zh-cn/appendix/index.md")
    audit = read_text("docs/zh-cn/appendix/completion-audit.md")
    verify = read_text("scripts/verify.sh")

    require(registry.get("$schema") == "/x-sources.schema.json", "x sources registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "x sources registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning X Sources Registry", "x sources schema title mismatch")
    source_policy = registry.get("source_policy")
    require(isinstance(source_policy, dict), "x sources must document reader-facing source policy")
    sources = registry.get("sources")
    require(isinstance(sources, list), "x sources registry sources must be a list")
    source_ids = {
        source.get("id")
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }
    require(
        source_ids
        == {
            "logicrw-jiayi-hl-summary-2026-05-08",
            "jiayi-original-hl-post-2026-05-08",
            "logicrw-fluid-control-lead-2026-05-19",
        },
        "x sources registry ids mismatch",
    )
    for required in [
        "/x-sources.json",
        "/x-sources.schema.json",
        "npm run x:sources:check",
        "待直接复核",
        "待采集",
        "2052596837547495549",
    ]:
        require(
            required in x_case
            or required in source_registry
            or required in appendix
            or required in audit
            or required in verify,
            f"x sources not linked: {required}",
        )


def check_source_to_case_playbook() -> None:
    registry = json.loads(read_text("docs/public/source-to-case-playbook.json"))
    schema = json.loads(read_text("docs/public/source-to-case-playbook.schema.json"))
    page = read_text("docs/zh-cn/appendix/source-to-case-playbook.md")
    x_case = read_text("docs/zh-cn/cases/x-signal/index.md")
    source_registry = read_text("docs/zh-cn/appendix/source-registry.md")
    exercises = read_text("docs/zh-cn/appendix/exercises.md")
    verify = read_text("scripts/verify.sh")

    require(registry.get("$schema") == "/source-to-case-playbook.schema.json", "source-to-case registry schema pointer mismatch")
    require(registry.get("schema_version") == 1, "source-to-case registry schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Source-to-Case Playbook", "source-to-case schema title mismatch")
    workflows = registry.get("workflows")
    require(isinstance(workflows, list), "source-to-case workflows must be a list")
    workflow_ids = {
        workflow.get("id")
        for workflow in workflows
        if isinstance(workflow, dict) and isinstance(workflow.get("id"), str)
    }
    require(
        workflow_ids
        == {
            "x-thread-to-case-card",
            "public-artifact-to-replay",
            "internal-signal-to-minimal-env",
            "hypothesis-to-research-project",
        },
        "source-to-case workflow ids mismatch",
    )
    for required in [
        "/source-to-case-playbook.json",
        "/source-to-case-playbook.schema.json",
        "npm run source:case:check",
        "templates/case-card.md",
        "待直接复核",
        "X / public discussion",
        "Public code artifact",
        "Sanitized operational problem",
        "Research hypothesis",
    ]:
        require(
            required in page
            or required in x_case
            or required in source_registry
            or required in exercises
            or required in verify,
            f"source-to-case playbook not linked: {required}",
        )


def check_release_metadata() -> None:
    changelog = read_text("CHANGELOG.md")
    release_page = read_text("docs/zh-cn/appendix/release-checklist.md")
    deployment = read_text("docs/DEPLOYMENT.md")
    readme = read_text("README.md")

    for required in [
        "## [0.1.0] - 2026-05-24",
        "npm run verify",
        "Source Boundary",
        "learning-beyond-gradients",
    ]:
        require(required in changelog, f"CHANGELOG missing {required}")

    for required in [
        "CHANGELOG.md",
        "npm run verify",
        "course-manifest.json",
        "code-tour.json",
        "benchmark-summary.json",
        "ablation-plan.json",
        "artifact-gap-analysis.json",
        "troubleshooting-tree.json",
        "source-to-case-playbook.json",
        "x-sources.json",
        "npm run benchmark:summary:check",
        "npm run code:tour:check",
        "npm run ablation:plan:check",
        "npm run artifact:gap:check",
        "npm run troubleshooting:tree:check",
        "npm run source:case:check",
        "npm run x:sources:check",
        "npm run cases:check",
        "npm run slides:check",
        "npm run speaker:notes:check",
        "npm run rubric:check",
        "npm run exercises:check",
        "npm run contribution:contract:check",
        "npm run concept:graph:check",
        "npm run learning:units:check",
        "npm run learning:outcomes:check",
        "npm run checkpoints:check",
        "npm run teaching:pack:check",
        "npm run research:projects:check",
        "npm run completion:audit:check",
        "npm run release:readiness:check",
        "CITATION.cff",
        "LICENSE",
        "SECURITY.md",
    ]:
        require(required in release_page, f"release checklist missing {required}")

    require("release-checklist.md" in deployment, "DEPLOYMENT must link to release checklist")
    for required in [
        "benchmark summary",
        "ablation plan",
        "artifact gap analysis",
        "troubleshooting tree",
        "source-to-case playbook",
        "X source registry",
        "case registry",
        "slide deck structure",
        "speaker notes",
        "rubric",
        "concept graph",
        "learning units",
        "learning outcomes",
        "checkpoints",
        "evaluation metrics",
        "teaching packs",
        "research projects",
        "release readiness",
    ]:
        require(required in deployment, f"DEPLOYMENT missing {required}")
    require("CHANGELOG.md" in readme, "README must link to CHANGELOG")


def check_workspace_hygiene() -> None:
    gitignore = read_text(".gitignore")
    local_setup = read_text("docs/zh-cn/appendix/local-setup.md")
    for required in [
        "node_modules/",
        "__pycache__/",
        "*.py[cod]",
        "docs/.vitepress/dist/",
        "docs/.vitepress/cache/",
        ".env",
        "!.env.example",
    ]:
        require(required in gitignore, f".gitignore missing {required}")

    for generated in [
        "docs/.vitepress/dist",
        "docs/.vitepress/cache",
    ]:
        require(not (ROOT / generated).exists(), f"generated artifact should not be present: {generated}")

    for required in [
        "docs/.vitepress/dist",
        "__pycache__",
        "npm run course:structure:check",
        "npm run troubleshooting:tree:check",
    ]:
        require(required in local_setup, f"local setup missing hygiene note: {required}")


def check_course_manifest() -> None:
    manifest_path = ROOT / "docs/public/course-manifest.json"
    schema_path = ROOT / "docs/public/course-manifest.schema.json"
    example_registry_path = ROOT / "docs/public/example-registry.json"
    example_registry_schema_path = ROOT / "docs/public/example-registry.schema.json"
    code_tour_path = ROOT / "docs/public/code-tour.json"
    code_tour_schema_path = ROOT / "docs/public/code-tour.schema.json"
    benchmark_summary_path = ROOT / "docs/public/benchmark-summary.json"
    benchmark_summary_schema_path = ROOT / "docs/public/benchmark-summary.schema.json"
    ablation_plan_path = ROOT / "docs/public/ablation-plan.json"
    ablation_plan_schema_path = ROOT / "docs/public/ablation-plan.schema.json"
    artifact_gap_path = ROOT / "docs/public/artifact-gap-analysis.json"
    artifact_gap_schema_path = ROOT / "docs/public/artifact-gap-analysis.schema.json"
    troubleshooting_tree_path = ROOT / "docs/public/troubleshooting-tree.json"
    troubleshooting_tree_schema_path = ROOT / "docs/public/troubleshooting-tree.schema.json"
    claims_registry_path = ROOT / "docs/public/claims-registry.json"
    claims_registry_schema_path = ROOT / "docs/public/claims-registry.schema.json"
    case_registry_path = ROOT / "docs/public/case-registry.json"
    case_registry_schema_path = ROOT / "docs/public/case-registry.schema.json"
    teaching_registry_path = ROOT / "docs/public/teaching-registry.json"
    teaching_registry_schema_path = ROOT / "docs/public/teaching-registry.schema.json"
    slide_deck_path = ROOT / "docs/public/slide-deck.json"
    slide_deck_schema_path = ROOT / "docs/public/slide-deck.schema.json"
    speaker_notes_path = ROOT / "docs/public/speaker-notes.json"
    speaker_notes_schema_path = ROOT / "docs/public/speaker-notes.schema.json"
    rubric_path = ROOT / "docs/public/rubric.json"
    rubric_schema_path = ROOT / "docs/public/rubric.schema.json"
    exercise_registry_path = ROOT / "docs/public/exercise-registry.json"
    exercise_registry_schema_path = ROOT / "docs/public/exercise-registry.schema.json"
    contribution_contract_path = ROOT / "docs/public/contribution-contract.json"
    contribution_contract_schema_path = ROOT / "docs/public/contribution-contract.schema.json"
    reproducibility_path = ROOT / "docs/public/reproducibility-checklist.json"
    reproducibility_schema_path = ROOT / "docs/public/reproducibility-checklist.schema.json"
    learning_units_path = ROOT / "docs/public/learning-units.json"
    learning_units_schema_path = ROOT / "docs/public/learning-units.schema.json"
    learning_outcomes_path = ROOT / "docs/public/learning-outcomes.json"
    learning_outcomes_schema_path = ROOT / "docs/public/learning-outcomes.schema.json"
    checkpoint_registry_path = ROOT / "docs/public/checkpoint-registry.json"
    checkpoint_registry_schema_path = ROOT / "docs/public/checkpoint-registry.schema.json"
    evaluation_metrics_path = ROOT / "docs/public/evaluation-metrics.json"
    evaluation_metrics_schema_path = ROOT / "docs/public/evaluation-metrics.schema.json"
    paper_blueprint_path = ROOT / "docs/public/paper-blueprint.json"
    paper_blueprint_schema_path = ROOT / "docs/public/paper-blueprint.schema.json"
    concept_graph_path = ROOT / "docs/public/concept-graph.json"
    concept_graph_schema_path = ROOT / "docs/public/concept-graph.schema.json"
    teaching_pack_path = ROOT / "docs/public/teaching-pack.json"
    teaching_pack_schema_path = ROOT / "docs/public/teaching-pack.schema.json"
    research_projects_path = ROOT / "docs/public/research-projects.json"
    research_projects_schema_path = ROOT / "docs/public/research-projects.schema.json"
    research_logbook_path = ROOT / "docs/public/research-logbook.json"
    research_logbook_schema_path = ROOT / "docs/public/research-logbook.schema.json"
    completion_audit_path = ROOT / "docs/public/completion-audit.json"
    completion_audit_schema_path = ROOT / "docs/public/completion-audit.schema.json"
    visual_verification_path = ROOT / "docs/public/visual-verification.json"
    visual_verification_schema_path = ROOT / "docs/public/visual-verification.schema.json"
    visual_acceptance_log_path = ROOT / "docs/public/visual-acceptance-log.json"
    visual_acceptance_log_schema_path = ROOT / "docs/public/visual-acceptance-log.schema.json"
    x_sources_path = ROOT / "docs/public/x-sources.json"
    x_sources_schema_path = ROOT / "docs/public/x-sources.schema.json"
    source_to_case_path = ROOT / "docs/public/source-to-case-playbook.json"
    source_to_case_schema_path = ROOT / "docs/public/source-to-case-playbook.schema.json"
    require(manifest_path.exists(), "missing course manifest")
    require(schema_path.exists(), "missing course manifest schema")
    require(example_registry_path.exists(), "missing example registry")
    require(example_registry_schema_path.exists(), "missing example registry schema")
    require(code_tour_path.exists(), "missing code tour registry")
    require(code_tour_schema_path.exists(), "missing code tour schema")
    require(benchmark_summary_path.exists(), "missing benchmark summary")
    require(benchmark_summary_schema_path.exists(), "missing benchmark summary schema")
    require(ablation_plan_path.exists(), "missing ablation plan")
    require(ablation_plan_schema_path.exists(), "missing ablation plan schema")
    require(artifact_gap_path.exists(), "missing artifact gap analysis")
    require(artifact_gap_schema_path.exists(), "missing artifact gap analysis schema")
    require(troubleshooting_tree_path.exists(), "missing troubleshooting tree registry")
    require(troubleshooting_tree_schema_path.exists(), "missing troubleshooting tree schema")
    require(claims_registry_path.exists(), "missing claims registry")
    require(claims_registry_schema_path.exists(), "missing claims registry schema")
    require(case_registry_path.exists(), "missing case registry")
    require(case_registry_schema_path.exists(), "missing case registry schema")
    require(teaching_registry_path.exists(), "missing teaching registry")
    require(teaching_registry_schema_path.exists(), "missing teaching registry schema")
    require(slide_deck_path.exists(), "missing slide deck registry")
    require(slide_deck_schema_path.exists(), "missing slide deck schema")
    require(speaker_notes_path.exists(), "missing speaker notes registry")
    require(speaker_notes_schema_path.exists(), "missing speaker notes schema")
    require(rubric_path.exists(), "missing rubric registry")
    require(rubric_schema_path.exists(), "missing rubric schema")
    require(exercise_registry_path.exists(), "missing exercise registry")
    require(exercise_registry_schema_path.exists(), "missing exercise registry schema")
    require(contribution_contract_path.exists(), "missing contribution contract")
    require(contribution_contract_schema_path.exists(), "missing contribution contract schema")
    require(reproducibility_path.exists(), "missing reproducibility checklist")
    require(reproducibility_schema_path.exists(), "missing reproducibility schema")
    require(learning_units_path.exists(), "missing learning units registry")
    require(learning_units_schema_path.exists(), "missing learning units schema")
    require(learning_outcomes_path.exists(), "missing learning outcomes registry")
    require(learning_outcomes_schema_path.exists(), "missing learning outcomes schema")
    require(checkpoint_registry_path.exists(), "missing checkpoint registry")
    require(checkpoint_registry_schema_path.exists(), "missing checkpoint registry schema")
    require(evaluation_metrics_path.exists(), "missing evaluation metrics registry")
    require(evaluation_metrics_schema_path.exists(), "missing evaluation metrics schema")
    require(paper_blueprint_path.exists(), "missing paper blueprint registry")
    require(paper_blueprint_schema_path.exists(), "missing paper blueprint schema")
    require(concept_graph_path.exists(), "missing concept graph registry")
    require(concept_graph_schema_path.exists(), "missing concept graph schema")
    require(teaching_pack_path.exists(), "missing teaching pack registry")
    require(teaching_pack_schema_path.exists(), "missing teaching pack schema")
    require(research_projects_path.exists(), "missing research projects registry")
    require(research_projects_schema_path.exists(), "missing research projects schema")
    require(research_logbook_path.exists(), "missing research logbook")
    require(research_logbook_schema_path.exists(), "missing research logbook schema")
    require(completion_audit_path.exists(), "missing completion audit registry")
    require(completion_audit_schema_path.exists(), "missing completion audit schema")
    require(visual_verification_path.exists(), "missing visual verification registry")
    require(visual_verification_schema_path.exists(), "missing visual verification schema")
    require(visual_acceptance_log_path.exists(), "missing visual acceptance log")
    require(visual_acceptance_log_schema_path.exists(), "missing visual acceptance log schema")
    require(x_sources_path.exists(), "missing x sources registry")
    require(x_sources_schema_path.exists(), "missing x sources schema")
    require(source_to_case_path.exists(), "missing source-to-case playbook")
    require(source_to_case_schema_path.exists(), "missing source-to-case playbook schema")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example_registry = json.loads(example_registry_path.read_text(encoding="utf-8"))
    example_registry_schema = json.loads(example_registry_schema_path.read_text(encoding="utf-8"))
    code_tour = json.loads(code_tour_path.read_text(encoding="utf-8"))
    code_tour_schema = json.loads(code_tour_schema_path.read_text(encoding="utf-8"))
    benchmark_summary = json.loads(benchmark_summary_path.read_text(encoding="utf-8"))
    benchmark_summary_schema = json.loads(benchmark_summary_schema_path.read_text(encoding="utf-8"))
    ablation_plan = json.loads(ablation_plan_path.read_text(encoding="utf-8"))
    ablation_plan_schema = json.loads(ablation_plan_schema_path.read_text(encoding="utf-8"))
    artifact_gap = json.loads(artifact_gap_path.read_text(encoding="utf-8"))
    artifact_gap_schema = json.loads(artifact_gap_schema_path.read_text(encoding="utf-8"))
    troubleshooting_tree = json.loads(troubleshooting_tree_path.read_text(encoding="utf-8"))
    troubleshooting_tree_schema = json.loads(troubleshooting_tree_schema_path.read_text(encoding="utf-8"))
    claims_registry = json.loads(claims_registry_path.read_text(encoding="utf-8"))
    claims_registry_schema = json.loads(claims_registry_schema_path.read_text(encoding="utf-8"))
    case_registry = json.loads(case_registry_path.read_text(encoding="utf-8"))
    case_registry_schema = json.loads(case_registry_schema_path.read_text(encoding="utf-8"))
    teaching_registry = json.loads(teaching_registry_path.read_text(encoding="utf-8"))
    teaching_registry_schema = json.loads(teaching_registry_schema_path.read_text(encoding="utf-8"))
    slide_deck = json.loads(slide_deck_path.read_text(encoding="utf-8"))
    slide_deck_schema = json.loads(slide_deck_schema_path.read_text(encoding="utf-8"))
    speaker_notes = json.loads(speaker_notes_path.read_text(encoding="utf-8"))
    speaker_notes_schema = json.loads(speaker_notes_schema_path.read_text(encoding="utf-8"))
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    rubric_schema = json.loads(rubric_schema_path.read_text(encoding="utf-8"))
    exercise_registry = json.loads(exercise_registry_path.read_text(encoding="utf-8"))
    exercise_registry_schema = json.loads(exercise_registry_schema_path.read_text(encoding="utf-8"))
    contribution_contract = json.loads(contribution_contract_path.read_text(encoding="utf-8"))
    contribution_contract_schema = json.loads(contribution_contract_schema_path.read_text(encoding="utf-8"))
    reproducibility = json.loads(reproducibility_path.read_text(encoding="utf-8"))
    reproducibility_schema = json.loads(reproducibility_schema_path.read_text(encoding="utf-8"))
    learning_units = json.loads(learning_units_path.read_text(encoding="utf-8"))
    learning_units_schema = json.loads(learning_units_schema_path.read_text(encoding="utf-8"))
    learning_outcomes = json.loads(learning_outcomes_path.read_text(encoding="utf-8"))
    learning_outcomes_schema = json.loads(learning_outcomes_schema_path.read_text(encoding="utf-8"))
    checkpoint_registry = json.loads(checkpoint_registry_path.read_text(encoding="utf-8"))
    checkpoint_registry_schema = json.loads(checkpoint_registry_schema_path.read_text(encoding="utf-8"))
    evaluation_metrics = json.loads(evaluation_metrics_path.read_text(encoding="utf-8"))
    evaluation_metrics_schema = json.loads(evaluation_metrics_schema_path.read_text(encoding="utf-8"))
    paper_blueprint = json.loads(paper_blueprint_path.read_text(encoding="utf-8"))
    paper_blueprint_schema = json.loads(paper_blueprint_schema_path.read_text(encoding="utf-8"))
    concept_graph = json.loads(concept_graph_path.read_text(encoding="utf-8"))
    concept_graph_schema = json.loads(concept_graph_schema_path.read_text(encoding="utf-8"))
    teaching_pack = json.loads(teaching_pack_path.read_text(encoding="utf-8"))
    teaching_pack_schema = json.loads(teaching_pack_schema_path.read_text(encoding="utf-8"))
    research_projects = json.loads(research_projects_path.read_text(encoding="utf-8"))
    research_projects_schema = json.loads(research_projects_schema_path.read_text(encoding="utf-8"))
    research_logbook = json.loads(research_logbook_path.read_text(encoding="utf-8"))
    research_logbook_schema = json.loads(research_logbook_schema_path.read_text(encoding="utf-8"))
    completion_audit = json.loads(completion_audit_path.read_text(encoding="utf-8"))
    completion_audit_schema = json.loads(completion_audit_schema_path.read_text(encoding="utf-8"))
    visual_verification = json.loads(visual_verification_path.read_text(encoding="utf-8"))
    visual_verification_schema = json.loads(visual_verification_schema_path.read_text(encoding="utf-8"))
    visual_acceptance_log = json.loads(visual_acceptance_log_path.read_text(encoding="utf-8"))
    visual_acceptance_log_schema = json.loads(visual_acceptance_log_schema_path.read_text(encoding="utf-8"))
    x_sources = json.loads(x_sources_path.read_text(encoding="utf-8"))
    x_sources_schema = json.loads(x_sources_schema_path.read_text(encoding="utf-8"))
    source_to_case = json.loads(source_to_case_path.read_text(encoding="utf-8"))
    source_to_case_schema = json.loads(source_to_case_schema_path.read_text(encoding="utf-8"))

    require(manifest.get("$schema") == "/course-manifest.schema.json", "course manifest schema pointer mismatch")
    require(manifest.get("schema_version") == 1, "course manifest schema_version must be 1")
    require(schema.get("title") == "Heuristic Learning Course Manifest", "course manifest schema title mismatch")
    require("examples" in schema.get("properties", {}), "course manifest schema must describe examples")
    require("public_resources" in schema.get("properties", {}), "course manifest schema must describe public_resources")
    require(example_registry.get("$schema") == "/example-registry.schema.json", "example registry schema pointer mismatch")
    require(example_registry.get("schema_version") == 1, "example registry schema_version must be 1")
    require(
        example_registry_schema.get("title") == "Heuristic Learning Example Registry",
        "example registry schema title mismatch",
    )
    require(code_tour.get("$schema") == "/code-tour.schema.json", "code tour schema pointer mismatch")
    require(code_tour.get("schema_version") == 1, "code tour schema_version must be 1")
    require(
        code_tour_schema.get("title") == "Heuristic Learning Code Tour Registry",
        "code tour schema title mismatch",
    )
    require(benchmark_summary.get("$schema") == "/benchmark-summary.schema.json", "benchmark summary schema pointer mismatch")
    require(benchmark_summary.get("schema_version") == 1, "benchmark summary schema_version must be 1")
    require(
        benchmark_summary_schema.get("title") == "Heuristic Learning Benchmark Summary",
        "benchmark summary schema title mismatch",
    )
    require(ablation_plan.get("$schema") == "/ablation-plan.schema.json", "ablation plan schema pointer mismatch")
    require(ablation_plan.get("schema_version") == 1, "ablation plan schema_version must be 1")
    require(
        ablation_plan_schema.get("title") == "Heuristic Learning Ablation Plan Registry",
        "ablation plan schema title mismatch",
    )
    require(artifact_gap.get("$schema") == "/artifact-gap-analysis.schema.json", "artifact gap schema pointer mismatch")
    require(artifact_gap.get("schema_version") == 1, "artifact gap schema_version must be 1")
    require(
        artifact_gap_schema.get("title") == "Heuristic Learning Artifact Gap Analysis",
        "artifact gap schema title mismatch",
    )
    require(troubleshooting_tree.get("$schema") == "/troubleshooting-tree.schema.json", "troubleshooting tree schema pointer mismatch")
    require(troubleshooting_tree.get("schema_version") == 1, "troubleshooting tree schema_version must be 1")
    require(
        troubleshooting_tree_schema.get("title") == "Heuristic Learning Troubleshooting Tree",
        "troubleshooting tree schema title mismatch",
    )
    require(claims_registry.get("$schema") == "/claims-registry.schema.json", "claims registry schema pointer mismatch")
    require(claims_registry.get("schema_version") == 1, "claims registry schema_version must be 1")
    require(
        claims_registry_schema.get("title") == "Heuristic Learning Claims Registry",
        "claims registry schema title mismatch",
    )
    require(case_registry.get("$schema") == "/case-registry.schema.json", "case registry schema pointer mismatch")
    require(case_registry.get("schema_version") == 1, "case registry schema_version must be 1")
    require(case_registry_schema.get("title") == "Heuristic Learning Case Registry", "case registry schema title mismatch")
    require(teaching_registry.get("$schema") == "/teaching-registry.schema.json", "teaching registry schema pointer mismatch")
    require(teaching_registry.get("schema_version") == 1, "teaching registry schema_version must be 1")
    require(
        teaching_registry_schema.get("title") == "Heuristic Learning Teaching Registry",
        "teaching registry schema title mismatch",
    )
    require(slide_deck.get("$schema") == "/slide-deck.schema.json", "slide deck schema pointer mismatch")
    require(slide_deck.get("schema_version") == 1, "slide deck schema_version must be 1")
    require(slide_deck_schema.get("title") == "Heuristic Learning Slide Deck Registry", "slide deck schema title mismatch")
    require(speaker_notes.get("$schema") == "/speaker-notes.schema.json", "speaker notes schema pointer mismatch")
    require(speaker_notes.get("schema_version") == 1, "speaker notes schema_version must be 1")
    require(
        speaker_notes_schema.get("title") == "Heuristic Learning Speaker Notes Registry",
        "speaker notes schema title mismatch",
    )
    require(rubric.get("$schema") == "/rubric.schema.json", "rubric schema pointer mismatch")
    require(rubric.get("schema_version") == 1, "rubric schema_version must be 1")
    require(rubric_schema.get("title") == "Heuristic Learning Rubric Registry", "rubric schema title mismatch")
    require(exercise_registry.get("$schema") == "/exercise-registry.schema.json", "exercise registry schema pointer mismatch")
    require(exercise_registry.get("schema_version") == 1, "exercise registry schema_version must be 1")
    require(
        exercise_registry_schema.get("title") == "Heuristic Learning Exercise Registry",
        "exercise registry schema title mismatch",
    )
    require(
        contribution_contract.get("$schema") == "/contribution-contract.schema.json",
        "contribution contract schema pointer mismatch",
    )
    require(contribution_contract.get("schema_version") == 1, "contribution contract schema_version must be 1")
    require(
        contribution_contract_schema.get("title") == "Heuristic Learning Contribution Contract",
        "contribution contract schema title mismatch",
    )
    require(
        reproducibility.get("$schema") == "/reproducibility-checklist.schema.json",
        "reproducibility checklist schema pointer mismatch",
    )
    require(reproducibility.get("schema_version") == 1, "reproducibility checklist schema_version must be 1")
    require(
        reproducibility_schema.get("title") == "Heuristic Learning Reproducibility Checklist",
        "reproducibility checklist schema title mismatch",
    )
    require(learning_units.get("$schema") == "/learning-units.schema.json", "learning units schema pointer mismatch")
    require(learning_units.get("schema_version") == 1, "learning units schema_version must be 1")
    require(
        learning_units_schema.get("title") == "Heuristic Learning Units Registry",
        "learning units schema title mismatch",
    )
    require(learning_outcomes.get("$schema") == "/learning-outcomes.schema.json", "learning outcomes schema pointer mismatch")
    require(learning_outcomes.get("schema_version") == 1, "learning outcomes schema_version must be 1")
    require(
        learning_outcomes_schema.get("title") == "Heuristic Learning Outcomes Registry",
        "learning outcomes schema title mismatch",
    )
    require(checkpoint_registry.get("$schema") == "/checkpoint-registry.schema.json", "checkpoint registry schema pointer mismatch")
    require(checkpoint_registry.get("schema_version") == 1, "checkpoint registry schema_version must be 1")
    require(
        checkpoint_registry_schema.get("title") == "Heuristic Learning Checkpoint Registry",
        "checkpoint registry schema title mismatch",
    )
    require(evaluation_metrics.get("$schema") == "/evaluation-metrics.schema.json", "evaluation metrics schema pointer mismatch")
    require(evaluation_metrics.get("schema_version") == 1, "evaluation metrics schema_version must be 1")
    require(
        evaluation_metrics_schema.get("title") == "Heuristic Learning Evaluation Metrics Registry",
        "evaluation metrics schema title mismatch",
    )
    require(paper_blueprint.get("$schema") == "/paper-blueprint.schema.json", "paper blueprint schema pointer mismatch")
    require(paper_blueprint.get("schema_version") == 1, "paper blueprint schema_version must be 1")
    require(
        paper_blueprint_schema.get("title") == "Heuristic Learning Paper Blueprint Registry",
        "paper blueprint schema title mismatch",
    )
    require(concept_graph.get("$schema") == "/concept-graph.schema.json", "concept graph schema pointer mismatch")
    require(concept_graph.get("schema_version") == 1, "concept graph schema_version must be 1")
    require(concept_graph_schema.get("title") == "Heuristic Learning Concept Graph", "concept graph schema title mismatch")
    require(teaching_pack.get("$schema") == "/teaching-pack.schema.json", "teaching pack schema pointer mismatch")
    require(teaching_pack.get("schema_version") == 1, "teaching pack schema_version must be 1")
    require(
        teaching_pack_schema.get("title") == "Heuristic Learning Teaching Pack Registry",
        "teaching pack schema title mismatch",
    )
    require(research_projects.get("$schema") == "/research-projects.schema.json", "research projects schema pointer mismatch")
    require(research_projects.get("schema_version") == 1, "research projects schema_version must be 1")
    require(
        research_projects_schema.get("title") == "Heuristic Learning Research Projects Registry",
        "research projects schema title mismatch",
    )
    require(research_logbook.get("$schema") == "/research-logbook.schema.json", "research logbook schema pointer mismatch")
    require(research_logbook.get("schema_version") == 1, "research logbook schema_version must be 1")
    require(
        research_logbook_schema.get("title") == "Heuristic Learning Research Logbook",
        "research logbook schema title mismatch",
    )
    require(completion_audit.get("$schema") == "/completion-audit.schema.json", "completion audit schema pointer mismatch")
    require(completion_audit.get("schema_version") == 1, "completion audit schema_version must be 1")
    require(
        completion_audit_schema.get("title") == "Heuristic Learning Completion Audit Registry",
        "completion audit schema title mismatch",
    )
    require(visual_verification.get("$schema") == "/visual-verification.schema.json", "visual verification schema pointer mismatch")
    require(visual_verification.get("schema_version") == 1, "visual verification schema_version must be 1")
    require(
        visual_verification_schema.get("title") == "Heuristic Learning Visual Verification Registry",
        "visual verification schema title mismatch",
    )
    require(
        visual_acceptance_log.get("$schema") == "/visual-acceptance-log.schema.json",
        "visual acceptance log schema pointer mismatch",
    )
    require(visual_acceptance_log.get("schema_version") == 1, "visual acceptance log schema_version must be 1")
    require(
        visual_acceptance_log_schema.get("title") == "Heuristic Learning Visual Acceptance Log",
        "visual acceptance log schema title mismatch",
    )
    require(x_sources.get("$schema") == "/x-sources.schema.json", "x sources schema pointer mismatch")
    require(x_sources.get("schema_version") == 1, "x sources schema_version must be 1")
    require(
        x_sources_schema.get("title") == "Heuristic Learning X Sources Registry",
        "x sources schema title mismatch",
    )
    require(source_to_case.get("$schema") == "/source-to-case-playbook.schema.json", "source-to-case schema pointer mismatch")
    require(source_to_case.get("schema_version") == 1, "source-to-case schema_version must be 1")
    require(
        source_to_case_schema.get("title") == "Heuristic Learning Source-to-Case Playbook",
        "source-to-case schema title mismatch",
    )
    course = manifest.get("course")
    require(isinstance(course, dict), "course manifest course must be an object")
    require(course.get("verification_command") == "npm run verify", "course manifest verification command mismatch")
    require(
        course.get("structure_check_command") == "npm run course:structure:check",
        "course manifest structure check command mismatch",
    )
    public_resources = manifest.get("public_resources")
    require(isinstance(public_resources, list), "course manifest public_resources must be a list")
    public_resource_ids = {
        resource.get("id")
        for resource in public_resources
        if isinstance(resource, dict) and isinstance(resource.get("id"), str)
    }
    require(
        {
            "course-manifest",
            "course-manifest-schema",
            "example-registry",
            "code-tour",
            "benchmark-summary",
            "ablation-plan",
            "artifact-gap-analysis",
            "troubleshooting-tree",
            "claims-registry",
            "case-registry",
            "teaching-registry",
            "slide-deck",
            "speaker-notes",
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
            "experiment-report-schema",
            "llms",
        }.issubset(public_resource_ids),
        "course manifest missing expected public resources",
    )

    manifest_pages = manifest.get("core_pages")
    require(isinstance(manifest_pages, list), "course manifest core_pages must be a list")
    page_paths = {
        page.get("path")
        for page in manifest_pages
        if isinstance(page, dict) and isinstance(page.get("path"), str)
    }
    for page in [
        "docs/zh-cn/syllabus/index.md",
        "docs/zh-cn/course-map/index.md",
        "docs/zh-cn/theory/learning-loop.md",
        "docs/zh-cn/theory/research-framework.md",
        "docs/zh-cn/examples/index.md",
        "docs/zh-cn/appendix/source-registry.md",
        "docs/zh-cn/appendix/source-to-case-playbook.md",
        "docs/zh-cn/appendix/release-checklist.md",
        "docs/zh-cn/appendix/local-setup.md",
        "docs/zh-cn/appendix/troubleshooting-tree.md",
        "docs/zh-cn/appendix/rubric.md",
        "docs/zh-cn/appendix/instructor-guide.md",
        "docs/zh-cn/appendix/course-schedule.md",
        "docs/zh-cn/appendix/completion-audit.md",
        "docs/zh-cn/appendix/public-entrypoints.md",
        "docs/zh-cn/appendix/visual-verification.md",
        "docs/zh-cn/appendix/reproducibility.md",
        "docs/zh-cn/appendix/exercises.md",
        "docs/zh-cn/appendix/research-projects.md",
        "docs/zh-cn/appendix/research-logbook.md",
        "docs/zh-cn/appendix/benchmark-protocol.md",
        "docs/zh-cn/appendix/benchmark-results.md",
        "docs/zh-cn/appendix/glossary.md",
        "docs/zh-cn/appendix/references.md",
        "docs/zh-cn/appendix/reading-guide.md",
            "docs/zh-cn/appendix/case-registry.md",
        "docs/zh-cn/appendix/code-tour.md",
        "docs/zh-cn/appendix/learning-units.md",
        "docs/zh-cn/appendix/learning-outcomes.md",
        "docs/zh-cn/appendix/checkpoints.md",
        "docs/zh-cn/appendix/teaching-pack.md",
        "docs/zh-cn/appendix/citation.md",
        "docs/zh-cn/appendix/contribution-protocol.md",
        "docs/zh-cn/appendix/research-roadmap.md",
        "docs/zh-cn/appendix/artifact-gap-analysis.md",
        "docs/zh-cn/slides/lecture-3/index.md",
        "docs/zh-cn/slides/lab-2/index.md",
    ]:
        require(page in page_paths, f"course manifest missing core page: {page}")

    manifest_examples = manifest.get("examples")
    require(isinstance(manifest_examples, list), "course manifest examples must be a list")
    registry_examples = example_registry.get("examples")
    benchmark_rows = benchmark_summary.get("summary")
    code_tours = code_tour.get("tours")
    require(isinstance(registry_examples, list), "example registry examples must be a list")
    require(isinstance(benchmark_rows, list), "benchmark summary rows must be a list")
    require(isinstance(code_tours, list), "code tour rows must be a list")
    by_id = {
        example.get("id"): example
        for example in manifest_examples
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    registry_by_id = {
        example.get("id"): example
        for example in registry_examples
        if isinstance(example, dict) and isinstance(example.get("id"), str)
    }
    benchmark_by_id = {
        row.get("id"): row
        for row in benchmark_rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    code_tour_by_example = {
        row.get("example_id"): row
        for row in code_tours
        if isinstance(row, dict) and isinstance(row.get("example_id"), str)
    }
    require(set(by_id) == set(EXAMPLES), "course manifest examples must match structure checker examples")
    require(set(registry_by_id) == set(EXAMPLES), "example registry examples must match structure checker examples")
    require(set(benchmark_by_id) == set(EXAMPLES), "benchmark summary examples must match structure checker examples")
    require(set(code_tour_by_example) == set(EXAMPLES), "code tour examples must match structure checker examples")
    ablation_rows = ablation_plan.get("ablations")
    require(isinstance(ablation_rows, list), "ablation plan rows must be a list")
    ablation_by_example = {
        row.get("example_id"): row
        for row in ablation_rows
        if isinstance(row, dict) and isinstance(row.get("example_id"), str)
    }
    require(set(ablation_by_example) == set(EXAMPLES), "ablation plan examples must match structure checker examples")
    for name, spec in EXAMPLES.items():
        example = by_id[name]
        registry_example = registry_by_id[name]
        benchmark_row = benchmark_by_id[name]
        ablation_row = ablation_by_example[name]
        require(example.get("example_dir") == spec["dir"], f"{name}: manifest example_dir mismatch")
        require(example.get("run_script") == spec["run_script"], f"{name}: manifest run_script mismatch")
        require(example.get("feedback_script") == spec["feedback_script"], f"{name}: manifest feedback_script mismatch")
        require(example.get("report") == spec["report"], f"{name}: manifest report mismatch")
        require(example.get("test") == spec["test"], f"{name}: manifest test mismatch")
        require(example.get("readme") == spec["readme"], f"{name}: manifest readme mismatch")
        for field in ["example_dir", "run_script", "feedback_script", "report", "test", "failure_mode", "source_status"]:
            require(registry_example.get(field) == example.get(field), f"{name}: example registry {field} mismatch")
        for field in ["report", "test", "failure_mode", "source_status"]:
            require(benchmark_row.get(field) == example.get(field), f"{name}: benchmark summary {field} mismatch")
        require(benchmark_row.get("policy_target") == registry_example.get("policy_target"), f"{name}: benchmark policy_target mismatch")
        require(registry_example.get("policy_target"), f"{name}: example registry missing policy_target")
        require(registry_example.get("course_links"), f"{name}: example registry missing course_links")
        require(ablation_row.get("evidence"), f"{name}: ablation row missing evidence")
        require(ablation_row.get("verification_commands"), f"{name}: ablation row missing verification commands")
        for term in spec["syllabus_terms"]:
            require(term in json.dumps(example, ensure_ascii=False), f"{name}: manifest missing term {term}")
            require(term in json.dumps(registry_example, ensure_ascii=False), f"{name}: example registry missing term {term}")

    ci = manifest.get("ci")
    require(isinstance(ci, dict), "course manifest ci must be an object")
    require(ci.get("verify_workflow") == ".github/workflows/verify.yml", "course manifest verify workflow mismatch")
    require(ci.get("deploy_workflow") == ".github/workflows/deploy.yml", "course manifest deploy workflow mismatch")
    require(ci.get("required_command") == "npm run verify", "course manifest required command mismatch")

    materials = teaching_registry.get("materials")
    require(isinstance(materials, list), "teaching registry materials must be a list")
    material_ids = {
        material.get("id")
        for material in materials
        if isinstance(material, dict) and isinstance(material.get("id"), str)
    }
    require(material_ids == {"lecture-1", "lecture-2", "lecture-3", "lab-1", "lab-2"}, "teaching registry ids mismatch")
    for material in materials:
        for key in ["path", "reading"]:
            value = material.get(key)
            if isinstance(value, str):
                require((ROOT / value).exists(), f"teaching registry missing path: {value}")
            elif isinstance(value, list):
                for item in value:
                    require((ROOT / item).exists(), f"teaching registry missing reading: {item}")

    slide_materials = slide_deck.get("materials")
    require(isinstance(slide_materials, list), "slide deck materials must be a list")
    slide_ids = {
        material.get("id")
        for material in slide_materials
        if isinstance(material, dict) and isinstance(material.get("id"), str)
    }
    require(slide_ids == material_ids, "slide deck ids must match teaching registry ids")

    notes = speaker_notes.get("notes")
    require(isinstance(notes, list), "speaker notes registry notes must be a list")
    note_ids = {
        note.get("id")
        for note in notes
        if isinstance(note, dict) and isinstance(note.get("id"), str)
    }
    require(
        note_ids
        == {
            "note-lecture-1",
            "note-lecture-2",
            "note-lecture-3",
            "note-lab-1",
            "note-lab-2",
        },
        "speaker notes registry ids mismatch",
    )
    note_material_ids = {
        note.get("material_id")
        for note in notes
        if isinstance(note, dict) and isinstance(note.get("material_id"), str)
    }
    require(note_material_ids == material_ids, "speaker notes must cover all teaching materials")

    rubric_modules = rubric.get("modules")
    require(isinstance(rubric_modules, list), "rubric modules must be a list")
    rubric_ids = {
        module.get("id")
        for module in rubric_modules
        if isinstance(module, dict) and isinstance(module.get("id"), str)
    }
    require(
        rubric_ids
        == {
            "source-and-problem",
            "probe-and-baseline",
            "heuristic-patch",
            "feedback-report",
            "regression-and-learning-review",
        },
        "rubric module ids mismatch",
    )

    claims = claims_registry.get("claims")
    require(isinstance(claims, list), "claims registry claims must be a list")
    claim_ids = {
        claim.get("id")
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("id"), str)
    }
    require(
        claim_ids
        == {
            "software-structure-learning",
            "feedback-report-as-agent-input",
            "failure-modes-over-average-score",
            "hl-rl-dl-division-of-labor",
            "source-status-is-course-structure",
        },
        "claims registry ids mismatch",
    )

    cases = case_registry.get("cases")
    require(isinstance(cases, list), "case registry cases must be a list")
    case_ids = {
        case.get("id")
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("id"), str)
    }
    require(
        case_ids
        == {
            "ant-gait",
            "breakout",
            "vizdoom",
            "robot-soccer",
            "traffic-simulation",
            "x-signal",
        },
        "case registry ids mismatch",
    )

    units = learning_units.get("units")
    require(isinstance(units, list), "learning units registry units must be a list")
    unit_ids = {
        unit.get("id")
        for unit in units
        if isinstance(unit, dict) and isinstance(unit.get("id"), str)
    }
    require(
        unit_ids
        == {
            "u0-context",
            "u1-minimal-loop",
            "u2-public-artifacts",
            "u3-control-and-systems",
            "u4-research-claims",
            "u5-anti-forgetting-project",
        },
        "learning units registry ids mismatch",
    )

    outcomes = learning_outcomes.get("outcomes")
    require(isinstance(outcomes, list), "learning outcomes registry outcomes must be a list")
    outcome_ids = {
        outcome.get("id")
        for outcome in outcomes
        if isinstance(outcome, dict) and isinstance(outcome.get("id"), str)
    }
    require(
        outcome_ids == {"lo-1", "lo-2", "lo-3", "lo-4", "lo-5"},
        "learning outcomes registry ids mismatch",
    )

    checkpoints = checkpoint_registry.get("checkpoints")
    require(isinstance(checkpoints, list), "checkpoint registry checkpoints must be a list")
    checkpoint_ids = {
        checkpoint.get("id")
        for checkpoint in checkpoints
        if isinstance(checkpoint, dict) and isinstance(checkpoint.get("id"), str)
    }
    require(
        checkpoint_ids == {"cp-0", "cp-1", "cp-2", "cp-3", "cp-4", "cp-5"},
        "checkpoint registry ids mismatch",
    )

    metrics = evaluation_metrics.get("metrics")
    require(isinstance(metrics, list), "evaluation metrics registry metrics must be a list")
    metric_ids = {
        metric.get("id")
        for metric in metrics
        if isinstance(metric, dict) and isinstance(metric.get("id"), str)
    }
    require(
        metric_ids
        == {
            "task-outcome",
            "failure-isolation",
            "update-cost",
            "regression-risk",
            "source-boundary",
        },
        "evaluation metrics registry ids mismatch",
    )

    paper_sections = paper_blueprint.get("sections")
    require(isinstance(paper_sections, list), "paper blueprint registry sections must be a list")
    paper_section_ids = {
        section.get("id")
        for section in paper_sections
        if isinstance(section, dict) and isinstance(section.get("id"), str)
    }
    require(
        paper_section_ids
        == {
            "abstract-and-positioning",
            "problem-and-related-work",
            "method-learning-loop",
            "experiments-and-results",
            "discussion-and-threats",
            "course-and-reuse",
        },
        "paper blueprint registry ids mismatch",
    )

    concepts = concept_graph.get("concepts")
    require(isinstance(concepts, list), "concept graph concepts must be a list")
    concept_ids = {
        concept.get("id")
        for concept in concepts
        if isinstance(concept, dict) and isinstance(concept.get("id"), str)
    }
    require(
        concept_ids
        == {
            "heuristic-learning",
            "signal",
            "probe",
            "baseline",
            "heuristic-patch",
            "feedback-report",
            "regression",
            "source-status",
        },
        "concept graph ids mismatch",
    )

    packs = teaching_pack.get("packs")
    require(isinstance(packs, list), "teaching pack registry packs must be a list")
    pack_ids = {
        pack.get("id")
        for pack in packs
        if isinstance(pack, dict) and isinstance(pack.get("id"), str)
    }
    require(
        pack_ids
        == {
            "tp0-quick-orientation",
            "tp1-hands-on-workshop",
            "tp2-research-seminar",
            "tp3-project-course",
        },
        "teaching pack registry ids mismatch",
    )

    projects = research_projects.get("projects")
    require(isinstance(projects, list), "research projects registry projects must be a list")
    project_ids = {
        project.get("id")
        for project in projects
        if isinstance(project, dict) and isinstance(project.get("id"), str)
    }
    require(
        project_ids
        == {
            "gridworld-new-probe",
            "robot-soccer-lane-check",
            "traffic-grid-safety-constraint",
            "breakout-reflection-prediction",
            "vizdoom-medikit-staging",
            "ant-gait-stability",
            "feedback-format-comparison",
            "anti-forgetting-test-set",
        },
        "research projects registry ids mismatch",
    )

    visual_checks = visual_verification.get("checks")
    require(isinstance(visual_checks, list), "visual verification checks must be a list")
    visual_check_ids = {
        check.get("id")
        for check in visual_checks
        if isinstance(check, dict) and isinstance(check.get("id"), str)
    }
    require(
        visual_check_ids
        == {
            "home-course-entry",
            "course-map-mobile",
            "examples-run-loop",
            "page-slide-mode",
            "public-registry-entrypoints",
            "completion-audit-page",
        },
        "visual verification ids mismatch",
    )

    x_source_items = x_sources.get("sources")
    require(isinstance(x_source_items, list), "x sources registry sources must be a list")
    x_source_ids = {
        source.get("id")
        for source in x_source_items
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }
    require(
        x_source_ids
        == {
            "logicrw-jiayi-hl-summary-2026-05-08",
            "jiayi-original-hl-post-2026-05-08",
            "logicrw-fluid-control-lead-2026-05-19",
        },
        "x sources registry ids mismatch",
    )


def main() -> None:
    check_pages()
    check_markdown_tables()
    check_no_raw_mermaid_blocks()
    check_package_scripts()
    check_examples()
    check_syllabus_alignment()
    check_llm_pointers()
    check_ci_workflows()
    check_templates()
    check_citation_metadata()
    check_course_schedule()
    check_reading_guide()
    check_case_registry()
    check_exercise_registry()
    check_contribution_contract()
    check_reproducibility()
    check_learning_units()
    check_learning_outcomes()
    check_checkpoints()
    check_evaluation_metrics()
    check_paper_blueprint()
    check_ablation_plan()
    check_concept_graph()
    check_teaching_pack()
    check_x_sources()
    check_source_to_case_playbook()
    check_release_metadata()
    check_workspace_hygiene()
    check_course_manifest()
    print(f"checked {len(PAGES)} pages and {len(EXAMPLES)} runnable examples")


if __name__ == "__main__":
    main()
