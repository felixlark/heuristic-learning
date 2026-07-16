---
title: 来源登记
description: Heuristic Learning 课程的来源层级、证据状态与声明边界
---

# 来源登记

本页帮助读者判断每个案例的证据强度。它不是参考文献列表，而是来源边界表：哪些内容已经有可运行实验，哪些只有公开材料支撑，哪些仍然只是研究方向。

## 来源状态定义

| 状态 | 含义 | 课程中如何使用 |
| --- | --- | --- |
| 已复现 | 已有 runnable example、feedback report 和测试 | 可以作为课程实验 |
| 已结构化 | 已有案例页或研究卡，但还没有完整实验 | 可以作为讨论材料 |
| 已定位 | 已找到公开 URL 或代码 artifact，但尚未转成实验 | 只能写为待复现方向 |
| 待采集 | 只有方向，还没有足够可引用内容 | 不能写成事实 |

## 公开主源

| 来源 | 类型 | 当前状态 | 学习落点 |
| --- | --- | --- | --- |
| [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) | Jiayi Weng 公开文章 | 已定位 | [HL 基础概念](/zh-cn/stage-2/)、[研究框架](/zh-cn/theory/research-framework) |
| [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) | 公开代码 artifact | 已定位 | [案例库](/zh-cn/cases/) |
| `mujoco/ant/heuristic_ant.py` | MuJoCo Ant artifact | 已复现为轻量 replay | [Ant Gait 案例](/zh-cn/cases/ant-gait/)、`examples/ant-gait-replay/` |
| `vizdoom/heuristic_vizdoom_d1_cv.py` | VizDoom artifact | 已复现为轻量 replay | [VizDoom 案例](/zh-cn/cases/vizdoom/)、`examples/vizdoom-replay/` |
| `atari/breakout/heuristic_breakout.py` | Atari Breakout artifact | 已复现为轻量 replay | [Breakout 案例](/zh-cn/cases/breakout/)、`examples/breakout-replay/` |
| Other Atari artifacts | 游戏控制 artifact | 已定位 | 待转成课程实验 |
| MuJoCo HalfCheetah artifacts | 连续控制 artifact | 已定位 | 待转成课程实验 |
| [`@0xdeusyu` shape-from-shading 帖](https://x.com/0xdeusyu/status/1986696571006951603) | X 科普线索 | 已结构化 | [视觉先验案例](/zh-cn/cases/visual-prior/)、`examples/shape-from-shading/` |
| [Ramachandran 1988, Nature](https://doi.org/10.1038/331163a0) | shape-from-shading 一手论文 | 已定位 | [视觉先验案例](/zh-cn/cases/visual-prior/) |
| [Adams, Graf & Ernst 2004](https://doi.org/10.1038/nn1312) | 可适应光照先验实验 | 已定位 | [视觉先验案例](/zh-cn/cases/visual-prior/) |
| `https://x.com/Trinkle23897/status/2052596837547495549` | Jiayi Weng X 原帖 | 已定位 | [X 来源案例](/zh-cn/cases/x-signal/) |
| `https://x.com/0xLogicrw/status/2052701677615218717` | X 中文转述，引用 Jiayi 原帖 | 已结构化 | [X 来源案例](/zh-cn/cases/x-signal/) |
| Jiayi Weng 后续 X thread 与评论 | X 后续讨论 | 待采集 | [研究路线图](/zh-cn/appendix/research-roadmap) |
| [SelfCheckGPT](https://aclanthology.org/2023.emnlp-main.557/) | 公开论文 | 已定位 | [事实约束审计研究](/zh-cn/appendix/constraint-audit) |
| [Chain-of-Verification](https://aclanthology.org/2024.findings-acl.212/) | 公开论文 | 已定位 | [事实约束审计研究](/zh-cn/appendix/constraint-audit) |
| [FActScore](https://aclanthology.org/2023.emnlp-main.741/) | 公开论文 | 已定位 | [事实约束审计研究](/zh-cn/appendix/constraint-audit) |

## 脱敏应用案例

| 来源 | 问题形态 | 当前状态 | 学习落点 |
| --- | --- | --- | --- |
| 脱敏应用方向：机器人足球策略学习 | 机器人足球策略需要在射门前检查通道是否被挡住 | 已复现为最小环境 | [机器人足球案例](/zh-cn/cases/robot-soccer/)、`examples/robot-soccer/` |
| 脱敏应用方向：交通控制 | 交通控制策略需要先保护下游容量，再决定放行 | 已复现为最小环境 | [交通模拟案例](/zh-cn/cases/traffic-simulation/)、`examples/traffic-grid/` |

脱敏应用案例只公开任务形态、状态字段、失败模式和验证命令；不公开原始消息、会议纪要、私有链接、个人数据或真实系统日志。公开协作的安全边界见根目录 `SECURITY.md`。

## X 来源状态

X 是 Jiayi Weng 相关讨论的重要公开入口。课程只区分来源层级，不要求读者了解采集工具：

- `@0xdeusyu` 的 shape-from-shading 帖已转成视觉先验研究案例；帖文本身只作为线索，事实主张由独立论文约束，运行命令为 `npm run examples:shape-from-shading` 与 `npm run examples:test`。
- Jiayi Weng / `@Trinkle23897` 原帖 URL 已知：`https://x.com/Trinkle23897/status/2052596837547495549`。在直接复核前，它只作为待复核一手来源。
- `@0xLogicrw` 在 2026-05-08 的中文转述引用了该原帖：`https://x.com/0xLogicrw/status/2052701677615218717`。这可以帮助定位问题结构，但不能替代原帖。
- `@0xLogicrw` 在 2026-05-19 转述的流体控制方向目前只作为待结构化研究方向。

X 来源矩阵见 [`/x-sources.json`](/x-sources.json)。其中 `extraction_cards` 把公开讨论转成课程抽取卡，明确概念、主张、学习落点、runnable example、验证命令和边界。更完整的来源到 case card 路径见 [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook)。

```bash
npm run x:sources:check
npm run source:case:check
```

轻量 replay 到真实 artifact 的保真度差距见 [Artifact 差距分析](/zh-cn/appendix/artifact-gap-analysis)，机器入口为 [`/artifact-gap-analysis.json`](/artifact-gap-analysis.json)，检查命令为 `npm run artifact:gap:check`。它负责区分“已能教学和回归测试”与“已完成真实环境复现”。

## 进入主线课程的门槛

一条来源进入主线课程前，至少要满足：

- 有公开 URL、脱敏来源标签或实验文件作为来源。
- 有明确状态：已复现、已结构化、已定位或待采集。
- 对应一个案例页、示例代码、实验记录或路线图待办。
- 如果声称“已复现”，必须能通过 `npm run verify`。

本页的结构由下面命令检查：

```bash
npm run source:registry:check
```

它会验证来源状态词、X 来源证据，以及“已复现”条目是否指向 runnable example。
