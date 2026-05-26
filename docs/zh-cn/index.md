---
title: 直觉学习课程首页
description: Heuristic Learning 中文研究与动手课程首页
---

# 直觉学习：从代码规则到可维护的学习系统

直觉学习（Heuristic Learning, HL）关注一个正在变得重要的现象：当编码智能体能够持续读日志、看回放、改代码、补测试时，一个系统可以在不更新神经网络权重的情况下变强。

这门课不把 HL 讲成已经成熟的理论，而是把它整理成一个可学习、可复现、可讨论的研究主题：

- **理论积累**：从 Jiayi Weng 的公开文章出发，提炼 HL、Heuristic System、反馈闭环、遗忘与维护成本等核心概念。
- **案例学习**：把 Atari、MuJoCo、VizDoom、机器人足球等案例变成学习卡片。
- **动手实践**：提供最小可运行环境，让读者看到“规则如何根据反馈被维护”。
- **可验证练习**：每个关键概念都要能落到命令、反馈报告、测试或复盘记录。

## 学习顺序

| 顺序 | 学什么 | 做什么 | 产出 |
| --- | --- | --- | --- |
| 1. 建立概念 | [学习路线](/zh-cn/stage-1/) 与 [HL 基础概念](/zh-cn/stage-2/) | 写出 feedback、update target、verification 的含义 | 一页术语笔记 |
| 2. 理解闭环 | [学习闭环](/zh-cn/theory/learning-loop) 与 [从 RL/DL 到 HL](/zh-cn/stage-3/) | 对照 RL/DL/HL 的更新对象 | 一张闭环图 |
| 3. 跑通示例 | [可运行示例](/zh-cn/examples/) 与 [Lab 1](/zh-cn/slides/lab-1/) | 运行 GridWorld 和 feedback report | 一份实验记录 |
| 4. 阅读案例 | [案例库](/zh-cn/cases/) 与 [来源登记](/zh-cn/appendix/source-registry) | 区分已复现、轻量 replay 和待验证线索 | 一张 case card |
| 5. 修改验证 | [代码导览](/zh-cn/appendix/code-tour) 与 [Lab 2](/zh-cn/slides/lab-2/) | 只改一个策略点，再跑测试和报告 | anti-forgetting checklist |
| 6. 复盘扩展 | [研究框架](/zh-cn/theory/research-framework) 与 [研究问题](/zh-cn/theory/research-framework) | 写出证据、反例和下一步实验 | 一个可反驳研究问题 |

## 推荐路线

1. 先看 [课程地图](/zh-cn/course-map/)：理解这份材料如何从概念走到练习。
2. 再看 [课程大纲](/zh-cn/syllabus/)：确认每个单元的阅读、命令和交付物。
3. 继续读 [学习路线](/zh-cn/stage-1/) 与 [HL 基础概念](/zh-cn/stage-2/)。
4. 对照 [RL/DL/HL](/zh-cn/stage-3/)：明确 HL 不是反向传播替代品，而是另一类更新对象。
5. 跑 [可运行示例](/zh-cn/examples/)：用最小环境看见状态、动作、反馈和规则更新。
6. 查 [案例库](/zh-cn/cases/)：用公开来源和脱敏应用案例练习 evidence-aware 的案例阅读。
7. 完成 [Lab 1](/zh-cn/slides/lab-1/) 和 [Lab 2](/zh-cn/slides/lab-2/)：把一次 heuristic update 写成可验证记录。

## 一句话定义

> HL 是一种由编码智能体维护软件结构的学习过程：反馈来自环境、测试、日志、回放或人类评价；更新对象是策略代码、状态检测器、配置、测试、记忆和实验记录，而不是神经网络权重。

## 当前最小闭环

1. 环境、测试、日志或回放暴露失败。
2. 编码智能体读取上下文，定位可修改的软件结构。
3. 只修改一个策略、规则、测试或记忆点。
4. 重新运行实验，生成反馈报告。
5. 记录结果，把新证据带回下一轮判断。

这个闭环是课程的组织核心：每章都要回答“反馈是什么、更新什么、如何验证没有退化”。
