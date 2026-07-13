---
title: 学习路线
description: 直觉学习课程的分阶段学习地图
---

# 学习路线

HL 适合用“先跑起来，再回到理论”的方式学习。原因很简单：如果只谈概念，HL 很容易被误解成“手写规则”；如果只看代码，又容易忽略它真正关心的是可维护的学习闭环。

如果你想先看全局地图，打开 [课程大纲](/zh-cn/syllabus/)；如果你想直接动手，从阶段 1 开始。

本地环境或验证失败时，先看 [本地运行与排错](/zh-cn/appendix/local-setup)。不要在反馈通道不可信时修改策略代码。

## 阶段 0：建立直觉

目标：知道 HL 解决的不是“如何训练神经网络”，而是“如何让程序化策略在反馈中持续改进”。

必读：

- Jiayi Weng 的 [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/)
- [HL 基础概念](/zh-cn/stage-2/)

产出：

- 能用自己的话解释 HL 与 Heuristic System 的区别。
- 能画出状态、动作、反馈、更新对象的闭环。

## 阶段 1：跑通最小系统

目标：运行 `examples/heuristic-gridworld`、`examples/robot-soccer`、`examples/vizdoom-replay` 与 `examples/traffic-grid`，观察同一个环境中 baseline policy 与 heuristic policy 的差异。

命令：

```bash
npm run examples:gridworld
npm run examples:robot-soccer
npm run examples:robot-soccer:feedback
npm run examples:vizdoom-replay:feedback
npm run examples:traffic-grid:feedback
npm run examples:test
```

产出：

- 能指出策略代码里哪些规则构成 Heuristic System 的一部分。
- 能修改一条规则，并用测试确认没有破坏基础路径。
- 能完成 [Lab 1](/zh-cn/examples/) 的实验记录。

## 阶段 2：学习研究案例

目标：把公开案例转成结构化卡片。

当前优先案例：

- Atari / Breakout：高频反馈、视觉状态与策略微调。
- VizDoom：回放、失败场景与规则迭代。
- MuJoCo：连续控制中的规则边界。
- 机器人足球：脱敏应用案例，关注“视觉 YOLO + 手工 Rule 规则”的维护成本。
- 交通模拟：脱敏应用案例，关注规则库、仿真 replay 与人工管制经验。

## 阶段 3：形成研究问题

目标：把 HL 从“有趣现象”推进到可验证研究。

建议问题：

- 如何定义 HL 的泛化能力？
- 如何衡量规则维护成本下降？
- 如何防止规则堆叠导致的工程型遗忘？
- 什么样的环境适合 HL，什么样的环境仍应优先 Deep RL？
