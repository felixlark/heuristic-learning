---
title: 研究课题
description: Heuristic Learning 的课程项目、研究问题和验收产物
---

# 研究课题

本页把 HL 的理论假设转成项目制学习任务。每个项目都必须绑定一个来源、一个 failure mode、一个可运行示例或案例页，以及一条统一验证命令。项目的目标不是“写更多规则”，而是证明一次规则更新如何被记录、复查和维护。

课堂练习和作业题库见 [练习集](/zh-cn/appendix/exercises)。本页更偏研究项目菜单，练习集更偏课程作业分层。

机器可读项目矩阵见 [`/research-projects.json`](/research-projects.json)，字段约束见 [`/research-projects.schema.json`](/research-projects.schema.json)。`npm run research:projects:check` 会检查每个项目是否绑定来源、failure mode、示例、交付物、验证命令和课程落点。

## 项目选择原则

| 原则 | 要求 |
| --- | --- |
| 有来源 | 来自公开 artifact、X 来源、脱敏应用问题或课程实验 |
| 有失败 | 必须有 baseline failure，不能只展示成功路径 |
| 有更新对象 | 能明确修改代码、阈值、检测器、配置、测试或实验记录 |
| 有验证 | 至少能跑一个示例命令、一个测试命令和 `npm run verify`，并符合 [实验协议](/zh-cn/appendix/benchmark-protocol) |
| 有学习复盘 | 最终产物能进入案例页、讲义、Rubric 或来源登记 |

如果一个想法暂时没有来源或可复现失败，它应该先进入 [来源登记](/zh-cn/appendix/source-registry)，不要直接进入主线项目。

## 入门项目

| 项目 | 起点 | 研究问题 | 交付物 | 验证 |
| --- | --- | --- | --- | --- |
| GridWorld 新 probe | `examples/heuristic-gridworld/` | 一个局部陷阱是否能被显式规则稳定规避？ | 新 probe、测试、反馈报告说明 | `npm run examples:test` |
| Robot Soccer 通道检查 | `examples/robot-soccer/` | 射门前检查通道是否比直接射门更可维护？ | case card、blocked-lane 扩展场景 | `npm run examples:robot-soccer:feedback` |
| Traffic Grid 安全约束 | `examples/traffic-grid/` | 下游容量应作为硬约束还是 reward 项？ | 实验记录、阈值敏感性说明 | `npm run examples:traffic-grid:feedback` |
| Constraint Audit 证据边界 | `examples/constraint-audit/` | 事实约束审计能否成为可维护反馈通道？ | 原子主张夹具、证据升级规则、反例说明 | `npm run examples:constraint-audit:feedback` |

入门项目适合 90 分钟导读或 2 小时工作坊。评分重点是是否能复述 signal、probe、patch、report 和 regression，而不是策略是否复杂。

## 公开 Artifact 项目

| 项目 | 起点 | 研究问题 | 交付物 | 验证 |
| --- | --- | --- | --- | --- |
| Breakout 反射预测 | `examples/breakout-replay/` | 几何预测如何从 Atari artifact 压缩为课程 replay？ | 字段映射表、replay 说明、测试 | `npm run examples:breakout-replay:feedback` |
| VizDoom Medikit Staging | `examples/vizdoom-replay/` | 视觉检测阈值如何转成可审计的等待策略？ | 来源对照、阈值边界、report | `npm run examples:vizdoom-replay:feedback` |
| Ant Gait 稳定性 | `examples/ant-gait-replay/` | 连续控制里的 heuristic update 是否仍然可 review？ | 控制参数说明、yaw probe、测试 | `npm run examples:ant-gait-replay:feedback` |

公开 artifact 项目必须引用 `Trinkle23897/learning-beyond-gradients` 的对应文件，但课程版 replay 不能假装等同于真实环境复现。高保真验证应作为可选扩展，并保持轻量 replay 的测试稳定。

## 研究型项目

| 项目 | 研究假设 | 可观察证据 | 最小验收 |
| --- | --- | --- | --- |
| 反馈格式比较 | JSON report 是否比自然语言日志更适合下一轮智能体维护？ | 同一 failure mode 的两种反馈记录 | 至少一个脚本能读取结构化字段 |
| 反遗忘测试集 | HL 是否会发生工程型遗忘？ | 新 patch 破坏旧 probe 的复现实验 | 新增一个回归测试和说明 |
| 更新成本度量 | 编码智能体是否降低 heuristic system 维护成本？ | 修改文件数、测试数、失败复盘时间 | 一个 experiment record 记录成本字段 |
| 混合系统边界 | DL/RL 与 HL 如何分工？ | 感知、策略、异常处理的边界表 | 理论页或案例页落点 |

研究型项目可以没有新环境，但必须增加可验证的研究 artifact，例如测试、报告 schema、案例卡、度量表或结构检查规则。讨论研究问题时使用 `templates/claim-review.md`，讨论工程型遗忘时使用 `templates/anti-forgetting-checklist.md`，避免只留下不可复查的口头判断。

## 项目矩阵命令

机器可读项目矩阵会把页面中的单条验收命令扩展成完整检查组合。当前允许的项目级命令包括：

```bash
npm run examples:gridworld:feedback
npm run examples:robot-soccer:feedback
npm run examples:traffic-grid:feedback
npm run examples:constraint-audit:feedback
npm run examples:breakout-replay:feedback
npm run examples:vizdoom-replay:feedback
npm run examples:ant-gait-replay:feedback
npm run examples:reports:check
npm run examples:test
npm run claims:registry:check
npm run verify
```

## Capstone 项目

一个完整 capstone 应该交付：

```text
1. 来源登记条目
2. case card 或案例页
3. runnable example 或固定 replay
4. baseline failure 与 heuristic patch
5. feedback report
6. regression test
7. 课程讲义或 Lab 任务
8. npm run verify 结果
```

建议路径：

1. 从 [来源登记](/zh-cn/appendix/source-registry) 选一个 `已定位` 或 `待采集` 线索。
2. 用 `templates/case-card.md` 写清楚状态、动作、反馈和更新对象。
3. 先做最小 replay，不急着接真实环境。
4. 写 baseline，让 failure mode 稳定出现。
5. 写 heuristic patch，并把维护风险写进 feedback report。
6. 增加测试和课程页链接。
7. 跑 `npm run verify`。

## 与 Rubric 的关系

[课程 Rubric](/zh-cn/appendix/rubric) 是评分标准，本页是项目菜单，[实验协议](/zh-cn/appendix/benchmark-protocol) 负责规定 baseline、probe、report 和 regression gate，[消融计划](/zh-cn/appendix/ablation-plan) 负责说明下一步变量对照。一个项目是否合格，最终仍按 Rubric 的五个维度验收：来源与问题定义、probe 与 baseline、heuristic patch、反馈报告、回归验证与学习复盘。

项目完成后，如果它没有进入来源登记、案例页、示例、报告、测试或课程页之一，就还只是个人笔记，不是课程的一部分。

维护本页或项目矩阵后运行：

```bash
npm run research:projects:check
npm run verify
```
