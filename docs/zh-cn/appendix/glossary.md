---
title: 术语表
description: Heuristic Learning 课程术语、边界和学习落点
---

# 术语表

本页用于统一课程、案例和实验中的术语。HL 还不是稳定学科名词体系，所以这里的定义采用“课程工作定义”：每个术语都要能落到课程的示例、报告或验证命令。

| 术语 | 工作定义 | 学习落点 |
| --- | --- | --- |
| Heuristic Learning | 由编码智能体消费反馈并维护软件结构的学习过程 | [学习闭环](/zh-cn/theory/learning-loop) |
| Heuristic System | 由策略代码、状态表示、反馈通道、测试、实验记录和维护记忆组成的系统 | [研究框架](/zh-cn/theory/research-framework) |
| Signal | 值得学习的来源信号，可以来自 X、公开 artifact、私有来源、日志或回放 | [来源登记](/zh-cn/appendix/source-registry) |
| Probe | 能稳定暴露失败的最小场景 | `tests/test_*.py` |
| Baseline | 自然但不充分的简单策略，用来固定“系统学会了什么” | `experiments/*/latest.json` |
| Heuristic patch | 对策略、检测器、阈值、控制参数或安全约束的可审查更新 | `examples/*/policies.py` |
| Feedback report | 供下一轮智能体读取的结构化学习记录 | `experiments/*/latest.json` |
| Regression | 证明新规则没有破坏旧 probe 的验证过程 | `npm run verify` |
| Candidate update | 反馈报告中给下一轮维护者的目标文件、规则和验证命令 | `candidate_update` |
| Source status | 来源在课程中的可信度和处理阶段 | [来源登记](/zh-cn/appendix/source-registry) |
| Engineering forgetting | 新规则修复一个场景却破坏旧行为、测试或记忆的退化 | [第 3 讲](/zh-cn/slides/lecture-3/) |
| Maintenance cost | 一次更新需要修改和审查的软件结构数量与耦合风险 | [研究框架](/zh-cn/theory/research-framework) |

## 与相邻领域的边界

| 领域 | HL 借鉴什么 | HL 不声称什么 |
| --- | --- | --- |
| Deep Learning | 表征、感知模型和端到端训练经验 | 不把所有学习都还原成权重更新 |
| Reinforcement Learning | 状态、动作、奖励、策略和回放语言 | 不把每次策略改进都解释成梯度或价值函数更新 |
| 软件工程 | 测试、CI、代码审查、回归验证 | 不把普通重构包装成学习 |
| 规则系统 | 可解释策略、阈值、检测器和专家经验 | 不回到不可维护的规则堆叠 |

## 课程使用规则

- 新术语进入正文前，先判断它能否指向来源、示例、报告或测试。
- 未验证的术语只能写成研究假设，不能写成结论。
- 如果一个术语不能帮助读者运行、修改或验证系统，先不要扩展主线。

相关阅读：[HL 基础概念](/zh-cn/stage-2/)、[学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework)。
