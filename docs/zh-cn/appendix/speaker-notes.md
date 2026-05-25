---
title: 讲者备注
description: Heuristic Learning 讲义的开场问题、demo 节点、讨论题和 exit ticket
---

# 讲者备注

本页把 3 讲 + 2 Lab 从“能读的幻灯片”推进到“能上课的讲义”。每条备注都回答五件事：如何开场、demo 时停在哪里、问学生什么、常见误解是什么、最后收什么交付物。

机器可读备注见 [`/speaker-notes.json`](/speaker-notes.json)，字段约束见 [`/speaker-notes.schema.json`](/speaker-notes.schema.json)。`npm run speaker:notes:check` 会检查备注是否仍绑定现有讲义、命令、材料和 manifest。

## 备注矩阵

| 讲义 | 开场问题 | 课堂重点 | Exit ticket |
| --- | --- | --- | --- |
| 第 1 讲讲者备注 | 如果学习对象不是权重，学习闭环如何定义？ | GridWorld feedback report 与 candidate update | 用 3 句话解释一次 HL 更新需要保留哪些证据 |
| 第 2 讲讲者备注 | 一个线索怎样进入课程主线而不过度声明？ | source status、case card、轻量 replay 边界 | 提交一张 case card 草稿 |
| 第 3 讲讲者备注 | patch 通过当前 probe 后为什么仍可能破坏旧经验？ | 任务结果、失败隔离、更新成本、回归风险 | 写出坏更新和对应回归测试 |
| Lab 1 讲者备注 | 从失败 probe 到 feedback report 如何亲手跑通？ | 只改一个策略点，并同步测试和 report | 提交 experiment record |
| Lab 2 讲者备注 | 如何在写 patch 前预测它可能遗忘什么？ | 旧经验、坏更新、测试文件、Rubric 自评 | 提交 anti-forgetting checklist |

## 使用顺序

1. 先读 [Slides 目录](/zh-cn/slides/) 和对应讲义。
2. 打开 `/speaker-notes.json` 找到 `material_id`。
3. 按 `opening_question` 开场，用 `demo_checkpoints` 控制课堂节奏。
4. 课后按 `exit_ticket` 收作业，并运行对应 `verification_commands`。

## 维护规则

1. 新增讲义时，必须同步新增一条 speaker note。
2. 修改讲义命令时，必须同步更新 `/speaker-notes.json`。
3. 如果课堂讨论产生新案例，先进入 [来源登记](/zh-cn/appendix/source-registry) 或 [案例矩阵](/zh-cn/appendix/case-registry)，不要直接写成已复现。

```bash
npm run speaker:notes:check
npm run verify
```
