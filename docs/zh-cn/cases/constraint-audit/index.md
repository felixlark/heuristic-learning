---
title: 事实约束审计案例
description: 用闭世界约束检查研究“生成与核验分离”的边界
---

# 事实约束审计案例

| 维度 | 内容 |
| --- | --- |
| 类型 | 研究假设最小环境 |
| 对应示例 | `examples/constraint-audit/` |
| Failure mode | `accepted_constraint_violation` |
| 学习重点 | 已知矛盾、未知主张与外部证据的区分 |

## 问题压缩

生成模型可能把看似连贯的句子当成答案。这个案例不尝试直接判断开放世界的“真相”，而是给出一个小型、可审计的事实目录。策略必须区分三种状态：目录支持、目录冲突、目录未知。

baseline 无条件接受。heuristic 只在目录支持时接受；目录冲突时要求修订；目录未知时升级为外部证据请求。

## 运行与验证

```bash
npm run examples:constraint-audit
npm run examples:constraint-audit:feedback
npm run examples:test
```

## 来源与边界

本案例受 SelfCheckGPT、Chain-of-Verification 和原子事实评估的公开研究启发，但不是这些方法的复现。它没有调用语言模型、检索系统或对抗训练；更不证明任何纳什均衡或通用去幻觉能力。研究设计与反驳条件见 [事实约束审计研究](/zh-cn/appendix/constraint-audit)。
