---
title: 学习成果矩阵
description: Heuristic Learning 课程的能力目标、证据、练习、Rubric 和验证命令
---

# 学习成果矩阵

本页定义读者完成课程后应具备的能力。它把学习单元、练习题、Rubric、证据路径和验证命令连成一张成果矩阵，让课程不只是“有哪些材料”，也能说明“学完能做什么”。

机器可读矩阵见 [`/learning-outcomes.json`](/learning-outcomes.json)，字段约束见 [`/learning-outcomes.schema.json`](/learning-outcomes.schema.json)。`npm run learning:outcomes:check` 会检查每个学习成果是否仍能连到学习单元、练习题、Rubric 模块、证据路径和验证命令。

## 成果总览

| 学习成果 | 能力表现 | 代表练习 | 验证命令 |
| --- | --- | --- | --- |
| LO1 解释 HL 问题边界 | 区分 HL、Heuristic System、RL/DL 分工和研究假设 | A1、A2、A3 | `npm run claims:registry:check` |
| LO2 运行并解释最小闭环 | 跑通示例，解释 baseline failure、heuristic outcome 和 feedback report | B1、C3 | `npm run examples:reports:check` |
| LO3 把来源转成案例证据 | 保留来源层级，写出 case card 和验证计划 | A4、D1、D3 | `npm run source:registry:check` |
| LO4 设计可维护 heuristic patch | 限定更新目标，并用测试或 replay 防退化 | B2、B4、B5、B6、C4、D4 | `npm run examples:test` |
| LO5 完成研究型课程交付 | 提交记录、报告、测试路径、Rubric 自评和 verify 结果 | C1、C2、C5、D2、D5 | `npm run verify` |

## 使用方式

学生自查：

1. 从本页选一个学习成果。
2. 打开 `/learning-outcomes.json` 查看绑定的练习和 Rubric 模块。
3. 完成对应练习，保留 evidence 中的页面、报告或模板路径。
4. 运行对应 verification command。

教师或助教验收：

1. 先看学生交付是否覆盖 `assessment`。
2. 再用 Rubric 判断质量，而不是只看命令是否通过。
3. 如果课程材料、练习或 Rubric 改动影响能力目标，先更新 `/learning-outcomes.json`。

本矩阵覆盖的局部命令：

```bash
npm run claims:registry:check
npm run examples:gridworld:feedback
npm run examples:reports:check
npm run source:registry:check
npm run x:sources:check
npm run examples:test
npm run examples:feedback
npm run exercises:check
npm run reproducibility:check
npm run verify
```

## 边界

- 学习成果不是自动评分器；命令只能证明仓库结构和证据链可复查。
- 如果学生只跑通命令但无法解释来源、failure mode、candidate update 或反遗忘边界，不能视为达成成果。
- 新增主线课程单元时，必须同步学习成果矩阵或说明它不改变现有能力目标。
