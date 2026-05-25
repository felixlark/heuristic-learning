---
title: 第 1 讲：Learning Beyond Gradients
description: 直觉学习课程第 1 讲讲义
---

# 第 1 讲：Learning Beyond Gradients

## 本讲问题

神经网络可以通过梯度更新权重。那一个由代码、规则、测试、日志和回放组成的软件系统，能不能通过编码智能体持续变强？

学完这一讲，你应该能解释三件事：

- HL 的更新对象为什么不是参数，而是可维护的软件结构。
- 一个 heuristic 为什么必须和反馈、测试、日志或 replay 绑定。
- 一个最小 HL 闭环如何从失败开始，并以可复查的代码改动结束。

## HL 的最小定义

> Heuristic Learning 是由编码智能体消费反馈并维护软件结构的学习过程。

关键点：

- 更新对象不是神经网络参数，而是策略代码、状态检测器、测试、配置和记忆。
- 反馈可以来自环境奖励、测试失败、日志异常、视频回放或人类评审。
- 学习结果不是一条孤立规则，而是可维护的 Heuristic System。

## 一个最小学习闭环

```mermaid
flowchart LR
  feedback[反馈: reward / test / log / replay] --> agent[编码智能体]
  agent --> patch[修改策略/测试/记忆]
  patch --> run[重新运行]
  run --> record[记录实验]
  record --> feedback
```

这个闭环的重点不是“自动改代码”本身，而是让失败经验被压缩成下一轮可以读取、执行和验证的结构。

## 为什么现在值得研究

过去启发式规则维护成本高，所以常被视为临时补丁。编码智能体改变了维护成本：它可以读失败、改代码、补测试、复盘结果，让规则变成长期资产。

对研究者来说，HL 提供了一个介于手写规则、强化学习和深度学习之间的研究对象：系统可以学习，但学习轨迹表现为代码、测试和记忆的演化。对工程师来说，HL 的价值在于把“线上经验”沉淀成可维护规则。对学生来说，它是理解智能体如何利用反馈改进系统的低门槛入口。

## 可运行观察

```bash
npm run examples:gridworld
npm run examples:gridworld:feedback
npm run examples:robot-soccer:feedback
npm run examples:vizdoom-replay:feedback
npm run examples:traffic-grid:feedback
npm run examples:breakout-replay:feedback
npm run examples:ant-gait-replay:feedback
npm run examples:test
```

观察：

- baseline 为什么不等于 HL？
- heuristic policy 哪些规则是显式可审查的？
- feedback report 为下一轮代码更新留下了什么证据？
- robot soccer 的 blocked-lane probe 为什么比单场胜负更适合做回归测试？
- VizDoom replay 为什么把“何时拾取 medikit”变成可测试的代码阈值？
- traffic-grid 为什么把“最大队列优先”改写成“先保护下游容量”的可维护约束？
- Breakout replay 为什么需要预测反射后的截点，而不是追当前球坐标？
- Ant gait replay 为什么把连续控制问题拆成 cadence、stance duty 和 yaw feedback？

## 课后任务

1. 在 GridWorld 中增加一个新陷阱。
2. 先写一个失败测试。
3. 修改 `heuristic_policy`。
4. 生成 feedback report。
5. 写 5 行复盘：新规则解决了什么，是否可能破坏旧行为。

配套实验：[Lab 1：跑通 Heuristic Learning 闭环](/zh-cn/slides/lab-1/)。
