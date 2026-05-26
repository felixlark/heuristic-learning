---
title: 阶段检查点
description: Heuristic Learning 学习单元的自测问题、证据、命令和通过条件
---

# 阶段检查点

本页给读者、助教和编码智能体一个更细的学习验收入口。学习单元回答“读什么、跑什么、交付什么”，学习成果回答“最终会什么”，阶段检查点回答“这一段学完怎么判断自己真的会了”。

机器可读检查点见 [`/checkpoint-registry.json`](/checkpoint-registry.json)，字段约束见 [`/checkpoint-registry.schema.json`](/checkpoint-registry.schema.json)。`npm run checkpoints:check` 会检查每个检查点是否绑定学习单元、学习成果、证据路径和验证命令。

## 检查点总览

| 检查点 | 对应单元 | 自测问题 | 验证命令 |
| --- | --- | --- | --- |
| CP0 建立语境自测 | U0 | 能否解释 HL、Heuristic System、RL/DL 分工和研究假设边界？ | `npm run claims:registry:check` |
| CP1 最小闭环自测 | U1 | 能否跑通 GridWorld feedback 并解释 report？ | `npm run examples:gridworld:feedback` |
| CP2 公开来源自测 | U2 | 能否区分公开 artifact、X 来源和待采集来源？ | `npm run source:registry:check` |
| CP3 系统控制自测 | U3 | 能否说明动作前提、安全约束和 regression probe？ | `npm run examples:test` |
| CP4 研究问题自测 | U4 | 能否把研究问题写成可反驳的 claim review？ | `npm run claims:registry:check` |
| CP5 反遗忘项目自测 | U5 | 能否提交包含旧行为、风险更新、回归保护和 verify 证据的项目？ | `npm run verify` |

## 使用方式

学习自查：

1. 先读 [学习单元矩阵](/zh-cn/appendix/learning-units)，确认当前所在单元。
2. 回到本页回答对应检查点问题。
3. 打开 `/checkpoint-registry.json` 查看 evidence、pass_condition 和 common_failure。
4. 运行检查点绑定的 verification commands。

教师或助教验收：

1. 用检查点决定课堂 exit ticket 或每周小作业。
2. 如果只跑通命令，但无法解释 `pass_condition` 中的证据链，不能判定通过。
3. 如果课程单元、学习成果或练习题调整，先更新 `/checkpoint-registry.json`。

## 命令集合

```bash
npm run checkpoints:check
npm run claims:registry:check
npm run examples:gridworld:feedback
npm run examples:reports:check
npm run source:registry:check
npm run cases:check
npm run x:sources:check
npm run examples:robot-soccer:feedback
npm run examples:traffic-grid:feedback
npm run examples:test
npm run research:projects:check
npm run exercises:check
npm run reproducibility:check
npm run verify
```

## 边界

- 阶段检查点不是自动评分器；它只证明证据、命令和学习目标没有漂移。
- 检查点要保留 common_failure，因为 HL 的学习重点经常藏在“错误但看似合理”的更新里。
- 新增主线单元时，必须同步检查点，或明确说明它复用已有检查点。
