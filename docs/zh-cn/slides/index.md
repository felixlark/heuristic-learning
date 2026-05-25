---
title: 幻灯片
description: Heuristic Learning 课程幻灯片目录
---

# 幻灯片

本目录把文档章节整理成适合课堂、组会或读书会使用的讲义。每一讲都遵循同一个结构：

- 一个核心问题
- 一张概念图
- 一个案例
- 一个可运行命令
- 一个课后改造任务

机器可读讲义矩阵见 [`/teaching-registry.json`](/teaching-registry.json)，字段约束见 [`/teaching-registry.schema.json`](/teaching-registry.schema.json)。`npm run teaching:registry:check` 会检查每讲/每个 lab 的路径、阅读材料、命令和验收产物是否仍然有效。

学习材料索引见 [`/slide-deck.json`](/slide-deck.json)，字段约束见 [`/slide-deck.schema.json`](/slide-deck.schema.json)。`npm run slides:check` 会检查每讲/每个 lab 的核心小节、示例绑定、练习命令和交付模板是否仍然有效。

讲者备注见 [讲者备注](/zh-cn/appendix/speaker-notes)，机器入口为 [`/speaker-notes.json`](/speaker-notes.json)，字段约束见 [`/speaker-notes.schema.json`](/speaker-notes.schema.json)。`npm run speaker:notes:check` 会检查开场问题、demo 节点、讨论题、常见误解和 exit ticket 是否仍绑定现有讲义。

## 已有讲义

| 讲义 | 主题 | 配套材料 |
| --- | --- | --- |
| [第 1 讲：Learning Beyond Gradients](/zh-cn/slides/lecture-1/) | 为什么要研究 HL | [HL 基础概念](/zh-cn/stage-2/) 与 [GridWorld 示例](/zh-cn/examples/) |
| [第 2 讲：从案例信号到可验证实验](/zh-cn/slides/lecture-2/) | 如何把 X、公开 artifact 和脱敏应用问题转成 HL 实验 | [学习闭环](/zh-cn/theory/learning-loop)、[来源登记](/zh-cn/appendix/source-registry) |
| [第 3 讲：失败类型与反遗忘](/zh-cn/slides/lecture-3/) | 如何防止 heuristic patch 破坏旧经验 | [研究框架](/zh-cn/theory/research-framework)、[课程 Rubric](/zh-cn/appendix/rubric) |
| [Lab 1：跑通 Heuristic Learning 闭环](/zh-cn/slides/lab-1/) | 运行、观察、修改并验证六个最小系统 | [可运行示例](/zh-cn/examples/) 与 `npm run verify` |
| [Lab 2：反遗忘审查](/zh-cn/slides/lab-2/) | 用测试、报告和 Rubric 审查一次 HL 更新 | [第 3 讲](/zh-cn/slides/lecture-3/) 与 [实验报告](/zh-cn/examples/) |

配套题库见 [练习集](/zh-cn/appendix/exercises)，可用于课堂作业、工作坊检查和 capstone 项目。
需要直接开课时，使用 [授课包](/zh-cn/appendix/teaching-pack) 选择 90 分钟导读、2 小时工作坊、研究讨论或 4-6 周项目课。

## 讲义标准

讲义不是文档的复制粘贴。它应该帮读者在 20 到 40 分钟内形成一个可检验的理解，并在课后用代码改动巩固。
