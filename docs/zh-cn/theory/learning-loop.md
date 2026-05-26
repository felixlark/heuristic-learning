---
title: 学习闭环
description: Heuristic Learning 如何从一次失败变成可维护的软件更新
---

# 学习闭环

Heuristic Learning 关心的不是“写一条规则让当前样例过关”，而是一个系统怎样从失败中留下可复用经验。一次合格的 HL 更新，至少要说明五件事：

1. 哪里失败了。
2. 为什么原来的策略会失败。
3. 修改了哪个可维护的软件结构。
4. 修改后如何验证有效。
5. 如何防止以后忘掉这次经验。

本页用 GridWorld 作为最小例子说明这条闭环。先运行：

```bash
npm run examples:gridworld
npm run examples:gridworld:feedback
```

运行后打开 `experiments/gridworld/latest.json`。读这份报告时，不要只看成功率；重点看它如何记录失败场景、策略差异和下一轮修改建议。

## 一个最小例子

GridWorld 里有起点、终点和陷阱。一个朴素策略会贪心地靠近终点：如果向右离终点更近，它就向右走。这个策略看起来合理，但在 `local_greedy_trap` 场景里会直接走进已知陷阱。

HL 的学习对象不是神经网络权重，而是这类可检查的软件结构：

| 对象 | 在 GridWorld 里的含义 |
| --- | --- |
| 失败场景 | `local_greedy_trap`：最短路会踩进陷阱 |
| 原始策略 | 贪心靠近终点 |
| 更新对象 | `examples/heuristic-gridworld/policies.py` 中的策略规则 |
| 验证方式 | feedback report 与 `tests/test_gridworld.py` |
| 复盘材料 | `experiments/gridworld/latest.json` |

这就是 HL 和普通“调参数”的差异：读者能看到系统学到了哪条经验，也能检查这条经验是否被测试和报告保留下来。

## 闭环的五步

| 步骤 | 要做什么 | GridWorld 例子 |
| --- | --- | --- |
| 1. 观察失败 | 找到一个具体、可重复的问题 | 贪心策略进入陷阱 |
| 2. 固定场景 | 把问题压缩成最小测试或 replay | `local_greedy_trap` |
| 3. 修改结构 | 只改一个清楚的软件对象 | 遇到已知陷阱时选择绕开 |
| 4. 生成报告 | 记录 baseline、heuristic 和候选更新 | `experiments/gridworld/latest.json` |
| 5. 回归验证 | 确认新规则没有破坏旧行为 | `npm run examples:test` |

读者可以把这五步套到其他示例上：Robot Soccer 是“射门前检查通道”，VizDoom 是“血量高时不要过早拾取 medikit”，Traffic Grid 是“先保护下游容量”。例子不同，但闭环相同。

## 怎么读反馈报告

`experiments/gridworld/latest.json` 至少要读三个部分：

| 字段 | 读者要看什么 |
| --- | --- |
| `policies` | baseline 和 heuristic 在同一环境里的行为差异 |
| `probes` | 哪个最小场景暴露了失败 |
| `candidate_update` | 下一轮应该改哪个文件、跑哪条验证命令 |

如果一份报告只告诉你“分数变高了”，它还不够。HL 需要的是能指导下一轮维护的证据：失败在哪里，经验被写进哪里，怎么证明没有退化。

## 什么样的更新才算 HL

下面两种更新很容易混淆：

| 做法 | 是否合格 | 原因 |
| --- | --- | --- |
| 只在当前输入上加一个特判 | 不够 | 不能说明会不会破坏其他场景 |
| 把失败场景写成 probe，再修改策略并保留测试 | 合格 | 经验被压缩成可复查的软件结构 |
| 只展示一次成功截图 | 不够 | 没有 baseline、报告和回归路径 |
| 生成 report，并让 report 指向下一轮 update target | 合格 | 智能体和读者都能继续维护 |

因此，HL 的关键不是“规则越多越好”，而是每条规则都能回答：它来自哪个失败？修改了哪个对象？用什么测试保护它？

## 练习

完成下面三个小任务：

1. 在 `experiments/gridworld/latest.json` 里找到 `local_greedy_trap`，用一句话解释 baseline 为什么失败。
2. 打开 `examples/heuristic-gridworld/policies.py`，指出 heuristic policy 比 baseline 多维护了什么判断。
3. 运行 `npm run examples:test`，确认这个判断已经被测试保护。

如果想继续练习，把同样的问题套到 [Robot Soccer 示例](/zh-cn/cases/robot-soccer/)：

- 失败场景是什么？
- baseline 为什么会射门失败？
- heuristic patch 修改了哪个动作前提？
- 哪个测试证明旧经验没有退化？

## 进入下一步

读完本页后，继续看：

- [可运行示例](/zh-cn/examples/)：用六个最小环境观察不同类型的失败。
- [从 RL/DL 到 HL](/zh-cn/stage-3/)：理解 HL 的更新对象为什么不是权重。
- [实验协议](/zh-cn/appendix/benchmark-protocol)：学习如何判断一个案例是否有足够证据进入主线实验。

最终验收仍然是：

```bash
npm run verify
```

这条命令会重新跑测试、生成反馈报告、检查课程结构并构建文档站。对 HL 来说，能被重复验证的经验才是学习结果。
