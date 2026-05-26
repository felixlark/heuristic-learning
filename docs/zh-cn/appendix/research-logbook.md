---
title: 研究日志
description: 把阅读、代码运行、研究问题和下一步实验连成可检查记录
---

# 研究日志

研究日志回答一个学习问题：读完一篇文章、一段 artifact 代码、一条 X 来源或一个脱敏应用问题之后，如何留下下一轮可以继续推进的证据。它把 [文献阅读指南](/zh-cn/appendix/reading-guide)、[案例矩阵](/zh-cn/appendix/case-registry)、[评估指标](/zh-cn/appendix/evaluation-metrics) 和 [论文蓝图](/zh-cn/appendix/paper-blueprint) 连接起来。

机器可读日志见 [`/research-logbook.json`](/research-logbook.json)，字段约束见 [`/research-logbook.schema.json`](/research-logbook.schema.json)。`npm run research:logbook:check` 会检查每条记录的来源、绑定示例、研究问题、指标、命令、交付物和边界。

## 记录格式

| 字段 | 含义 |
| --- | --- |
| `source_type` | 来源类别：公开文章、公开代码 artifact、X 来源、脱敏应用问题或跨示例分析 |
| `reading_goal` | 本次阅读要抽取的可教学问题 |
| `bound_examples` | 读完后应该能落到哪些 runnable example |
| `bound_claims` | 影响哪些研究问题，而不是直接写成结论 |
| `metrics` | 用哪些指标判断后续实验是否更强 |
| `commands` | 本条记录至少要跑通的命令 |
| `deliverables` | 应更新的课程页、实验报告或模板 |
| `boundary` | 禁止外推、禁止公开或禁止声明的部分 |

## 当前日志

| 记录 | 来源类型 | 绑定示例 | 验证命令 | 下一步 |
| --- | --- | --- | --- | --- |
| `lbg-core-loop-reading` | `public-essay` | `gridworld`、`vizdoom-replay` | `npm run examples:test`、`npm run claims:registry:check` | 继续把文章里的任务类型映射到 case registry |
| `breakout-artifact-reading` | `public-code-artifact` | `breakout-replay` | `npm run examples:breakout-replay:feedback`、`npm run artifact:gap:check` | 补 reflection 参数扰动练习 |
| `x-signal-case-reading` | `x-source` | `breakout-replay`、`ant-gait-replay` | `npm run x:sources:check`、`npm run source:case:check` | 复核一手原帖并更新证据状态 |
| `robot-soccer-signal-reading` | `sanitized-application` | `robot-soccer` | `npm run examples:robot-soccer:feedback`、`npm run examples:test` | 扩展安全通道场景 |
| `cross-example-report-reading` | `cross-example-analysis` | 六个 runnable examples | `npm run examples:reports:check`、`npm run benchmark:summary:check`、`npm run metrics:check` | 为每个报告补人工可读 edit hint |

## 阅读目标

| 记录 | reading_goal |
| --- | --- |
| `lbg-core-loop-reading` | 把 Learning Beyond Gradients 中的核心更新对象抽象为可教学的 HL 学习闭环。 |
| `breakout-artifact-reading` | 把 Breakout artifact 的几何预测思想压缩成读者能读懂和能测试的 replay。 |
| `x-signal-case-reading` | 把 Jiayi Weng 相关 X 来源拆成来源状态、可可学习、可验证问题和禁止声明。 |
| `robot-soccer-signal-reading` | 把机器人足球方向转成脱敏、可运行、可测试的 blocked-lane 教学案例。 |
| `cross-example-report-reading` | 比较六个 latest.json 是否足以定位 failure mode 和 update target。 |

## 使用方式

1. 先从 [文献阅读指南](/zh-cn/appendix/reading-guide) 或 [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook) 选择来源。
2. 对公开 artifact、X 来源或脱敏应用问题，先用 `templates/reproduction-note.md` 写清来源状态、复现范围、缺失保真度、反驳路径和下一步实验。
3. 写清楚本次阅读只想抽取一个问题，不把整篇文章或整段代码一次性搬进仓库。
4. 绑定一个或多个 runnable example，并列出最短命令。
5. 绑定研究问题和评估指标，说明它支持、削弱或只是提出问题。
6. 写出 `boundary`，尤其是待直接复核来源、轻量 replay、私有资料脱敏和未跑真实环境这些边界。
7. 跑 `npm run research:logbook:check` 和相关命令，确保日志不是孤立笔记。

## 与论文蓝图的关系

研究日志不是论文目录。它记录“读到什么、跑了什么、还缺什么”；[论文蓝图](/zh-cn/appendix/paper-blueprint) 才决定这些记录能否进入正式写作。没有示例、命令、指标和边界的日志，只能作为研究线索，不能升级为主线结论。

## 交付模板

- `templates/reproduction-note.md`：把来源状态、复现范围、保真度缺口、反驳路径和下一步实验分开时使用。
- `templates/claim-review.md`：把阅读记录升级为研究问题审查时使用。
- `templates/anti-forgetting-checklist.md`：把跨示例报告或规则更新变成反遗忘审查时使用。
- `templates/case-card.md`：把来源线索升级为案例卡时使用。
- `templates/experiment-record.md`：把命令结果和 candidate update 固化为实验记录时使用。

## 维护命令

```bash
npm run research:logbook:check
npm run research:projects:check
npm run claims:registry:check
npm run verify
```
