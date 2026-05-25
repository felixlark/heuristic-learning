---
title: 课程大纲
description: Heuristic Learning 课程章节、案例、命令和验证产物总览
---

# 课程大纲

本页把 HL 仓库整理成一张学习与验证地图。学生可以按章节学习，AI 研究者可以按案例扩展，工程师可以按示例和测试改代码，编码智能体可以按命令验证。

## 总体结构

| 单元 | 核心问题 | 配套材料 | 可验证产物 |
| --- | --- | --- | --- |
| 0. 建立直觉 | HL 为什么不是“手写规则”的旧瓶装新酒？ | [课程地图](/zh-cn/course-map/)、[学习路线](/zh-cn/stage-1/)、[HL 基础概念](/zh-cn/stage-2/) | 能解释状态、动作、反馈、更新对象 |
| 1. 跑通闭环 | 一个规则系统如何从反馈中被维护？ | [可运行示例](/zh-cn/examples/)、[Lab 1](/zh-cn/slides/lab-1/) | `npm run verify` |
| 2. 形成理论 | HL 如何定义问题、度量与边界？ | [学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework)、[研究命题](/zh-cn/theory/research-propositions)、[从 RL/DL 到 HL](/zh-cn/stage-3/) | 能把案例映射到度量表 |
| 3. 沉淀案例 | 公开 artifact 与内部线索如何进入课程？ | [案例库](/zh-cn/cases/)、[来源登记](/zh-cn/appendix/source-registry) | case card + source status |
| 4. 课程表达 | 如何把研究材料讲给学生或组会？ | [第 1 讲](/zh-cn/slides/lecture-1/)、[第 2 讲](/zh-cn/slides/lecture-2/)、[第 3 讲](/zh-cn/slides/lecture-3/)、[Lab 1](/zh-cn/slides/lab-1/)、[Lab 2](/zh-cn/slides/lab-2/)、[教师指南](/zh-cn/appendix/instructor-guide)、[课程进度表](/zh-cn/appendix/course-schedule)、[教学仓库对标](/zh-cn/appendix/course-patterns)、[练习集](/zh-cn/appendix/exercises)、[研究课题](/zh-cn/appendix/research-projects)、[实验协议](/zh-cn/appendix/benchmark-protocol)、[课程 Rubric](/zh-cn/appendix/rubric) | 讲义 + lab 记录 |

## 可运行实验矩阵

| 实验 | 来源状态 | baseline failure | heuristic patch | 运行命令 | 反馈产物 |
| --- | --- | --- | --- | --- | --- |
| GridWorld | 本仓库最小教学环境 | `local_greedy_trap` | 显式避开已知陷阱 | `npm run examples:gridworld` | `experiments/gridworld/latest.json` |
| Ant Gait Replay | 公开 artifact，已复现为轻量 replay | `yaw_drift` | 速度自适应 CPG + stance duty + yaw feedback | `npm run examples:ant-gait-replay` | `experiments/ant-gait-replay/latest.json` |
| Breakout Replay | 公开 artifact，已复现为轻量 replay | `missed_after_wall_reflection` | 预测侧墙反射后的挡板截点 | `npm run examples:breakout-replay` | `experiments/breakout-replay/latest.json` |
| Robot Soccer | 飞书线索，已复现为最小环境 | `blocked_shot` | 射门前检查通道并换线 | `npm run examples:robot-soccer` | `experiments/robot-soccer/latest.json` |
| VizDoom Replay | 公开 artifact，已复现为轻量 replay | `wasted_pickup` | 血量高时 staged wait | `npm run examples:vizdoom-replay` | `experiments/vizdoom-replay/latest.json` |
| Traffic Grid | 飞书线索，已复现为最小环境 | `spillback` | 保护下游容量再放行 | `npm run examples:traffic-grid` | `experiments/traffic-grid/latest.json` |

统一生成反馈：

```bash
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run teaching:registry:check
npm run course:structure:check
```

## 学习路径

### 学生路径

