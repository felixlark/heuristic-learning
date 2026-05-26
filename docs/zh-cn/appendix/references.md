---
title: 来源与背景阅读
description: Heuristic Learning 课程使用的一手来源和背景材料
---

# 来源与背景阅读

本页记录课程当前使用的公开来源和背景材料。它不是完整文献综述；每条来源能支持的结论强度，以 [来源登记](/zh-cn/appendix/source-registry) 为准。
引用本课程仓库、原始来源和轻量 replay 时，请先阅读 [引用与署名](/zh-cn/appendix/citation)。
如果你要按研究路径系统阅读这些材料，先走 [文献阅读指南](/zh-cn/appendix/reading-guide)，再把阅读产物落到来源登记、研究问题矩阵或 runnable example。

## 一手来源

| 来源 | 用途 | 状态 |
| --- | --- | --- |
| [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) | HL 概念和案例主源 | 已定位 |
| [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) | Atari、MuJoCo、VizDoom artifact | 部分已复现为轻量 replay |
| [Jiayi Weng X 原帖](https://x.com/Trinkle23897/status/2052596837547495549) | X 来源和社区传播入口 | 已结构化 |

## 背景概念

| 主题 | 本课程中的使用方式 |
| --- | --- |
| Reinforcement Learning | 作为 state/action/reward/policy/probe 的对照语言 |
| Deep Learning | 作为权重更新、表征学习和感知模块的对照 |
| Software Testing | 作为 HL 反遗忘和回归验证的基础机制 |
| Program Synthesis / Coding Agents | 作为“更新者”的工程前提，而不是单独的理论结论 |

## 引用规则

- 公开来源用于定义概念和案例时，必须进入 [来源登记](/zh-cn/appendix/source-registry)。
- 背景概念只用于界定问题边界，不作为 HL 结论证据。
- X 和私有来源必须标注来源层级，不能把二手转述写成已验证事实。
- 已复现的主张必须指向 runnable example、feedback report 和测试路径。

新增参考时，同时检查：

```bash
npm run source:registry:check
npm run course:structure:check
```
