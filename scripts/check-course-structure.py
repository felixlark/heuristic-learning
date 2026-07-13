#!/usr/bin/env python3
"""Check the learner-facing course contract without course-production metadata."""

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    target = ROOT / path
    require(target.exists(), f"missing learner-facing file: {path}")
    return target.read_text(encoding="utf-8")


def main():
    package = json.loads(read("package.json"))
    scripts = package["scripts"]
    pages = {
        "home": read("docs/index.md"),
        "zh-home": read("docs/zh-cn/index.md"),
        "map": read("docs/zh-cn/course-map/index.md"),
        "syllabus": read("docs/zh-cn/syllabus/index.md"),
        "concepts": read("docs/zh-cn/stage-2/index.md"),
        "comparison": read("docs/zh-cn/stage-3/index.md"),
        "loop": read("docs/zh-cn/theory/learning-loop.md"),
        "examples": read("docs/zh-cn/examples/index.md"),
        "cases": read("docs/zh-cn/cases/index.md"),
        "talk": read("docs/zh-cn/talk/index.md"),
        "benchmark": read("docs/zh-cn/benchmark/index.md"),
    }

    for key in ("zh-home", "map", "syllabus"):
        for term in ("概念", "示例", "案例", "验证"):
            require(term in pages[key], f"{key} must include unified learning step: {term}")

    for key in ("concepts", "comparison", "loop"):
        require(
            any(link in pages[key] for link in ("/zh-cn/examples", "/zh-cn/cases", "Learning Beyond Gradients")),
            f"theory page {key} must link to an example, case, or source",
        )

    for term in ("Gymnasium", "holdout", "audit", "追加", "负面结果"):
        require(term in pages["benchmark"], f"benchmark page missing: {term}")
    require("幻灯片按钮" in pages["talk"], "talk page must explain page-level slide mode")

    forbidden = ("longbiaochen", "/zh-cn/slides/", "讲者备注", "为什么参考", "复用 EasyVibe")
    public_text = "\n".join(pages.values())
    for term in forbidden:
        require(term not in public_text, f"learner-facing core pages contain legacy term: {term}")

    registry = json.loads(read("docs/public/example-registry.json"))
    for example in registry["examples"]:
        for field in ("example_dir", "test", "policy_target"):
            require((ROOT / example[field]).exists(), f"{example['id']} missing {field}")
        require(example["run_script"] in scripts, f"{example['id']} missing run script")
        require(example["feedback_script"] in scripts, f"{example['id']} missing feedback script")

    for script in ("examples:cartpole:dev", "examples:cartpole:holdout", "examples:cartpole:audit"):
        require(script in scripts, f"missing advanced benchmark script: {script}")
    require((ROOT / "tests/test_cartpole_benchmark.py").exists(), "advanced benchmark test missing")

    print(f"checked {len(pages)} learner pages, {len(registry['examples'])} core examples, and advanced benchmark")


if __name__ == "__main__":
    main()