1. 读 [学习路线](/zh-cn/stage-1/)。
2. 跑 `npm run verify`。
3. 完成 [Lab 1](/zh-cn/slides/lab-1/)。
4. 选一个案例页，解释它的 baseline failure 和 heuristic patch。
5. 写一份 `templates/experiment-record.md` 风格的复盘，并按 [课程 Rubric](/zh-cn/appendix/rubric) 自查。

### 研究者路径

1. 读 [学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework) 与 [研究命题](/zh-cn/theory/research-propositions)。
2. 查 [来源登记](/zh-cn/appendix/source-registry)，确认哪些来源已复现、哪些只是线索。
3. 用 `templates/case-card.md` 新增一个案例。
4. 尽量把案例压缩成 `examples/*` 里的最小可运行环境。
5. 用 `npm run verify` 证明代码、反馈报告和文档可以一起构建。

### 工程师路径

1. 从 [可运行示例](/zh-cn/examples/) 选一个小环境，不先读完整附录。
2. 跑对应命令，例如 `npm run examples:breakout-replay`。
3. 打开 [代码导览](/zh-cn/appendix/code-tour)，只改一个策略更新点。
4. 运行 `npm run examples:test` 和对应 feedback 命令，确认旧 probe 没有退化。
5. 最后再跑 `npm run verify`，把代码、报告和文档一起验收。

### 编码智能体路径

1. 读取 `llms.txt`。
2. 查看 `experiments/*/latest.json` 中的 `candidate_update`。
3. 先补测试，再修改策略。
4. 运行 `npm run verify`。
5. 更新相关案例页、来源登记和实验记录。

## 当前覆盖与缺口

| 维度 | 当前覆盖 | 下一步 |
| --- | --- | --- |
| 理论 | 基础概念、学习闭环、RL/DL/HL 对照、研究框架 | 扩展泛化、遗忘、维护成本度量 |
| 实验 | 6 个纯 Python 最小环境 | 增加真实 MuJoCo 高保真验证 |
| 案例 | Ant、Breakout、VizDoom、机器人足球、交通模拟、X 线索 | 继续补 Jiayi 原帖 thread 和后续应用卡片 |
| 课程 | 第 1 讲、第 2 讲、第 3 讲、Lab 1、Lab 2、教师指南、课程进度表、练习集、研究课题、实验协议与 Rubric | 继续拆成 4-5 讲课程 |
| 验证 | tests、feedback report、report schema、VitePress build、Browser/IAB 视觉验收、GitHub Pages 部署 | 后续维护 GitHub Actions 与 Pages 真实路由 |

更具体的版本路线见 [研究路线图](/zh-cn/appendix/research-roadmap)。任何新增章节如果不能落到来源、实验或验证产物，就还不应该进入主线课程。

结构一致性由 `npm run course:structure:check` 检查：它会确认课程页面、示例目录、package scripts、实验报告、测试文件和本页矩阵没有漂移。
章节级“读、跑、改、复盘”闭环见 [学习单元矩阵](/zh-cn/appendix/learning-units)，阶段自测见 [阶段检查点](/zh-cn/appendix/checkpoints)。机器可读入口为 [`/learning-units.json`](/learning-units.json) 和 [`/checkpoint-registry.json`](/checkpoint-registry.json)。
机器可读入口见 [`/course-manifest.json`](/course-manifest.json)，其中列出核心页面、六个示例、报告路径和 CI 验证入口；字段约束见 [`/course-manifest.schema.json`](/course-manifest.schema.json)。示例专用矩阵见 [`/example-registry.json`](/example-registry.json) 和 [`/example-registry.schema.json`](/example-registry.schema.json)；benchmark 摘要见 [`/benchmark-summary.json`](/benchmark-summary.json) 和 [`/benchmark-summary.schema.json`](/benchmark-summary.schema.json)；讲义与 lab 矩阵见 [`/teaching-registry.json`](/teaching-registry.json) 和 [`/teaching-registry.schema.json`](/teaching-registry.schema.json)；教学仓库对标矩阵见 [`/course-patterns.json`](/course-patterns.json) 和 [`/course-patterns.schema.json`](/course-patterns.schema.json)。
