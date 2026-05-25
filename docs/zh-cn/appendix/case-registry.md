---
title: 案例矩阵
description: Heuristic Learning 案例到来源、示例、学习成果和验证命令的映射
---

# 案例矩阵

本页把案例库从叙述页面推进成可检查的研究矩阵。它回答四个问题：

- 这个案例来自什么来源？
- 是否已经落到 runnable example？
- 它训练哪类学习成果？
- 用什么命令证明案例、示例和来源边界没有漂移？

机器可读矩阵见 [`/case-registry.json`](/case-registry.json)，字段约束见 [`/case-registry.schema.json`](/case-registry.schema.json)。`npm run cases:check` 会检查案例页、来源引用、示例 id、failure mode、学习成果和验证命令。

## 案例总览

| 案例 | 来源状态 | 示例 | 教学用途 | 验证命令 |
| --- | --- | --- | --- | --- |
| MuJoCo Ant Gait | 已复现为轻量 replay | `ant-gait-replay` | 连续控制、yaw feedback、反遗忘回归 | `npm run examples:ant-gait-replay:feedback` |
| Atari Breakout | 已复现为轻量 replay | `breakout-replay` | 物理预测、side-wall reflection、replay probe | `npm run examples:breakout-replay:feedback` |
| VizDoom Medikit Staging | 已复现为轻量 replay | `vizdoom-replay` | 感知阈值、medikit staging、轻量 replay | `npm run examples:vizdoom-replay:feedback` |
| Robot Soccer | 已复现为最小环境 | `robot-soccer` | 视觉规则库、blocked-lane probe、动作前提 | `npm run examples:robot-soccer:feedback` |
| Traffic Simulation | 已复现为最小环境 | `traffic-grid` | downstream capacity、系统安全约束、仿真 replay | `npm run examples:traffic-grid:feedback` |
| X and FieldTheory Signals | 已结构化 | 无直接示例 | 一手原帖、二手转述、公开 artifact 和研究假设分层 | `npm run x:sources:check` |

## 使用方式

学生做案例作业时：

1. 从 [案例库](/zh-cn/cases/) 选一个案例页。
2. 打开 `/case-registry.json`，确认它绑定的 `example_id`、`failure_mode` 和 `learning_outcome_ids`。
3. 跑对应 feedback 命令，阅读 `experiments/*/latest.json`。
4. 用 [学习成果矩阵](/zh-cn/appendix/learning-outcomes) 和 [Rubric](/zh-cn/appendix/rubric) 写自评。

研究者扩展案例时：

1. 先更新 [来源登记](/zh-cn/appendix/source-registry)，保留“已复现、已结构化、已定位、待采集”的状态。
2. 如果新增 runnable example，同步 `example-registry`、测试、报告和课程页。
3. 如果只是来源线索，只能绑定为无直接示例的 case card，不得写成已复现。
4. 最后运行：

```bash
npm run cases:check
npm run examples:test
npm run examples:ant-gait-replay:feedback
npm run examples:breakout-replay:feedback
npm run examples:vizdoom-replay:feedback
npm run examples:robot-soccer:feedback
npm run examples:traffic-grid:feedback
npm run source:registry:check
npm run x:sources:check
npm run verify
```

## 边界

- 案例矩阵不是来源原文库；公开仓库不保存飞书原文、X cookie、私有日志或未脱敏截图。
- `已复现为轻量 replay` 只能说明课程 probe 已经保留核心 failure mode，不能等同于真实环境高保真复现。
- 没有 runnable example 的 X 线索仍可进入案例矩阵，但只能作为来源抽取训练材料。

当前案例边界：

- 当前是轻量 replay，不等同于真实 MuJoCo Ant 高保真复现。
- 当前不包含 Atari 环境、RAM 解码、视觉分割或真实视频渲染。
- 当前移除了 EnvPool/OpenCV，只保留可讲授的检测字段和时机策略。
- 公开仓库只保留脱敏最小环境，不公开飞书原文或真实机器人日志。
- 当前不是东湖真实仿真接口，只是脱敏后的容量约束最小环境。
- 未通过 ft、X API 或公开 URL 复核的内容不能写成已复现事实。
