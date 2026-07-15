---
title: 事实约束审计研究
description: 将自检与对抗性主张转成可反驳的闭世界约束实验
---

# 事实约束审计研究

“让模型扮演事实与幻觉两个角色、通过博弈收敛”是一个值得检验的研究想法，不是当前课程的结论。这个页面把它缩小为更严格的问题：**在已给定、可审计的事实目录里，独立的约束检查能否阻止一个已知矛盾被直接接受？**

这与真实世界事实核查不同。真实世界的知识不完整、会随时间变化，并且需要可信的检索源；本实验故意不把“模型自洽”当成“事实为真”。

## 相关公开研究

[SelfCheckGPT](https://aclanthology.org/2023.emnlp-main.557/) 用多次采样的一致性来检测黑盒生成中的潜在幻觉；[Chain-of-Verification](https://aclanthology.org/2024.findings-acl.212/) 将草稿、验证问题、独立作答和最终修订拆开。二者支持“把生成与核验分离”作为可研究方向，但都不推出纳什均衡、也不保证无外部证据时的事实正确性。

[FActScore](https://aclanthology.org/2023.emnlp-main.741/) 进一步提醒我们：评估应落到原子事实和可追溯知识源，而不是只检查一句话内部是否自洽。

## 最小实验

```bash
npm run examples:constraint-audit
npm run examples:constraint-audit:feedback
npm run examples:test
```

代码和报告：

```text
examples/constraint-audit/
experiments/constraint-audit/latest.json
tests/test_constraint_audit.py
```

实验有一个封闭事实目录，以及四条“对抗性”候选主张：两条与目录冲突、一条目录支持、一条目录未知。

| 策略 | 已知矛盾 | 目录未知 | 结果 |
| --- | --- | --- | --- |
| baseline | 直接接受 | 直接接受 | `accepted_constraint_violation` |
| constraint audit | 阻断并要求修订 | 请求外部证据 | `blocked_constraint_violation` |

这里的 `adversarial` 只指测试夹具刻意提供反例，不表示两个语言模型在训练、博弈或达到均衡。

## 能与不能说明什么

这个实例可以说明：把“已知约束冲突”和“未知、需要外部证据”分开，会比无条件接受更可审计，也更容易写成回归测试。

它不能说明：

- 约束目录本身完整或永远正确；
- 自博弈会收敛到纳什均衡；
- 检出逻辑矛盾就等同于检出所有幻觉；
- 该机制不降低答案质量，或无需任何标注/检索成本；
- 该夹具的结果能迁移到通用大模型、医疗、法律或其他高风险事实任务。

## 可反驳的下一步

要推进成实证研究，至少需要：

1. 将原子主张绑定到时间戳、来源 URI 和可失效的证据片段。
2. 把“生成者”和“审计者”在模型、提示、证据或采样上真正独立化，避免同一错误被重复确认。
3. 在有标注的事实性数据集上同时报告精度、召回、拒答率、覆盖率和答案效用；未知主张不能被当作错误或事实。
4. 增加反例：目录过期、来源冲突、表述歧义与真实但罕见的主张。
5. 将任何“自博弈/均衡”表述改成可观测变量，例如策略稳定性、错误相关性与跨模型泛化，而不是用电影类比替代评估。

它是 [研究框架](/zh-cn/theory/research-framework) 中“事实约束审计能否成为可维护反馈通道？”的最小研究夹具；完整验证仍使用：

```bash
npm run examples:constraint-audit:feedback
npm run examples:reports:check
npm run claims:registry:check
npm run verify
```
