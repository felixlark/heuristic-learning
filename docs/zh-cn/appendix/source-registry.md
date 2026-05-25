---
title: 来源登记
description: Heuristic Learning 仓库的公开来源、内部线索与采集状态
---

# 来源登记

本页用于记录 HL 课程材料的来源状态。它不是参考文献列表，而是一个维护台账：哪些来源已经被转成课程内容，哪些只是线索，哪些还缺验证。

## 来源状态定义

| 状态 | 含义 | 能否写入主线课程 |
| --- | --- | --- |
| 已复现 | 已有本仓库 runnable example、feedback report 和测试 | 可以 |
| 已结构化 | 已有案例页，但还没有真实环境或完整实验 | 可以作为线索 |
| 已定位 | 已找到公开 artifact，但尚未转成课程实验 | 只能写为待办 |
| 待采集 | 知道应从某渠道采集，但当前没有可引用内容 | 不能写成事实 |

## 公开主源

| 来源 | 类型 | 当前状态 | 本仓库落点 |
| --- | --- | --- | --- |
| [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) | Jiayi Weng 公开文章 | 已定位 | [HL 基础概念](/zh-cn/stage-2/)、[研究框架](/zh-cn/theory/research-framework) |
| [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) | 公开代码 artifact | 已定位 | [案例库](/zh-cn/cases/) |
| `mujoco/ant/heuristic_ant.py` | MuJoCo Ant artifact | 已复现为轻量 replay | [Ant Gait 案例](/zh-cn/cases/ant-gait/)、`examples/ant-gait-replay/` |
| `vizdoom/heuristic_vizdoom_d1_cv.py` | VizDoom artifact | 已复现为轻量 replay | [VizDoom 案例](/zh-cn/cases/vizdoom/)、`examples/vizdoom-replay/` |
| `atari/breakout/heuristic_breakout.py` | Atari Breakout artifact | 已复现为轻量 replay | [Breakout 案例](/zh-cn/cases/breakout/)、`examples/breakout-replay/` |
| Other Atari artifacts | 游戏控制 artifact | 已定位 | 待转成课程实验 |
| MuJoCo HalfCheetah artifacts | 连续控制 artifact | 已定位 | 待转成课程实验 |
| `https://x.com/Trinkle23897/status/2052596837547495549` | Jiayi Weng X 原帖 | 已定位 | [X 线索案例](/zh-cn/cases/x-signal/) |
| `https://x.com/0xLogicrw/status/2052701677615218717` | X 中文转述，引用 Jiayi 原帖 | 已结构化 | [X 线索案例](/zh-cn/cases/x-signal/) |
| Jiayi Weng 后续 X thread 与评论 | X 后续讨论 | 待采集 | [研究路线图](/zh-cn/appendix/research-roadmap) |

## 内部线索

| 来源 | 线索 | 当前状态 | 本仓库落点 |
| --- | --- | --- | --- |
| 飞书消息，2026-05-17 | 把 Heuristic Learning 用在机器人足球策略学习 | 已复现为最小环境 | [机器人足球案例](/zh-cn/cases/robot-soccer/)、`examples/robot-soccer/` |
| 飞书任务消息，2026-05-13 | 把翁家翌的启发式学习用于武汉东湖交通模拟器 | 已复现为最小环境 | [交通模拟案例](/zh-cn/cases/traffic-simulation/)、`examples/traffic-grid/` |

内部线索不能直接写成公开事实。写入课程时必须标清“来自飞书任务/消息线索”，并优先转成最小可运行实验。
不要把飞书原文、会议纪要、个人数据、token、cookie 或私有链接写进 issue、PR、文档或实验报告；公开协作的安全边界见根目录 `SECURITY.md`。

## X / FieldTheory 状态

X 是重要一手来源。当前本地 FieldTheory cache 已命中 Jiayi HL 相关转述和被引用原帖：

```bash
ft status
ft search "Jiayi Weng" --limit 10
ft show 2052701677615218717
```

当前记录：

- `ft status` 显示本地 cache 有 920 条 bookmark。
- `Jiayi Weng` 命中 `@0xLogicrw` 在 2026-05-08 的中文转述。
- 该转述引用 Jiayi Weng / `@Trinkle23897` 在 2026-05-08 的原帖 `2052596837547495549`。
- 当前 `ft show 2052596837547495549` 返回 `Bookmark not found`，所以 Jiayi 原帖只标为 `referenced-not-cached`。
- 当前 `ft search` 版本对带连字符的查询可能报 SQL 解析错误，抽取流程应使用文本输出、`ft show` 或直接读取本地 JSONL cache。

机器可读 X 线索矩阵见 [`/x-sources.json`](/x-sources.json)，字段约束见 [`/x-sources.schema.json`](/x-sources.schema.json)。其中 `extraction_cards` 负责把已命中的 X 线索转成课程抽取卡，明确概念、课程化主张、落点、runnable example、验证命令和边界。更完整的来源到 case card 操作路径见 [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook)，机器入口为 [`/source-to-case-playbook.json`](/source-to-case-playbook.json)。检查命令为：

```bash
npm run x:sources:check
npm run source:case:check
```

轻量 replay 到真实 artifact 的保真度差距见 [Artifact 差距分析](/zh-cn/appendix/artifact-gap-analysis)，机器入口为 [`/artifact-gap-analysis.json`](/artifact-gap-analysis.json)，检查命令为 `npm run artifact:gap:check`。它负责区分“已能教学和回归测试”与“已完成真实环境复现”。

后续采集规则：

1. 优先用 `ft sync` 或 `ft sync --api` 更新本地 cache。
2. 再用 `ft search`、`ft list`、`ft show` 或本地 JSONL 读取候选帖。
3. 每条 X 线索必须转成 case card，至少包含作者、发布日期、URL、原始主张、当前验证状态和本仓库落点。
4. 没有本地命中或可引用 URL 时，不把 X 线索写进主线结论。

## 进入主线课程的门槛

一条来源进入主线课程前，至少要满足：

- 有公开 URL、内部消息位置或实验文件作为来源。
- 有明确状态：已复现、已结构化、已定位或待采集。
- 对应一个案例页、示例代码、实验记录或路线图待办。
- 如果声称“已复现”，必须能通过 `npm run verify`。

本页的结构由下面命令检查：

```bash
npm run source:registry:check
```

它会验证来源状态词、X/FieldTheory 证据，以及“已复现”条目是否指向本仓库的 runnable example。

这个登记页应该随着案例扩展持续更新，避免课程内容变成不可追溯的二手概括。
