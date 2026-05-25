---
title: 第 3 讲：失败类型与反遗忘
description: 直觉学习课程第 3 讲讲义
---

# 第 3 讲：失败类型与反遗忘

## Slide 1：问题

一个 heuristic patch 通过了当前 probe，为什么仍然可能不是一次好的 HL 更新？

因为 HL 的学习对象是可维护软件结构。一次更新不仅要修复眼前失败，还要降低未来维护成本，并且不能让旧经验被新规则覆盖。

## Slide 2：把失败先分类

先分类再修复，可以避免把所有问题都写成更长的条件分支。

| 失败类型 | 本仓库 probe | 常见错误更新 |
| --- | --- | --- |
| 局部贪心 | `local_greedy_trap` | 只加一个格子的黑名单 |
| 动作前提缺失 | `blocked_shot` | 继续强化射门偏好 |
| 资源时机错误 | `wasted_pickup` | 永远推迟拾取资源 |
| 物理预测不足 | `missed_after_wall_reflection` | 追当前坐标而非预测落点 |
| 控制稳定性退化 | `yaw_drift` | 增大前进力但放大偏航 |
| 系统容量约束缺失 | `spillback` | 只优化局部吞吐 |

分类的作用是让下一次智能体更新知道：应该改检测器、动作选择、预测模型、控制参数，还是安全约束。

## Slide 3：Patch 不等于学习

一次 patch 要进入课程主线，至少要留下三类证据：

| 证据 | 目的 | 本仓库位置 |
| --- | --- | --- |
| Failure probe | 证明旧策略稳定失败 | `tests/test_*.py` |
| Feedback report | 记录为什么失败、改了什么 | `experiments/*/latest.json` |
| Regression gate | 证明旧经验没有被破坏 | `npm run verify` |

没有 regression gate 的 patch 只是一次修补；有可重复失败、可审查报告和统一验证门槛，才接近 HL 意义上的学习。

## Slide 4：反遗忘是工程问题

DL 里的遗忘常表现为参数分布变化。HL 里的遗忘更像工程退化：

- 新规则抢占了旧规则的优先级。
- 新阈值只适合一个 replay。
- 新 detector 漏掉了边界条件。
- 新 report 没有更新，智能体下一轮读到过期记忆。
- 文档说已复现，但示例、测试或来源登记没有同步。

所以 HL 的反遗忘不只靠测试。它还需要来源登记、实验报告、课程结构检查和机器可读 manifest 共同约束。

## Slide 5：六个案例的反遗忘检查

课堂上逐个问同一个问题：新 heuristic 会不会破坏旧行为？

| 案例 | 回归问题 | 最小检查 |
| --- | --- | --- |
| GridWorld | 避开陷阱后是否还能到达目标？ | `npm run examples:gridworld` |
| Robot Soccer | 绕开封堵后是否仍会射门？ | `npm run examples:robot-soccer` |
| VizDoom | 等待 medikit 后是否会在低血量拾取？ | `npm run examples:vizdoom-replay` |
| Traffic Grid | 保护下游后是否仍保持吞吐？ | `npm run examples:traffic-grid` |
| Breakout | 反射预测后是否还能处理直线球？ | `npm run examples:breakout-replay` |
| Ant Gait | 偏航反馈后是否仍能向前推进？ | `npm run examples:ant-gait-replay` |

统一检查：

```bash
npm run examples:test
npm run examples:feedback
npm run verify
```

## Slide 6：维护成本度量

研究者可以用一个轻量表格记录每次更新的维护成本：

| 维度 | 观察问题 |
| --- | --- |
| 规则局部性 | 这次改动是否集中在一个策略函数或 detector？ |
| 可解释性 | 失败和修复能否被 3 句话说明？ |
| 报告一致性 | `candidate_update` 是否指向真实下一步？ |
| 旧行为覆盖 | 旧 probe 是否仍在测试里？ |
| 来源追踪 | 是否能从案例页回到原始 artifact 或线索？ |

这个表格不替代指标实验，但能把“启发式是否值得保留”从主观印象变成可审查记录。

## Slide 7：课堂练习

选择一个案例，模拟一次会导致遗忘的坏更新：

1. 描述坏更新会修复哪个 probe。
2. 写出它可能破坏的旧行为。
3. 指出应该新增哪个测试。
4. 更新对应 `experiments/*/latest.json` 中的下一轮建议。
5. 用 `npm run verify` 证明课程结构仍一致。

不要为了练习真的提交坏策略；目标是学会在 patch 之前预测退化路径。

## Slide 8：课后任务

给任意一个示例补一条“反遗忘检查”说明：

- 在案例页写清楚旧行为是什么。
- 在 test 文件中确认这个旧行为已经被覆盖。
- 在反馈报告中把下一轮更新写成可执行任务。
- 运行 `npm run examples:reports:check` 和 `npm run course:structure:check`。

配套阅读：[学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework) 与 [课程 Rubric](/zh-cn/appendix/rubric)。
