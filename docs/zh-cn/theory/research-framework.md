---
title: 研究框架
description: Heuristic Learning 的问题定义、证据边界和可检验研究问题
---

# 研究框架

HL 还不是已经定型的教科书理论。学习这部分时，重点不是背诵几个结论，而是学会把一个直觉判断改写成可检查的问题：它支持什么、证据在哪里、可能怎样被反驳、下一步应该跑什么实验。

本页把研究部分收束成三件事：

1. 判断一个问题是否适合用 HL 讨论。
2. 选择合适的评估维度。
3. 把案例写成可检验研究问题，而不是写成口号。

## 最小问题定义

一个任务进入 HL 讨论前，至少要满足四个条件：

| 条件 | 解释 | 可读例子 |
| --- | --- | --- |
| 策略能落到软件结构 | 决策逻辑能写进代码、配置、阈值、检测器或测试 | GridWorld `policies.py` |
| 反馈能被记录 | 失败不是口头描述，而是能保存为 trace、log、replay、测试或评审记录 | `experiments/*/latest.json` |
| 更新对象可审查 | 修改对象能被读者或 reviewer 看懂 | VizDoom `pickup_health` 阈值 |
| 回归能验证 | 新规则必须证明没有破坏旧场景 | `npm run examples:test` |

如果只有人工经验，没有反馈报告和回归测试，它只是一个 heuristic system。只有当失败、修改和验证都能留下证据时，它才接近 Heuristic Learning。

## 研究对象

HL 不问“规则是否一定比神经网络强”。更合适的问题是：

- 失败如何被压缩成可测试场景？
- 哪些经验值得写成显式规则、阈值、检测器或回放？
- 编码智能体能否降低维护这些规则的成本？
- 新规则如何避免破坏旧经验？
- 轻量 replay 与真实环境复现之间差多少？

这些问题都要求证据路径，而不是只要求最终分数。

## 评估维度

阅读案例或设计实验时，优先用五个维度检查：

| 维度 | 要回答的问题 | 示例证据 |
| --- | --- | --- |
| 任务结果 | 更新后行为是否改善？ | `goal`、`stable_flow`、`valued_pickup` |
| 失败隔离 | 是否找到了稳定失败场景？ | `blocked_shot`、`spillback` |
| 更新成本 | 需要改多少规则、测试或控制参数？ | policy diff、实验记录 |
| 回归风险 | 新规则会不会忘掉旧经验？ | `tests/test_*.py`、固定 replay |
| 来源边界 | 当前证据能支持多强的结论？ | 来源登记、case card、引用说明 |

分数可以作为度量之一，但不能是唯一度量。HL 更关心系统如何把失败经验沉淀为可维护结构。

## 可检验研究问题

下面的问题来自当前示例和案例。它们不是定论；学习时要把它们当成可以继续验证或反驳的问题。

| 研究问题 | 当前证据 | 下一步检验 |
| --- | --- | --- |
| 学习对象是否可以是软件结构？ | Breakout、VizDoom、Ant 的轻量 replay 展示了阈值、轨迹预测和控制参数更新 | 在真实 Atari、VizDoom 或 MuJoCo 环境中复测 |
| 反馈报告能否帮助下一轮智能体维护代码？ | 六个 `experiments/*/latest.json` 都记录 baseline、heuristic 和 candidate update | 比较结构化 report、普通日志和纯 prompt 记忆的差异 |
| 失败类型是否比平均分更适合学习？ | `local_greedy_trap`、`blocked_shot`、`spillback` 等 probe 能解释具体错误 | 检查 probe 是否能跨随机种子或扩展场景稳定复现 |
| HL 与 RL/DL 如何分工？ | 当前材料显示 HL 更适合固化已知失败、测试和工程记忆 | 接入高保真环境，比较参数学习与软件结构更新的边界 |
| 来源状态如何约束结论强度？ | 来源登记区分公开 artifact、轻量 replay、X 线索和脱敏应用问题 | 对 X 来源做一手复核，未复核前不写成实验结论 |
| 事实约束审计能否成为可维护反馈通道？ | 闭世界夹具能稳定阻断已知矛盾，并将目录未知主张升级给外部证据 | 在带来源的原子事实数据集上评估精度、召回、拒答率和答案效用 |

机器可读的研究问题矩阵保留在 [`/claims-registry.json`](/claims-registry.json)。它供脚本检查证据页、示例、验证命令和反驳说明；读者不需要先读 registry，先读本页和案例页即可。

```bash
npm run examples:breakout-replay
npm run examples:vizdoom-replay
npm run examples:ant-gait-replay
npm run examples:constraint-audit
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run examples:test
npm run source:registry:check
npm run course:structure:check
npm run claims:registry:check
npm run metrics:check
npm run verify
```

## 实验骨架

一个主线实验至少要保留同一个骨架：

```text
case signal -> minimal environment -> baseline failure -> heuristic patch
            -> feedback report -> regression test
```

对应到仓库：

| 层 | 文件 |
| --- | --- |
| 环境 | `examples/*/env.py` 或 replay env |
| 策略 | `examples/*/policies.py` |
| 运行入口 | `examples/*/run.py` |
| 反馈报告 | `examples/*/feedback_loop.py` 与 `experiments/*/latest.json` |
| 回归验证 | `tests/test_*.py` |
| 读者解释 | `docs/zh-cn/examples/` 与 `docs/zh-cn/cases/` |

统一验证命令是：

```bash
npm run verify
```

## 与 RL/DL 的边界

HL 不排斥 RL 或 DL。更合理的边界是：

- 当感知表征复杂、状态不可手写时，DL 适合做检测器或表征层。
- 当策略需要大量探索且奖励可以稳定采样时，RL 仍然适合做策略学习。
- 当失败模式能被回放、日志、测试和代码规则清楚表达时，HL 适合做快速固化与长期维护。

真实系统可以是混合结构：视觉模型负责感知，RL 负责部分连续控制，HL 负责规则、异常处理、测试、回放和工程记忆。

继续学习时，读 [实验协议](/zh-cn/appendix/benchmark-protocol) 看如何设计可验证实验，读 [评估指标矩阵](/zh-cn/appendix/evaluation-metrics) 看如何判断证据强度，读 [研究课题](/zh-cn/appendix/research-projects) 选择可继续推进的问题。
