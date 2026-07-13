---
title: 真实环境 Benchmark
description: Heuristic Learning 的真实控制环境实验、评估纪律与证据边界
---

# 真实环境 Benchmark

最小示例用于理解机制，真实环境 benchmark 用于检验主张。Jiayi Weng 在 `learning-beyond-gradients/heuristic_learning` 中实现了五个 Gymnasium 控制任务，并公开实验账本、策略代码、汇总报告和失败记录。

## 实验怎样避免自我欺骗

| 规则 | 做法 | 原因 |
| --- | --- | --- |
| 固定数据划分 | 开发种子 `0..19`、保留种子 `1000..1049`、审计种子 `2000..2049` | 防止边看最终结果边调规则 |
| 追加式账本 | 每次运行都追加，不删除失败或部分结果 | 保留真实的试错成本 |
| 分开更新类型 | 结构修改、数值调参、教师蒸馏、RL 基线分别记录 | 避免把不同来源的提升混为一谈 |
| 记录成本 | 环境步数、耗时、版本、代码修改和迭代次数 | 比较结果时同时比较维护代价 |
| 冻结后审计 | 最终策略在未参与选择的种子上运行 | 检查开发阶段的结论能否迁移 |

## 上游结果怎么读

上游报告的核心结论是：五个环境中四个达到严格目标，五个都进入目标的 5% 范围，但不同任务的学习路径并不一致。

- CartPole 的初始规则已经很强，后续结构修改反而下降。这提醒我们“改了代码”不等于“学到了东西”。
- MountainCar 最终使用可读的有限时域动力学规划器，说明 heuristic 不必只是 `if/else`。
- Acrobot 的最佳透明策略来自 PPO 教师蒸馏，应单独标记为“教师辅助”，不能当作纯手写规则提升。
- LunarLander 的结构更新出现退化，较好的结果来自数值调参。
- BipedalWalker 在独立审计上进入严格目标的 5% 范围，但没有达到严格阈值，是应被保留的负面结果。

以上是对上游公开结果的整理，本仓库尚未在相同机器和依赖版本上完整复跑全部 728 条记录。原始证据见 [上游 benchmark](https://github.com/Trinkle23897/learning-beyond-gradients/tree/main/heuristic_learning) 和 [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/)。

## 本仓库的复现入口

基础课程继续使用六个纯 Python 小实验；研究进阶增加一个原创 CartPole 入口，用相同的评估原则演示真实环境实验：

```bash
python3 -m pip install 'gymnasium[classic-control]'
npm run examples:cartpole:dev
npm run examples:cartpole:audit
```

不要在看过 `holdout` 或 `audit` 结果后继续调策略。需要继续迭代时，建立新的未见种子范围并记录原因，而不是复用最终评估集。

当前透明策略已在开发种子 `0..19` 上完成本地验证，20 个 episode 的平均、最低和最高步数均为 500。结果保存在 `experiments/cartpole/dev-validation.json`。这只说明开发集表现，不能代替冻结后的保留集和审计集结论。

## 可以继续研究的问题

1. 结构修改与数值调参怎样公平比较成本？
2. 一条规则跨环境、跨随机种子时会遗忘哪些旧能力？
3. 教师蒸馏得到的透明策略，解释性和可靠性如何验证？
4. 当规则系统变大时，测试覆盖能否跟上更新速度？
5. 哪些任务应使用 HL，哪些任务应交给 RL/DL，哪些适合组合？
