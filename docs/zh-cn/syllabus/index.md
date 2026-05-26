---
title: 课程大纲
description: Heuristic Learning 课程章节、案例、命令和验证产物总览
---

# 课程大纲

本页把 HL 整理成一张学习与验证地图。学习顺序是：先建立概念，再跑通闭环，随后阅读案例、修改策略、检查回归，最后把一次更新复盘成可讨论的研究问题。

## 总体结构

| 单元 | 核心问题 | 配套材料 | 可验证产物 |
| --- | --- | --- | --- |
| 0. 建立概念 | HL 为什么不是“手写规则”的旧瓶装新酒？ | [课程地图](/zh-cn/course-map/)、[学习路线](/zh-cn/stage-1/)、[HL 基础概念](/zh-cn/stage-2/) | 能解释状态、动作、反馈、更新对象 |
| 1. 跑通闭环 | 一个规则系统如何从反馈中被维护？ | [学习闭环](/zh-cn/theory/learning-loop)、[可运行示例](/zh-cn/examples/)、[Lab 1](/zh-cn/slides/lab-1/) | `npm run verify` |
| 2. 对照理论 | HL 如何区别于 RL 和 DL？ | [从 RL/DL 到 HL](/zh-cn/stage-3/)、[研究框架](/zh-cn/theory/research-framework)、[研究命题](/zh-cn/theory/research-propositions) | 能把案例映射到度量表 |
| 3. 阅读案例 | 公开 artifact、脱敏应用案例和 X 来源如何形成研究问题？ | [案例库](/zh-cn/cases/)、[来源登记](/zh-cn/appendix/source-registry)、[来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook) | case card + source status |
| 4. 修改验证 | 如何让 heuristic patch 被测试、报告和回归检查约束？ | [代码导览](/zh-cn/appendix/code-tour)、[第 1 讲](/zh-cn/slides/lecture-1/)、[第 2 讲](/zh-cn/slides/lecture-2/)、[第 3 讲](/zh-cn/slides/lecture-3/)、[Lab 2](/zh-cn/slides/lab-2/) | report + regression test |
| 5. 复盘扩展 | 如何把一次更新写成可反驳、可复现的学习问题？ | [练习集](/zh-cn/appendix/exercises)、[实验协议](/zh-cn/appendix/benchmark-protocol)、[课程 Rubric](/zh-cn/appendix/rubric)、[研究课题](/zh-cn/appendix/research-projects) | anti-forgetting checklist + 复盘记录 |

## 可运行实验矩阵

| 实验 | 来源状态 | baseline failure | heuristic patch | 运行命令 | 反馈产物 |
| --- | --- | --- | --- | --- | --- |
| GridWorld | 最小教学环境 | `local_greedy_trap` | 显式避开已知陷阱 | `npm run examples:gridworld` | `experiments/gridworld/latest.json` |
| Ant Gait Replay | 公开 artifact，已复现为轻量 replay | `yaw_drift` | 速度自适应 CPG + stance duty + yaw feedback | `npm run examples:ant-gait-replay` | `experiments/ant-gait-replay/latest.json` |
| Breakout Replay | 公开 artifact，已复现为轻量 replay | `missed_after_wall_reflection` | 预测侧墙反射后的挡板截点 | `npm run examples:breakout-replay` | `experiments/breakout-replay/latest.json` |
| Robot Soccer | 脱敏应用案例，已复现为最小环境 | `blocked_shot` | 射门前检查通道并换线 | `npm run examples:robot-soccer` | `experiments/robot-soccer/latest.json` |
| VizDoom Replay | 公开 artifact，已复现为轻量 replay | `wasted_pickup` | 血量高时 staged wait | `npm run examples:vizdoom-replay` | `experiments/vizdoom-replay/latest.json` |
| Traffic Grid | 脱敏应用案例，已复现为最小环境 | `spillback` | 保护下游容量再放行 | `npm run examples:traffic-grid` | `experiments/traffic-grid/latest.json` |

统一生成反馈：

```bash
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run teaching:registry:check
npm run course:structure:check
```

## 统一学习路径

1. 读 [学习路线](/zh-cn/stage-1/) 和 [HL 基础概念](/zh-cn/stage-2/)，先写出 HL 的反馈、更新对象和验证方式。
2. 跑 `npm run examples:gridworld`，观察 baseline 为什么会在 `local_greedy_trap` 失败。
3. 跑 `npm run examples:gridworld:feedback`，读懂 `experiments/gridworld/latest.json` 如何记录下一轮更新。
4. 阅读 [从 RL/DL 到 HL](/zh-cn/stage-3/)，确认 HL 不是反向传播替代品，而是软件结构的更新过程。
5. 从 [案例库](/zh-cn/cases/) 选择一个案例，写出来源状态、failure mode、baseline 和 heuristic patch。
6. 打开 [代码导览](/zh-cn/appendix/code-tour)，只改一个策略更新点。
7. 运行 `npm run examples:test` 和对应 feedback 命令，确认旧 probe 没有退化。
8. 完成 [Lab 2](/zh-cn/slides/lab-2/)，用 [课程 Rubric](/zh-cn/appendix/rubric) 自查证据链。
9. 最后跑 `npm run verify`，把代码、报告和文档一起验收。

## 当前覆盖与缺口

| 维度 | 当前覆盖 | 下一步 |
| --- | --- | --- |
| 理论 | 基础概念、学习闭环、RL/DL/HL 对照、研究框架 | 扩展泛化、遗忘、维护成本度量 |
| 实验 | 6 个纯 Python 最小环境 | 增加真实 MuJoCo 高保真验证 |
| 案例 | Ant、Breakout、VizDoom、机器人足球、交通模拟、X 来源 | 继续补公开来源复核和高保真实验 |
| 学习材料 | 第 1 讲、第 2 讲、第 3 讲、Lab 1、Lab 2、练习集、研究课题、实验协议与 Rubric | 继续拆成 4-5 讲课程 |
| 验证 | tests、feedback report、report schema、VitePress build、页面路由和视觉验收 | 持续补充真实环境复验 |

更具体的版本路线见 [研究路线图](/zh-cn/appendix/research-roadmap)。任何新增章节如果不能落到来源、实验或验证产物，就还不应该进入主线课程。

结构一致性由 `npm run course:structure:check` 检查：它会确认课程页面、示例目录、package scripts、实验报告、测试文件和本页矩阵没有漂移。
章节级“读、跑、改、复盘”闭环见 [学习单元矩阵](/zh-cn/appendix/learning-units)，阶段自测见 [阶段检查点](/zh-cn/appendix/checkpoints)。机器可读入口为 [`/learning-units.json`](/learning-units.json) 和 [`/checkpoint-registry.json`](/checkpoint-registry.json)。
机器可读入口见 [`/course-manifest.json`](/course-manifest.json)，其中列出核心页面、六个示例、报告路径和 CI 验证入口；字段约束见 [`/course-manifest.schema.json`](/course-manifest.schema.json)。示例专用矩阵见 [`/example-registry.json`](/example-registry.json) 和 [`/example-registry.schema.json`](/example-registry.schema.json)；benchmark 摘要见 [`/benchmark-summary.json`](/benchmark-summary.json) 和 [`/benchmark-summary.schema.json`](/benchmark-summary.schema.json)；讲义与 lab 矩阵见 [`/teaching-registry.json`](/teaching-registry.json) 和 [`/teaching-registry.schema.json`](/teaching-registry.schema.json)。
