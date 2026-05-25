---
title: 文献阅读指南
description: Heuristic Learning 课程的一手来源和背景概念阅读顺序
---

# 文献阅读指南

本页给研究者和学生一条可执行的阅读路径：先读一手来源，再看公开 artifact，最后把背景概念落到课程的命题、示例和验证命令。它不是完整文献综述；所有来源状态仍以 [来源登记](/zh-cn/appendix/source-registry) 为准。

## 阅读原则

| 原则 | 说明 |
| --- | --- |
| 先一手来源 | 优先读 Jiayi Weng 的文章、公开代码 artifact 和 X 原帖 |
| 再背景对照 | RL、DL、软件测试和编码智能体只用于界定问题边界 |
| 不把线索写成结论 | X/脱敏应用问题进入主线前必须有 case card、来源状态和可验证落点 |
| 每个主张都要落地 | 读完一条主张后，必须能指到命题、示例、报告或路线图任务 |

## 第一轮：建立 HL 语境

| 材料 | 读法 | 学习落点 |
| --- | --- | --- |
| `Learning Beyond Gradients` | 先抓住“更新对象不是权重，而是可维护系统结构”的主张 | [HL 基础概念](/zh-cn/stage-2/)、[研究命题](/zh-cn/theory/research-propositions) |
| `Trinkle23897/learning-beyond-gradients` | 不急着复现全部环境，先定位哪些 artifact 能被压缩成 replay/probe | [来源登记](/zh-cn/appendix/source-registry)、[案例库](/zh-cn/cases/) |
| Jiayi Weng X 原帖 | 只当作一手信号，不直接当作已复现实验 | [X 来源案例](/zh-cn/cases/x-signal/) |

读完后运行：

```bash
npm run claims:registry:check
npm run source:registry:check
```

## 第二轮：对照 RL/DL

| 背景 | 读法 | 课程问题 |
| --- | --- | --- |
| Deep Learning | 把它当作“参数更新”和“表征学习”的对照，而不是 HL 的反面 | 哪些任务仍应由模型做感知？ |
| Reinforcement Learning | 把 state/action/reward/policy 作为共享语言 | 哪些 failure mode 适合 replay 和测试，而不是继续采样？ |
| Software Testing | 把回归测试视为 HL 的反遗忘机制 | 新 heuristic 是否破坏旧经验？ |
| Coding Agents | 把编码智能体视为更新者 | feedback report 是否足够指导下一轮修改？ |

对应阅读：

- [从 RL/DL 到 HL](/zh-cn/stage-3/)
- [学习闭环](/zh-cn/theory/learning-loop)
- [研究框架](/zh-cn/theory/research-framework)
- [实验协议](/zh-cn/appendix/benchmark-protocol)
- [论文蓝图](/zh-cn/appendix/paper-blueprint)

## 第三轮：读代码而不是只读观点

| 代码入口 | 对应问题 | 验证命令 |
| --- | --- | --- |
| `examples/breakout-replay/` | 当前观测和物理预测的差异 | `npm run examples:breakout-replay` |
| `examples/vizdoom-replay/` | 资源拾取时机如何变成阈值规则 | `npm run examples:vizdoom-replay` |
| `examples/ant-gait-replay/` | 连续控制参数如何变成可审查更新对象 | `npm run examples:ant-gait-replay` |
| `examples/robot-soccer/` | 动作前提检查如何避免 blocked shot | `npm run examples:robot-soccer` |
| `examples/traffic-grid/` | 系统容量约束如何防止 spillback | `npm run examples:traffic-grid` |
| `examples/heuristic-gridworld/` | 最小 HL 闭环如何工作 | `npm run examples:gridworld` |

统一检查：

```bash
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
```

## 第四轮：从案例到研究问题

| 研究动作 | 目标 | 不应误用 |
| --- | --- | --- |
| 抽取 failure mode | 把案例压缩成可观察失败 | 不把平均分提升当成唯一证据 |
| 设计 probe | 让失败可回放、可测试 | 不把不可复现线索写成结论 |
| 写 feedback report | 指导下一轮策略或测试修改 | 不只写运行日志 |
| 定义反驳路径 | 说明什么结果会推翻当前命题 | 不把研究假设写成事实 |

对应仓库结构：

- [课程大纲](/zh-cn/syllabus/)
- [课程进度表](/zh-cn/appendix/course-schedule)
- [Slides 目录](/zh-cn/slides/)
- [练习集](/zh-cn/appendix/exercises)
- [课程 Rubric](/zh-cn/appendix/rubric)

## 阅读产物模板

每读完一条外部材料，至少形成下面其中一种产物：

| 产物 | 使用场景 | 模板或落点 |
| --- | --- | --- |
| Source row | 只是发现来源，还没有验证 | [来源登记](/zh-cn/appendix/source-registry) |
| Case card | 能描述环境、policy surface 和 feedback | `templates/case-card.md` |
| Experiment record | 已能运行示例或 replay | `templates/experiment-record.md` |
| Claim update | 材料支持或反驳一个命题 | `/claims-registry.json` |
| Roadmap task | 还需要真实环境或更多证据 | [研究路线图](/zh-cn/appendix/research-roadmap) |

## 不足与下一步

当前仓库的文献层仍有边界：

- 还没有完整论文综述，因为 HL 本身还处于思想形成期。
- 如果需要写论文或技术报告，使用 `/paper-blueprint.json` 和 `npm run paper:blueprint:check` 约束章节、证据和边界。
- 轻量 replay 不能替代真实 MuJoCo、Atari、VizDoom 环境复现。
- X 来源需要继续采集和脱敏结构化。
- RL/DL 背景仍以课程对照为主，后续可以补更严格的对照实验。

新增参考或阅读产物后，至少运行：

```bash
npm run source:registry:check
npm run claims:registry:check
npm run course:structure:check
npm run verify
```
