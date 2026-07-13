---
title: 论文蓝图
description: Heuristic Learning 研究写作的章节、证据、研究问题、指标和边界矩阵
---

# 论文蓝图

本页把 HL 仓库的理论、案例、示例、指标和课程材料整理成一份可写论文或技术报告的蓝图。它不是正式论文草稿，也不把当前轻量 replay 写成高保真复现实验；它的作用是让读者知道：哪些主张已有证据，哪些只能写成假设，哪些命令能验证当前材料没有漂移。

机器可读蓝图见 [`/paper-blueprint.json`](/paper-blueprint.json)，字段约束见 [`/paper-blueprint.schema.json`](/paper-blueprint.schema.json)。`npm run paper:blueprint:check` 会检查章节、研究问题、指标、示例、证据路径、验证命令和 manifest 是否一致。

## 章节结构

| 章节 | 写作目的 | 主要证据 | 验证命令 |
| --- | --- | --- | --- |
| 摘要与定位 | 说明 HL 的研究对象、证据形态和课程边界 | [HL 基础概念](/zh-cn/stage-2/)、[从 RL/DL 到 HL](/zh-cn/stage-3/)、[文献阅读指南](/zh-cn/appendix/reading-guide) | `npm run claims:registry:check`、`npm run source:registry:check` |
| 问题定义与相关工作 | 连接 Jiayi 来源、RL/DL、软件测试和编码智能体边界 | [来源与背景阅读](/zh-cn/appendix/references)、[来源登记](/zh-cn/appendix/source-registry)、[文献阅读指南](/zh-cn/appendix/reading-guide) | `npm run source:registry:check`、`npm run claims:registry:check` |
| 方法：学习闭环 | 定义 signal、probe、baseline、patch、report 和 regression | [学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework)、`/example-registry.json` | `npm run examples:registry:check`、`npm run metrics:check` |
| 实验与结果 | 用六个示例说明 baseline failure、heuristic outcome 和后续变量对照 | [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)、[消融计划](/zh-cn/appendix/ablation-plan)、`/benchmark-summary.json`、`/ablation-plan.json`、`experiments/*/latest.json` | `npm run examples:feedback`、`npm run examples:reports:check`、`npm run benchmark:summary:check`、`npm run ablation:plan:check` |
| 讨论、局限与威胁 | 说明来源、复现、高保真环境和视觉验收边界 | [引用与署名](/zh-cn/appendix/citation)、[可复现性检查](/zh-cn/appendix/reproducibility)、[视觉验收](/zh-cn/appendix/visual-verification) | `npm run reproducibility:check`、`npm run visual:verification:check`、`npm run x:sources:check` |
| 教学使用与复现材料 | 说明读者如何沿同一套证据链学习、复现和扩展 | [学习单元](/zh-cn/appendix/learning-units)、[授课包](/zh-cn/appendix/teaching-pack) | `npm run learning:units:check`、`npm run teaching:pack:check` |

## 写作纪律

1. 每个章节必须绑定至少一个证据路径。
2. 涉及研究主张时，先看 `/claims-registry.json` 和 [研究问题](/zh-cn/theory/research-framework)。
3. 涉及实验结果时，先跑 `npm run examples:feedback` 和 `npm run benchmark:summary:check`。
4. 涉及局限时，必须保留来源状态、轻量 replay 和 Browser/IAB 验收边界。
5. 涉及教学使用时，只写读者如何学习、复现和扩展；不把未验证来源写成研究结论。

## 从蓝图到报告

最小报告可以按以下顺序写：

```text
Abstract:
Problem:
Method:
Experiments:
Threats:
Teaching use:
```

每一段都要能在 `/paper-blueprint.json` 里找到对应章节，并能用该章节的 `verification_commands` 复查。

```bash
npm run paper:blueprint:check
npm run verify
```
