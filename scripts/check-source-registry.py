#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/zh-cn/appendix/source-registry.md"

ALLOWED_STATUSES = {
    "已复现",
    "已复现为轻量 replay",
    "已复现为最小环境",
    "已结构化",
    "已定位",
    "待采集",
}

REPRODUCED_EXAMPLES = {
    "examples/ant-gait-replay/",
    "examples/breakout-replay/",
    "examples/robot-soccer/",
    "examples/vizdoom-replay/",
    "examples/traffic-grid/",
}

REQUIRED_X_EVIDENCE = [
    "https://x.com/Trinkle23897/status/2052596837547495549",
    "https://x.com/0xLogicrw/status/2052701677615218717",
    "ft sync",
    "ft show",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def iter_table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 4 and cells[0] != "来源":
            rows.append(cells)
    return rows


def check_registry() -> None:
    require(REGISTRY.exists(), "missing source registry")
    text = REGISTRY.read_text(encoding="utf-8")
    rows = iter_table_rows(text)
    require(rows, "source registry has no table rows")

    statuses: list[str] = []
    reproduced_rows: list[list[str]] = []
    for row in rows:
        status = row[2]
        statuses.append(status)
        require(
            any(allowed in status for allowed in ALLOWED_STATUSES),
            f"unknown source status: {status}",
        )
        if "已复现" in status:
            reproduced_rows.append(row)

    for status in ["已复现", "已结构化", "已定位", "待采集"]:
        require(any(status in item for item in statuses), f"source registry missing status family: {status}")

    registry_text = "\n".join("|".join(row) for row in reproduced_rows)
    for example in REPRODUCED_EXAMPLES:
        require(example in registry_text, f"reproduced source missing runnable example link: {example}")
        require((ROOT / example).is_dir(), f"reproduced example directory missing: {example}")

    for evidence in REQUIRED_X_EVIDENCE:
        require(evidence in text, f"source registry missing X/FieldTheory evidence: {evidence}")

    require("不能直接写成公开事实" in text, "source registry must warn about internal-source limits")
    require("不把 X 线索写进主线结论" in text, "source registry must guard unverified X claims")

    print(f"checked {len(rows)} source rows and {len(reproduced_rows)} reproduced rows")


if __name__ == "__main__":
    check_registry()
