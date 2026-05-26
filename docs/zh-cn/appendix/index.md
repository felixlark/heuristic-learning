---
title: 资料与学习资源
description: HL 课程资料来源、学习规范与研究路线
---

# 资料与学习资源

## 资料分层

| 层级 | 来源 | 用途 |
| --- | --- | --- |
| 一手公开源 | Jiayi 文章、GitHub artifact、X 原帖 | 定义概念与案例 |
| 背景概念 | RL、DL、软件测试、编码智能体 | 界定 HL 的问题边界 |
| 脱敏应用问题 | 私有来源抽象后的任务形态 | 补充应用方向和真实需求 |
| 课程实验 | `examples/`、测试、运行记录 | 形成可验证学习材料 |
| 理论框架 | [研究框架](/zh-cn/theory/research-framework) | 固化问题定义、度量与实验范式 |

## 学习原则

- 先保留可运行最小闭环，再扩展复杂案例。
- 每个概念页都要链接到案例或示例。
- 每个示例都要有一条最短运行命令和至少一个测试。
- 不把未验证的 X 来源或脱敏应用问题写成事实，只写成“待复核来源”或“案例待验证”。
- 任何新规则都要配回归测试，防止 HL 自己发生工程型遗忘。

## 研究路线

后续研究问题见 [研究路线图](/zh-cn/appendix/research-roadmap)。新增任务应能落到来源、案例、示例、报告、测试或课程页。

## 附录入口

- [本地运行与排错](/zh-cn/appendix/local-setup)
- [排错决策树](/zh-cn/appendix/troubleshooting-tree)
- [术语表](/zh-cn/appendix/glossary)
- [来源与背景阅读](/zh-cn/appendix/references)
- [文献阅读指南](/zh-cn/appendix/reading-guide)
- [案例矩阵](/zh-cn/appendix/case-registry)
- [代码导览](/zh-cn/appendix/code-tour)
- [学习单元矩阵](/zh-cn/appendix/learning-units)
- [学习成果矩阵](/zh-cn/appendix/learning-outcomes)
- [阶段检查点](/zh-cn/appendix/checkpoints)
- [评估指标矩阵](/zh-cn/appendix/evaluation-metrics)
- [论文蓝图](/zh-cn/appendix/paper-blueprint)
- [讲者备注](/zh-cn/appendix/speaker-notes)
- [概念图谱](/zh-cn/appendix/concept-graph)
- [授课包](/zh-cn/appendix/teaching-pack)
- [引用与署名](/zh-cn/appendix/citation)
- [来源登记](/zh-cn/appendix/source-registry)
- [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook)
- [发布清单](/zh-cn/appendix/release-checklist)
- [课程评分与验收 Rubric](/zh-cn/appendix/rubric)
- [练习集](/zh-cn/appendix/exercises)
- [教师指南](/zh-cn/appendix/instructor-guide)
- [课程进度表](/zh-cn/appendix/course-schedule)
- [完成度审计](/zh-cn/appendix/completion-audit)
- [视觉与浏览器验收](/zh-cn/appendix/visual-verification)
- [可复现性检查清单](/zh-cn/appendix/reproducibility)
- [研究课题](/zh-cn/appendix/research-projects)
- [研究日志](/zh-cn/appendix/research-logbook)
- [消融计划](/zh-cn/appendix/ablation-plan)
- [Artifact 差距分析](/zh-cn/appendix/artifact-gap-analysis)
- [实验协议](/zh-cn/appendix/benchmark-protocol)
- [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)
- [研究路线图](/zh-cn/appendix/research-roadmap)
- [贡献与研究协议](/zh-cn/appendix/contribution-protocol)
- `templates/case-card.md`
- `templates/experiment-record.md`
- `templates/reproduction-note.md`

## 数据入口

