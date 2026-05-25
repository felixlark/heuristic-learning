---
title: 从 RL/DL 到 HL
description: 强化学习、深度学习与直觉学习的对照
---

# 从 RL/DL 到 HL

HL 不是 Deep Learning 或 Reinforcement Learning 的替代品。它更像是在“可被代码表达、可被测试反馈驱动”的问题上，提供另一种学习对象。

| 维度 | Deep Learning | Deep RL | Heuristic Learning |
| --- | --- | --- | --- |
| 更新对象 | 神经网络参数 | 策略/价值网络参数 | 软件结构、规则、测试、记忆 |
| 更新机制 | 反向传播 | 奖励驱动的梯度/采样更新 | 编码智能体直接修改代码 |
| 反馈来源 | 数据集损失 | 环境奖励、轨迹 | 测试、日志、回放、奖励、人类反馈 |
| 优势 | 表征能力强 | 可处理复杂决策 | 可解释、可审查、可快速固化 |
| 风险 | 数据/算力成本 | 样本效率低、难调 | 规则冲突、工程型遗忘 |

## 对 AI 研究者：研究对象从权重转向软件结构

HL 的研究问题不是“能否用规则替代模型”，而是：当更新者是编码智能体时，哪些可审查的软件结构可以承载经验？一个可研究的 HL 案例至少要说明 failure mode、可观测反馈、更新对象、回归风险和可反驳路径。

研究者可以从 [研究框架](/zh-cn/theory/research-framework) 和 [研究命题](/zh-cn/theory/research-propositions) 进入，把每个案例写成“主张 -> 证据 -> 反例 -> 下一步实验”的形式。当前仓库中的轻量 replay 只能支持教学型假设，不能直接写成高保真复现实验结论。

## 对工程师：先判断该学习什么

工程实践里，HL 适合那些反馈清晰、失效可复现、更新对象可以被测试保护的问题。例如策略阈值、动作前提、状态检测器、回放 probe、配置和回归测试，都比“重新训练一个模型”更容易审查和维护。

不适合 HL 的问题也要明确：感知能力不足、状态不可观测、奖励定义不稳定、或需要大规模泛化时，仍然应优先考虑模型训练、数据改进或环境设计。工程师可以从 [可运行示例](/zh-cn/examples/) 开始，只改一个策略点，再用 `npm run examples:test` 和对应 feedback 命令确认旧行为没有退化。

## 对学生：用最小闭环理解差异

学生不需要先掌握完整 RL 或深度学习体系。更直接的路径是先跑一个最小环境，观察 baseline 为什么失败，再看 heuristic patch 如何把失败经验固化成可读代码。

推荐顺序是：[学习路线](/zh-cn/stage-1/) -> [HL 基础概念](/zh-cn/stage-2/) -> [GridWorld 示例](/zh-cn/examples/) -> [Lab 1](/zh-cn/slides/lab-1/)。完成一次实验记录后，再回到本页对照 RL/DL/HL 的更新对象差异。

## 继续形成研究问题

更具体的问题定义、度量维度和实验范式见 [学习闭环](/zh-cn/theory/learning-loop) 与 [研究框架](/zh-cn/theory/research-framework)。后续新增案例时，应优先补齐 baseline failure、heuristic patch、feedback report 和 regression test，而不是只补叙述。
