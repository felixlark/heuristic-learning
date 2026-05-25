---
title: 案例库
description: Heuristic Learning 的案例、实验入口与证据边界
---

# 案例库

案例库把 Heuristic Learning 放到具体任务里学习。每个案例都按同一个模板阅读：

- 环境是什么？
- 状态如何表示？
- 策略如何写成代码？
- 反馈从哪里来？
- 智能体更新了什么？
- 如何验证没有退化？

读案例时重点看三件事：它的来源边界是什么、是否有可运行实验、验证命令能否复现同一个 failure mode。案例到来源、示例、学习成果和验证命令的对照见 [案例矩阵](/zh-cn/appendix/case-registry)。

## 公开主源

Jiayi Weng 的 [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) 与 [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) 是当前最高信号源。该仓库包含文章、Atari、MuJoCo、VizDoom 示例和渲染脚本，因此不仅是概念文章，也有实验 artifact。

## 应用案例：机器人足球

机器人足球适合用来理解“规则系统如何变成可学习系统”。一个典型系统已经有视觉检测、状态估计、动作接口和大量手工规则；难点不是完全没有策略，而是规则维护繁琐、冲突难查、迭代慢。[机器人足球案例](/zh-cn/cases/robot-soccer/) 把这个问题压缩成 blocked-lane 最小实验。

## 应用案例：交通模拟

交通模拟适合讨论规则库、仿真 replay 与人工管制经验如何进入 HL 闭环。[交通模拟案例](/zh-cn/cases/traffic-simulation/) 把真实路网问题先压缩成 downstream spillback：上游放行如果忽略下游容量，就会把拥堵推向更难恢复的位置。

## X 来源案例

X 是 Jiayi Weng 相关讨论的重要公开入口。[X 来源案例](/zh-cn/cases/x-signal/) 只抽取可验证的问题结构：哪些主张有公开文章或代码 artifact 支撑，哪些还只是待复核研究问题。

## v1 案例清单

| 案例 | 学习重点 | 可运行入口 |
| --- | --- | --- |
| MuJoCo / Ant Gait | yaw-stabilization 与可读控制器 | `npm run examples:ant-gait-replay` |
| Atari / Breakout | wall-reflection 与代码化经验记忆 | `npm run examples:breakout-replay` |
| X / Jiayi 公开讨论 | 来源层级、主张边界与研究问题 | `npm run x:sources:check` |
| VizDoom | medikit staging 与感知阈值 | `npm run examples:vizdoom-replay` |
| 机器人足球 | blocked-lane 与动作前提 | `npm run examples:robot-soccer` |
| 交通模拟 | downstream spillback 与容量约束 | `npm run examples:traffic-grid` |

案例矩阵由下面命令检查：

```bash
npm run cases:check
```
