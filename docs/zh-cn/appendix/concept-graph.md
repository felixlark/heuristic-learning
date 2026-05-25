---
title: 概念图谱
description: Heuristic Learning 术语、研究命题、示例、讲义和验证命令的机器可读映射
---

# 概念图谱

本页把术语表中的关键概念连接到研究命题、可运行示例、讲义和验证命令。它的作用是让读者和编码智能体都能从一个概念出发，找到应该阅读的页面、应该运行的示例、应该交付的材料。

机器可读图谱见 [`/concept-graph.json`](/concept-graph.json)，字段约束见 [`/concept-graph.schema.json`](/concept-graph.schema.json)。`npm run concept:graph:check` 会检查图谱是否仍与术语表、命题 registry、示例 registry、讲义 registry 和 package scripts 一致。

## 核心概念

| 概念 | 连接到的命题 | 代表示例 | 讲义 | 验证 |
| --- | --- | --- | --- | --- |
| Heuristic Learning | 学习对象可以是软件结构；反馈报告是下一轮智能体的训练样本 | GridWorld、Breakout、Ant Gait | 第 1 讲、第 2 讲 | `npm run claims:registry:check`、`npm run examples:feedback` |
| Signal | 来源状态必须进入课程结构 | Robot Soccer、Traffic Grid、Breakout | 第 2 讲 | `npm run source:registry:check`、`npm run x:sources:check` |
| Probe | 失败类型比平均分更适合课程化 | 六个 runnable examples | 第 2 讲、Lab 1 | `npm run examples:registry:check`、`npm run examples:test` |
| Baseline | 失败类型比平均分更适合课程化 | 六个 runnable examples | 第 2 讲、Lab 1 | `npm run benchmark:summary:check`、`npm run examples:reports:check` |
| Heuristic patch | 学习对象可以是软件结构 | Robot Soccer、Traffic Grid、Breakout、Ant Gait | 第 2 讲、第 3 讲、Lab 2 | `npm run examples:feedback`、`npm run examples:test` |
| Feedback report | 反馈报告是下一轮智能体的训练样本 | 六个 runnable examples | 第 1 讲、第 2 讲、Lab 1 | `npm run examples:feedback`、`npm run examples:reports:check` |
| Regression | 失败类型和来源状态的回归约束 | 六个 runnable examples | 第 3 讲、Lab 2 | `npm run examples:test`、`npm run verify` |
| Source status | 来源状态必须进入课程结构 | Robot Soccer、Traffic Grid、VizDoom、Breakout、Ant Gait | 第 2 讲 | `npm run source:registry:check`、`npm run x:sources:check` |

## 使用方式

学生使用：

1. 从 [术语表](/zh-cn/appendix/glossary) 选一个概念。
2. 在本页找到代表示例和讲义。
3. 运行图谱中的命令。
4. 用 `templates/experiment-record.md` 写下观察。

研究者使用：

1. 从 `claim_ids` 找到 [研究命题](/zh-cn/theory/research-propositions)。
2. 从 `example_ids` 找到能支持或反驳命题的最小 replay。
3. 从 `commands` 确认当前证据是否可复查。
4. 用 `templates/claim-review.md` 标注证据状态和反驳路径。

编码智能体使用：

1. 读取 `/concept-graph.json`。
2. 根据概念定位 `pages`、`example_ids` 和 `commands`。
3. 修改任何概念相关页面后，运行 `npm run concept:graph:check` 和 `npm run verify`。

## 学习规则

- 新术语进入主线前，必须能连到至少一个命题、一个示例、一个讲义材料和一条验证命令。
- 如果概念没有 runnable example，只能停留在研究路线图或来源登记，不进入本图谱的核心概念表。
- 如果新增示例或讲义改变了概念落点，必须同步 `/concept-graph.json`。
