---
title: 研究命题
description: Heuristic Learning 当前可讨论、可反驳、可实验化的核心命题
---

# 研究命题

Jiayi Weng 的 HL 思路还没有形成正式论文体系。本页把仓库当前采用的研究主张拆成命题、证据状态和可运行检验，避免把直觉性判断写成已定论。

机器可读命题矩阵见 [`/claims-registry.json`](/claims-registry.json)，字段约束见 [`/claims-registry.schema.json`](/claims-registry.schema.json)。`npm run claims:registry:check` 会检查每条命题是否绑定证据页、示例、验证命令和可反驳说明。

## 命题 1：学习对象可以是软件结构

传统 RL/DL 常把学习压缩进参数。HL 的第一条命题是：在很多工程任务里，真正值得学习的对象可以是检测器、阈值、控制律、测试、回放和评审规则。

| 证据状态 | 当前材料 |
| --- | --- |
| 公开 artifact | `learning-beyond-gradients` 中的 Breakout、VizDoom、Ant 启发式代码 |
| 轻量复现 | `examples/breakout-replay/`、`examples/vizdoom-replay/`、`examples/ant-gait-replay/` |
| 待验证边界 | 这些规则跨关卡、跨随机种子、跨真实仿真器是否稳定 |

可运行检验：

```bash
npm run examples:breakout-replay
npm run examples:vizdoom-replay
npm run examples:ant-gait-replay
npm run examples:test
```

## 命题 2：反馈报告是下一轮智能体的训练样本

HL 不是一次性写规则。它要求失败被压缩成结构化记录，让下一轮编码智能体知道应该改哪里、保留什么约束、跑什么测试。

| 字段 | 作用 |
| --- | --- |
| `policies` | 固定 baseline 与 heuristic 的行为差异 |
| `feedback` | 把观察转成维护约束 |
| `candidate_update.target` | 指向下一轮可修改文件 |
| `candidate_update.verification` | 锁定回归验证命令 |

可运行检验：

```bash
npm run examples:feedback
npm run examples:reports:check
```

## 命题 3：失败类型比平均分更适合课程化

课程读者需要看到系统为什么失败，而不只是看最终 reward。HL 仓库因此优先组织 failure mode：`local_greedy_trap`、`blocked_shot`、`wasted_pickup`、`spillback`、`missed_after_wall_reflection`、`yaw_drift`。

| Failure mode | 学习重点 | 示例 |
| --- | --- | --- |
| `local_greedy_trap` | 局部最短路不是全局安全策略 | GridWorld |
| `blocked_shot` | 动作前检查比距离启发更关键 | Robot Soccer |
| `wasted_pickup` | 价值需要时机判断 | VizDoom |
| `spillback` | 局部吞吐会破坏下游约束 | Traffic Grid |
| `missed_after_wall_reflection` | 当前观测需要物理外推 | Breakout |
| `yaw_drift` | 控制律需要稳定性反馈 | Ant Gait |

可反驳点：如果一个 failure mode 无法稳定复现、无法写成测试，或者 heuristic patch 只在单个手写状态上有效，它就不能作为主线命题证据。

可运行检验：

```bash
npm run examples:registry:check
npm run examples:test
```

## 命题 4：HL 和 RL/DL 是分工关系

HL 不主张替代 RL/DL。更可操作的命题是：

| 层 | 更适合的方法 | 原因 |
| --- | --- | --- |
| 感知表征 | DL | 图像、语音、复杂状态不适合全手写 |
| 大规模探索 | RL | 奖励可采样且交互成本可控时，参数学习更自然 |
| 已知失败固化 | HL | 日志、回放、测试和规则能把经验沉淀为可维护结构 |
| 工程反遗忘 | HL | 显式回归测试和来源登记能约束后续智能体更新 |

本仓库的轻量示例只验证第三、第四层。第一、第二层需要后续接入真实环境或模型实验。

可运行检验：

```bash
npm run examples:feedback
npm run verify
```

## 命题 5：来源状态必须进入课程结构

没有论文时，来源治理本身就是研究质量的一部分。HL 课程应区分公开来源、内部线索、轻量复现、完整复现和研究假设。

对应文件：

| 文件 | 作用 |
| --- | --- |
| [来源登记](/zh-cn/appendix/source-registry) | 标注每个信号的来源状态 |
| [引用与署名](/zh-cn/appendix/citation) | 区分原始作者、课程整理和轻量 replay |
| [实验协议](/zh-cn/appendix/benchmark-protocol) | 规定 baseline、patch、report 与测试 |
| [评估指标矩阵](/zh-cn/appendix/evaluation-metrics) | 规定任务结果、失败隔离、更新成本、回归风险和来源边界 |
| `SECURITY.md` | 防止把私有素材误发布为公共证据 |

可运行检验：

```bash
npm run source:registry:check
npm run course:structure:check
```

## 下一步研究任务

这些命题下一步要转成更严格的实验：

1. 在真实 VizDoom、Atari 或 MuJoCo 环境里复测轻量 replay 的边界。
2. 让编码智能体根据 `experiments/*/latest.json` 自动提出 patch，再由测试决定是否接受。
3. 比较纯 prompt 经验、结构化 feedback report 和传统单元测试在反遗忘上的差异。
4. 把 X/FieldTheory 信号转成脱敏 case card，并要求每个 case card 至少落到一个 probe 或研究待办。

这些任务对应 [研究路线图](/zh-cn/appendix/research-roadmap) 和 [研究课题](/zh-cn/appendix/research-projects)。当前页面只是命题地图，不替代实证结论。

如果要把这些命题整理成论文或技术报告，先使用 [论文蓝图](/zh-cn/appendix/paper-blueprint) 和 `/paper-blueprint.json`。`npm run paper:blueprint:check` 会检查命题、指标、示例、证据路径和边界是否仍然一致。
