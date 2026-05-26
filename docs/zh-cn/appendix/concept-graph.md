---
title: 概念图谱
description: Heuristic Learning 术语、研究问题、示例、讲义和验证命令的机器可读映射
---

# 概念图谱

本页把术语表中的关键概念连接到研究问题、可运行示例、讲义和验证命令。它的作用是让读者和编码智能体都能从一个概念出发，找到应该阅读的页面、应该运行的示例、应该交付的材料。

机器可读图谱见 [`/concept-graph.json`](/concept-graph.json)，字段约束见 [`/concept-graph.schema.json`](/concept-graph.schema.json)。`npm run concept:graph:check` 会检查图谱是否仍与术语表、研究问题 registry、示例 registry、讲义 registry 和 package scripts 一致。

## 交互式图谱

点击节点，查看它在学习闭环里的位置、对应示例、阅读页面和验证命令。中心节点说明 HL 的学习对象；外圈节点按来源、验证、更新和复盘组织。

<ClientOnly>
  <ConceptGraphExplorer />
</ClientOnly>

图谱覆盖 Heuristic Learning、Signal、Probe、Baseline、Heuristic patch、Feedback report、Regression 和 Source status。每个节点都从 `/concept-graph.json` 读取对应的示例、讲义、页面和验证命令。

## 使用方式

学生使用：

1. 从 [术语表](/zh-cn/appendix/glossary) 选一个概念。
2. 在本页找到代表示例和讲义。
3. 运行图谱中的命令。
4. 用 `templates/experiment-record.md` 写下观察。

研究者使用：

1. 从 `claim_ids` 找到 [研究问题](/zh-cn/theory/research-framework)。
2. 从 `example_ids` 找到能支持或反驳研究问题的最小 replay。
3. 从 `commands` 确认当前证据是否可复查。
4. 用 `templates/claim-review.md` 标注证据状态和反驳路径。

编码智能体使用：

1. 读取 `/concept-graph.json`。
2. 根据概念定位 `pages`、`example_ids` 和 `commands`。
3. 修改任何概念相关页面后，运行 `npm run concept:graph:check` 和 `npm run verify`。

## 学习规则

- 新术语进入主线前，必须能连到至少一个研究问题、一个示例、一个讲义材料和一条验证命令。
- 如果概念没有 runnable example，只能停留在研究路线图或来源登记，不进入本图谱的核心概念表。
- 如果新增示例或讲义改变了概念落点，必须同步 `/concept-graph.json`。
