---
title: 评估指标矩阵
description: Heuristic Learning 研究评估维度、证据路径和验证命令
---

# 评估指标矩阵

本页把 [研究框架](/zh-cn/theory/research-framework) 中的度量维度整理成可检查的课程矩阵。它不是排行榜，也不把当前轻量 replay 写成完整论文实验；它的作用是让每个 HL 案例都能回答同一组问题：任务是否改善、失败是否被隔离、更新成本是否可复现、旧经验是否被保护、来源边界是否清楚。

机器可读矩阵见 [`/evaluation-metrics.json`](/evaluation-metrics.json)，字段约束见 [`/evaluation-metrics.schema.json`](/evaluation-metrics.schema.json)。`npm run metrics:check` 会检查指标、示例、命题、证据路径、验证命令和 manifest 是否一致。

## 五个指标

| 指标 | 核心问题 | 主要证据 | 验证命令 |
| --- | --- | --- | --- |
| 任务结果 | HL 更新是否让原任务从失败状态进入更可接受的行为区间？ | [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)、`/benchmark-summary.json` | `npm run benchmark:summary:check`、`npm run examples:reports:check` |
| 失败隔离 | 反馈是否把错误缩小到可更新的 heuristic target？ | `/example-registry.json`、[研究命题](/zh-cn/theory/research-propositions)、[案例矩阵](/zh-cn/appendix/case-registry) | `npm run examples:registry:check`、`npm run cases:check` |
| 更新成本 | 一次 patch 需要修改多少知识、代码或控制参数？ | `templates/experiment-record.md`、`templates/anti-forgetting-checklist.md`、[研究课题](/zh-cn/appendix/research-projects) | `npm run research:projects:check`、`npm run checkpoints:check` |
| 回归风险 | 新 heuristic 是否保护旧经验？ | `tests/`、[Lab 2](/zh-cn/slides/lab-2/)、[可复现性检查清单](/zh-cn/appendix/reproducibility) | `npm run examples:test`、`npm run verify` |
| 来源边界 | 案例来源状态是否足以支撑声明强度？ | [来源登记](/zh-cn/appendix/source-registry)、`/case-registry.json`、`/x-sources.json` | `npm run source:registry:check`、`npm run cases:check`、`npm run x:sources:check` |

## 如何使用

1. 读一个案例页或跑一个示例。
2. 打开 `/evaluation-metrics.json`，找到绑定的 `example_ids` 和 `claim_ids`。
3. 先用任务结果判断行为变化，再用失败隔离判断是否找到了可更新对象。
4. 如果要提出新 patch，必须补更新成本和回归风险。
5. 如果案例来自 X、私有来源或二手资料，先补来源边界，不要直接写成复现事实。

## 学习规则

1. 新增主线示例时，至少要进入任务结果、失败隔离和回归风险之一。
2. 新增研究命题时，至少要绑定一个评估指标，说明它如何被反驳。
3. 修改 benchmark、case registry、X 来源或研究项目时，同步检查 `/evaluation-metrics.json`。
4. 如果一个指标暂时只能作为研究假设，文档里必须保留边界说明。

```bash
npm run metrics:check
npm run verify
```