- [`/course-manifest.json`](/course-manifest.json)：列出核心页面、六个可运行示例、实验报告和验证入口。
- [`/course-manifest.schema.json`](/course-manifest.schema.json)：约束 manifest 字段、示例条目和 CI 入口的 JSON Schema。
- [`/example-registry.json`](/example-registry.json)：列出每个 runnable example 的命令、failure mode、报告、测试、更新目标和课程链接。
- [`/example-registry.schema.json`](/example-registry.schema.json)：约束示例矩阵字段，供 `npm run examples:registry:check` 验证。
- [`/code-tour.json`](/code-tour.json)：列出每个 runnable example 的代码阅读顺序、编辑目标、运行命令和测试路径。
- [`/code-tour.schema.json`](/code-tour.schema.json)：约束代码导览字段，供 `npm run code:tour:check` 验证。
- [`/benchmark-summary.json`](/benchmark-summary.json)：列出六个主线示例的 baseline outcome、heuristic outcome、报告、测试和边界。
- [`/benchmark-summary.schema.json`](/benchmark-summary.schema.json)：约束 benchmark 摘要字段，供 `npm run benchmark:summary:check` 验证。
- [`/ablation-plan.json`](/ablation-plan.json)：列出六个主线示例的变量对照、不变量、证据路径和验证命令。
- [`/ablation-plan.schema.json`](/ablation-plan.schema.json)：约束消融计划字段，供 `npm run ablation:plan:check` 验证。
- [`/artifact-gap-analysis.json`](/artifact-gap-analysis.json)：列出轻量 replay 到真实 artifact 的保真度差距、下一步实验和边界。
- [`/artifact-gap-analysis.schema.json`](/artifact-gap-analysis.schema.json)：约束 Artifact 差距分析字段，供 `npm run artifact:gap:check` 验证。
- [`/troubleshooting-tree.json`](/troubleshooting-tree.json)：列出失败面、诊断命令、修复动作、复验命令和关联页面。
- [`/troubleshooting-tree.schema.json`](/troubleshooting-tree.schema.json)：约束排错决策树字段，供 `npm run troubleshooting:tree:check` 验证。
- [`/claims-registry.json`](/claims-registry.json)：列出研究问题、证据页、示例、验证命令和可反驳边界。
- [`/claims-registry.schema.json`](/claims-registry.schema.json)：约束研究问题矩阵字段，供 `npm run claims:registry:check` 验证。
- [`/case-registry.json`](/case-registry.json)：列出案例页、来源状态、绑定示例、failure mode、学习成果和验证命令。
- [`/case-registry.schema.json`](/case-registry.schema.json)：约束案例矩阵字段，供 `npm run cases:check` 验证。
- [`/teaching-registry.json`](/teaching-registry.json)：列出讲义与 lab 的阅读材料、命令和验收产物。
- [`/teaching-registry.schema.json`](/teaching-registry.schema.json)：约束课程材料矩阵字段，供 `npm run teaching:registry:check` 验证。
- [`/slide-deck.json`](/slide-deck.json)：列出每讲与 Lab 的必备标题、绑定示例、课堂命令和交付模板。
- [`/slide-deck.schema.json`](/slide-deck.schema.json)：约束讲义结构字段，供 `npm run slides:check` 验证。
- [`/speaker-notes.json`](/speaker-notes.json)：列出每讲的开场问题、demo 节点、讨论题、常见误解和 exit ticket。
- [`/speaker-notes.schema.json`](/speaker-notes.schema.json)：约束讲者备注字段，供 `npm run speaker:notes:check` 验证。
- [`/rubric.json`](/rubric.json)：列出评分模块、权重、评分档位、证据路径和验收命令。
- [`/rubric.schema.json`](/rubric.schema.json)：约束评分表字段，供 `npm run rubric:check` 验证。
- [`/exercise-registry.json`](/exercise-registry.json)：列出练习题、输入材料、示例、交付物和验收命令。
- [`/exercise-registry.schema.json`](/exercise-registry.schema.json)：约束练习矩阵字段，供 `npm run exercises:check` 验证。
- [`/contribution-contract.json`](/contribution-contract.json)：列出贡献类型、证据字段、必备路径、验证命令和禁止材料。
- [`/contribution-contract.schema.json`](/contribution-contract.schema.json)：约束贡献契约字段，供 `npm run contribution:contract:check` 验证。
- [`/learning-units.json`](/learning-units.json)：列出每个课程单元的阅读、示例、命令、交付物和验收条件。
- [`/learning-units.schema.json`](/learning-units.schema.json)：约束学习单元矩阵字段，供 `npm run learning:units:check` 验证。
- [`/learning-outcomes.json`](/learning-outcomes.json)：列出学习成果到学习单元、练习题、Rubric、证据和验证命令的映射。
- [`/learning-outcomes.schema.json`](/learning-outcomes.schema.json)：约束学习成果矩阵字段，供 `npm run learning:outcomes:check` 验证。
- [`/checkpoint-registry.json`](/checkpoint-registry.json)：列出每个学习单元的阶段自测问题、证据、命令、通过条件和常见失败。
- [`/checkpoint-registry.schema.json`](/checkpoint-registry.schema.json)：约束阶段检查点字段，供 `npm run checkpoints:check` 验证。
- [`/evaluation-metrics.json`](/evaluation-metrics.json)：列出任务结果、失败隔离、更新成本、回归风险和来源边界。
- [`/evaluation-metrics.schema.json`](/evaluation-metrics.schema.json)：约束评估指标字段，供 `npm run metrics:check` 验证。
- [`/paper-blueprint.json`](/paper-blueprint.json)：列出研究写作章节、研究问题、指标、示例、证据路径和边界。
- [`/paper-blueprint.schema.json`](/paper-blueprint.schema.json)：约束论文蓝图字段，供 `npm run paper:blueprint:check` 验证。
- [`/concept-graph.json`](/concept-graph.json)：列出核心概念到研究问题、示例、讲义、页面和验证命令的映射。
- [`/concept-graph.schema.json`](/concept-graph.schema.json)：约束概念图谱字段，供 `npm run concept:graph:check` 验证。
- [`/teaching-pack.json`](/teaching-pack.json)：列出授课包的讲义、阅读材料、demo 命令、交付物和验收项。
- [`/teaching-pack.schema.json`](/teaching-pack.schema.json)：约束授课包字段，供 `npm run teaching:pack:check` 验证。
- [`/research-projects.json`](/research-projects.json)：列出研究项目的来源、failure mode、示例、交付物、验证命令和课程落点。
- [`/research-projects.schema.json`](/research-projects.schema.json)：约束研究项目字段，供 `npm run research:projects:check` 验证。
- [`/research-logbook.json`](/research-logbook.json)：列出阅读来源、绑定示例、研究问题、指标、命令、交付物和边界。
- [`/research-logbook.schema.json`](/research-logbook.schema.json)：约束研究日志字段，供 `npm run research:logbook:check` 验证。
- [`/completion-audit.json`](/completion-audit.json)：列出目标拆解、必跑命令、证据边界和完成前检查。
- [`/completion-audit.schema.json`](/completion-audit.schema.json)：约束完成度审计字段，供 `npm run completion:audit:check` 验证。
- [`/visual-verification.json`](/visual-verification.json)：列出官方 Browser/IAB 或 Chrome 插件的视觉验收路径、视口和验收重点。
- [`/visual-verification.schema.json`](/visual-verification.schema.json)：约束视觉验收字段，供 `npm run visual:verification:check` 验证。
- [`/reproducibility-checklist.json`](/reproducibility-checklist.json)：列出环境、示例、研究问题、教学、贡献和站点复现检查。
- [`/reproducibility-checklist.schema.json`](/reproducibility-checklist.schema.json)：约束可复现性清单字段，供 `npm run reproducibility:check` 验证。
- [`/x-sources.json`](/x-sources.json)：列出 X 来源的证据状态、来源层级、抽取主张、学习落点和边界。
- [`/x-sources.schema.json`](/x-sources.schema.json)：约束 X 来源矩阵字段，供 `npm run x:sources:check` 验证。
- [`/source-to-case-playbook.json`](/source-to-case-playbook.json)：列出 X、公开 artifact、脱敏应用问题和研究假设转成 case card 的路径。
- [`/source-to-case-playbook.schema.json`](/source-to-case-playbook.schema.json)：约束来源到案例 playbook 字段，供 `npm run source:case:check` 验证。
