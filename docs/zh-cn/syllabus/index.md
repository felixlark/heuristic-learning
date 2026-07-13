---
title: 课程大纲
description: Heuristic Learning 的单元目标、实验命令、交付物和通过标准
---

# 课程大纲

本页回答“每个学习单元具体怎么学、怎么做、怎样算通过”。如果只想先获得全局路线，先看 [课程地图](/zh-cn/course-map/)；回到本页时，按单元完成阅读、实验、记录和复盘。

## 使用方式

每个单元都按同一节奏推进：

1. 课前读：先理解本单元要解决的概念问题。
2. 课中做：运行最小实验或阅读一个案例证据。
3. 课后交付：把观察写成可复查的记录。
4. 通过标准：用命令、报告、测试或 Rubric 检查是否完成。

学习时不要跳过交付物。HL 的核心不是记住术语，而是把一次失败、一次规则更新和一次回归检查连成证据链。

## 单元安排

| 单元 | 课前读 | 课中做 | 课后交付 | 通过标准 |
| --- | --- | --- | --- | --- |
| 0. 建立概念 | [学习路线](/zh-cn/stage-1/)、[HL 基础概念](/zh-cn/stage-2/) | 用自己的话区分 state、action、feedback、update target、verification | 一页术语笔记 | 能解释 HL 为什么不是“手写规则”的旧瓶装新酒 |
| 1. 跑通最小闭环 | [学习闭环](/zh-cn/theory/learning-loop)、[可运行示例](/zh-cn/examples/)、[Lab 1](/zh-cn/examples/) | 运行 GridWorld，定位 `local_greedy_trap` | GridWorld 实验记录 | `npm run examples:gridworld` 和 `npm run examples:gridworld:feedback` 通过，并生成 `experiments/gridworld/latest.json` |
| 2. 对照 RL / DL / HL | [从 RL/DL 到 HL](/zh-cn/stage-3/)、[研究框架](/zh-cn/theory/research-framework) | 把一个案例拆成状态、动作、反馈、patch、regression | 一张 RL/DL/HL 对照表 | 能说明这个问题适合改权重、改策略，还是改系统结构 |
| 3. 阅读案例证据 | [案例库](/zh-cn/cases/)、[来源登记](/zh-cn/appendix/source-registry)、[来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook) | 选择一个公开 artifact、脱敏应用案例或 X 来源，写出来源状态 | case card + source status | 能区分已复现、轻量 replay、待验证线索和研究假设 |
| 4. 修改并验证策略 | [代码导览](/zh-cn/appendix/code-tour)、[第 1 讲](/zh-cn/talk/)、[第 2 讲](/zh-cn/talk/)、[第 3 讲](/zh-cn/talk/)、[Lab 2](/zh-cn/theory/learning-loop) | 只改一个策略点，并补充或复用回归检查 | report + regression test | `npm run examples:test` 和对应 feedback 命令通过 |
| 5. 复盘成研究问题 | [练习集](/zh-cn/appendix/exercises)、[实验协议](/zh-cn/appendix/benchmark-protocol)、[课程 Rubric](/zh-cn/appendix/rubric)、[研究课题](/zh-cn/appendix/research-projects) | 用证据、反例和下一步实验重写一次更新 | anti-forgetting checklist + 复盘记录 | 能把更新写成可反驳、可复现的学习问题，并通过 `npm run verify` |

## 实验命令

先跑一个最小闭环，再扩展到六个示例。

```bash
npm run examples:gridworld
npm run examples:gridworld:feedback
npm run examples:test
```

完整实验矩阵：

