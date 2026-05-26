---
title: 学习单元矩阵
description: Heuristic Learning 课程章节的读、跑、改、复盘闭环
---

# 学习单元矩阵

本页把 HL 课程从“页面列表”收束成可执行学习单元。每个单元都必须回答四件事：读什么、跑什么、改什么、交付什么。这样读者不会只停留在理论页，也不会只跑示例而不知道它支持哪个研究问题。

机器可读矩阵见 [`/learning-units.json`](/learning-units.json)，字段约束见 [`/learning-units.schema.json`](/learning-units.schema.json)。`npm run learning:units:check` 会检查每个单元的阅读页、示例、命令、交付物和验收命令是否仍然存在。

## 单元设计原则

| 原则 | 要求 |
| --- | --- |
| 先读后跑 | 每个单元至少有一个理论页或案例页作为阅读入口 |
| 跑出失败 | 每个动手单元必须能观察 baseline failure 或 feedback report |
| 修改有边界 | 改动目标必须是策略、阈值、测试、case card 或实验记录，不是随意重构 |
| 复盘可检查 | 每个单元都要产生可审查交付物，并给出验收命令 |

## 课程单元

| 单元 | 核心问题 | 阅读 | 动手命令 | 交付物 |
| --- | --- | --- | --- | --- |
| U0 建立语境 | HL 为什么值得作为学习对象？ | [学习路线](/zh-cn/stage-1/)、[HL 基础概念](/zh-cn/stage-2/)、[文献阅读指南](/zh-cn/appendix/reading-guide) | `npm run claims:registry:check` | 一页概念图或术语解释 |
| U1 最小闭环 | 如何从失败 probe 到 feedback report？ | [学习闭环](/zh-cn/theory/learning-loop)、[可运行示例](/zh-cn/examples/)、[Lab 1](/zh-cn/slides/lab-1/) | `npm run examples:gridworld:feedback` | GridWorld 实验记录 |
| U2 公开 artifact | 如何把 Jiayi artifact 压缩成轻量 replay？ | [案例库](/zh-cn/cases/)、[VizDoom 案例](/zh-cn/cases/vizdoom/)、[Breakout 案例](/zh-cn/cases/breakout/) | `npm run examples:vizdoom-replay:feedback`、`npm run examples:breakout-replay:feedback` | 一张 case card |
| U3 控制与系统约束 | 连续控制和工程系统里 HL 更新什么？ | [Ant Gait 案例](/zh-cn/cases/ant-gait/)、[交通模拟案例](/zh-cn/cases/traffic-simulation/)、[实验协议](/zh-cn/appendix/benchmark-protocol) | `npm run examples:ant-gait-replay:feedback`、`npm run examples:traffic-grid:feedback` | failure mode 对照表 |
| U4 研究问题 | 当前证据支持哪些研究问题，边界在哪里？ | [研究框架](/zh-cn/theory/research-framework)、[研究问题](/zh-cn/theory/research-framework)、[论文蓝图](/zh-cn/appendix/paper-blueprint) | `npm run claims:registry:check`、`npm run paper:blueprint:check` | 研究问题-证据-反驳路径说明 |
| U5 反遗忘项目 | 一次 HL 更新如何通过课程验收？ | [Lab 2](/zh-cn/slides/lab-2/)、[练习集](/zh-cn/appendix/exercises)、[课程 Rubric](/zh-cn/appendix/rubric) | `npm run examples:test`、`npm run verify` | anti-forgetting checklist 与 Rubric 自评 |

## 使用方式

建议按 U0 到 U5 顺序完成；授课时可以把每个单元拆成一次课堂或一次组会任务。编码智能体在维护仓库时，应优先查看 `/learning-units.json`，确认新增页面或示例是否改变了已有单元的阅读、命令或交付物。

新增或修改学习单元后，至少运行：

```bash
npm run learning:units:check
npm run course:structure:check
npm run verify
```
