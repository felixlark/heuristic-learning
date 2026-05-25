---
title: 研究框架
description: Heuristic Learning 的问题定义、度量与实验范式
---

# 研究框架

HL 现在更像一个正在形成的研究方向，而不是已有稳定教科书的领域。本页把当前仓库采用的研究框架写清楚：哪些问题可以被称为 HL，如何设计实验，如何判断系统真的学到了东西。

## 最小问题定义

一个任务可以进入 HL 研究范围，至少需要满足四个条件：

| 条件 | 解释 | 课程示例 |
| --- | --- | --- |
| 策略可被软件结构表达 | 决策逻辑能落到代码、配置、规则、检测器或测试里 | GridWorld `policies.py` |
| 反馈可被记录 | 失败不是一句口头描述，而是能保存为 reward、trace、log、replay 或评审记录 | `experiments/*/latest.json` |
| 更新对象可被审查 | 智能体修改的不是黑盒权重，而是人能 review 的 artifact | `vizdoom_policies.py` 阈值 |
| 回归可以验证 | 新规则必须证明没有破坏旧 probe | `python3 -m unittest discover -s tests` |

如果一个系统只有人工写规则，但没有反馈记录和回归验证，它只是 heuristic system，不是完整的 Heuristic Learning 过程。如果一个系统只有编码智能体随手改代码，但没有可复现实验，它也不能算研究意义上的 HL。

## 研究对象

HL 的研究对象不是“规则是否比神经网络强”，而是下面这些更具体的问题：

- 反馈如何变成代码修改任务？
- 哪些状态检测器值得被显式维护？
- 新规则如何和旧规则组合，避免工程型遗忘？
- 回放、日志和测试分别适合捕捉哪类失败？
- 编码智能体是否降低了 heuristic system 的长期维护成本？

这些问题都要求实验 artifact，而不是只要求最终分数。

## 度量维度

课程暂时采用四类度量：

| 度量 | 关注点 | 例子 |
| --- | --- | --- |
| 任务结果 | 策略是否解决当前场景 | `goal`、`stable_flow`、`valued_pickup` |
| 失败隔离 | probe 是否能稳定复现失败 | `blocked_shot`、`spillback` |
| 更新成本 | 修复需要改多少结构 | policy 阈值、检测器、测试、记忆 |
| 回归风险 | 新规则是否破坏旧场景 | 单元测试、固定 replay、实验 JSON |

分数可以是度量之一，但不能是唯一度量。HL 关心的是系统如何把失败经验沉淀为可维护结构。

## 实验范式

每个主线实验都应该保留同一个骨架：

```text
case signal -> minimal environment -> baseline failure -> heuristic patch
            -> feedback report -> regression test -> course note
```

对应到仓库：

| 层 | 文件 |
| --- | --- |
| 环境 | `examples/*/env.py` 或 replay env |
| 策略 | `examples/*/policies.py` |
| 运行入口 | `examples/*/run.py` |
| 反馈报告 | `examples/*/feedback_loop.py` 与 `experiments/*/latest.json` |
| 回归验证 | `tests/test_*.py` |
| 教学解释 | `docs/zh-cn/examples/` 与 `docs/zh-cn/cases/` |

因此，章节、案例、实验和附录必须互相指向，而不是各写各的。

统一验证命令是：

```bash
npm run verify
```

它会重新生成实验报告并运行 `scripts/check-experiment-reports.py`，所以“反馈可记录”和“回归可验证”不是文档承诺，而是仓库检查的一部分。

## 与 RL/DL 的边界

HL 不排斥 RL 或 DL。更合理的边界是：

- 当感知表征复杂、状态不可手写时，DL 适合做检测器或表征层。
- 当策略需要大量探索并且奖励可以稳定采样时，RL 仍然适合做策略学习。
- 当失败模式能被回放、日志、测试和代码规则清楚表达时，HL 适合做快速固化与长期维护。

因此一个真实系统可以是混合结构：视觉模型负责感知，RL 负责部分连续控制，HL 负责规则、异常处理、测试、回放和工程记忆。

## 当前研究假设

课程先采用三个工作假设，后续通过案例迭代修正：

1. 编码智能体会降低 heuristic system 的维护成本，使显式规则重新变成有研究价值的学习对象。
2. HL 的核心产物不是单条规则，而是可审查、可测试、可复盘的软件结构。
3. 好的 HL 实验应该让读者能看到失败、改动、验证和记录，而不只是看到最终成功。

这些假设目前还不是论文结论。课程的任务是把它们转成可运行实验与可讨论的课程材料。

可执行项目见 [研究课题](/zh-cn/appendix/research-projects)，实验设计和报告约束见 [实验协议](/zh-cn/appendix/benchmark-protocol)。研究评估维度见 [评估指标矩阵](/zh-cn/appendix/evaluation-metrics) 和 `/evaluation-metrics.json`，更新后运行 `npm run metrics:check`。术语边界见 [术语表](/zh-cn/appendix/glossary)，公开来源和背景阅读见 [来源与背景阅读](/zh-cn/appendix/references)。