| 实验 | 学习重点 | baseline failure | 运行命令 | 反馈产物 |
| --- | --- | --- | --- | --- |
| GridWorld | 最小 HL 闭环 | `local_greedy_trap` | `npm run examples:gridworld` | `experiments/gridworld/latest.json` |
| Robot Soccer | 动作前提与通道检查 | `blocked_shot` | `npm run examples:robot-soccer` | `experiments/robot-soccer/latest.json` |
| VizDoom Replay | 资源时机与轻量 replay | `wasted_pickup` | `npm run examples:vizdoom-replay` | `experiments/vizdoom-replay/latest.json` |
| Traffic Grid | 系统容量与安全约束 | `spillback` | `npm run examples:traffic-grid` | `experiments/traffic-grid/latest.json` |
| Breakout Replay | 物理预测与 replay probe | `missed_after_wall_reflection` | `npm run examples:breakout-replay` | `experiments/breakout-replay/latest.json` |
| Ant Gait Replay | 连续控制与可审查参数 | `yaw_drift` | `npm run examples:ant-gait-replay` | `experiments/ant-gait-replay/latest.json` |

统一生成和检查反馈：

```bash
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run course:structure:check
```

## 交付物模板

| 交付物 | 必须包含 | 可参考页面 |
| --- | --- | --- |
| 术语笔记 | feedback、update target、verification、regression 的定义 | [术语表](/zh-cn/appendix/glossary) |
| 实验记录 | 命令、环境、baseline failure、结果、候选更新 | [实验记录模板](https://github.com/felixlark/heuristic-learning/blob/main/templates/experiment-record.md) |
| case card | 来源、环境、策略表面、验证路径、课程链接 | [案例矩阵](/zh-cn/appendix/case-registry) |
| 回归检查 | 旧行为、风险更新、regression guard、审查结果 | [反遗忘清单](https://github.com/felixlark/heuristic-learning/blob/main/templates/anti-forgetting-checklist.md) |
| 研究问题 | 证据、反例、边界、下一步实验 | [研究问题](/zh-cn/theory/research-framework) |

## 通过标准

完成本课程的最低标准：

1. 能解释 HL 的更新对象为什么是软件结构，而不是神经网络权重。
2. 至少跑通一个示例、一个 feedback report 和对应测试。
3. 至少阅读一个案例，并写清来源状态和验证边界。
4. 至少完成一次单点 heuristic update，并检查旧 probe 没有退化。
5. 用 Rubric 自查一次交付物，最后运行完整验证。

```bash
npm run verify
```

扩展学习可以继续完成 [练习集](/zh-cn/appendix/exercises) 和 [研究课题](/zh-cn/appendix/research-projects)。章节级“读、跑、改、复盘”矩阵见 [学习单元矩阵](/zh-cn/appendix/learning-units)，阶段自测见 [阶段检查点](/zh-cn/appendix/checkpoints)。

## 当前覆盖与缺口

| 维度 | 当前覆盖 | 下一步 |
| --- | --- | --- |
| 理论 | 基础概念、学习闭环、RL/DL/HL 对照、研究框架 | 扩展泛化、遗忘、维护成本度量 |
| 实验 | 6 个纯 Python 最小环境 | 增加真实 MuJoCo 高保真验证 |
| 案例 | Ant、Breakout、VizDoom、机器人足球、交通模拟、X 来源 | 继续补公开来源复核和高保真实验 |
| 学习材料 | 第 1 讲、第 2 讲、第 3 讲、Lab 1、Lab 2、练习集、研究课题、实验协议与 Rubric | 继续拆成更多讲次和作业 |
| 验证 | tests、feedback report、report schema、VitePress build、页面路由和视觉验收 | 持续补充真实环境复验 |

更具体的版本路线见 [研究路线图](/zh-cn/appendix/research-roadmap)。任何新增章节如果不能落到来源、实验或验证产物，就还不应该进入主线课程。

机器可读入口见 [`/course-manifest.json`](/course-manifest.json)、[`/learning-units.json`](/learning-units.json)、[`/checkpoint-registry.json`](/checkpoint-registry.json)、[`/example-registry.json`](/example-registry.json) 和 `/course-manifest.json`。
