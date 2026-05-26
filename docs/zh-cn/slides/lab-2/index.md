---
title: Lab 2：反遗忘审查
description: 第 3 讲配套实验：用测试、反馈报告和 Rubric 审查一次 HL 更新
---

# Lab 2：反遗忘审查

本实验对应 [第 3 讲：失败类型与反遗忘](/zh-cn/slides/lecture-3/)。目标不是追求一次更聪明的 heuristic，而是学会判断一次更新是否会破坏旧经验。

## 时间安排

| 时间 | 任务 | 产出 |
| --- | --- | --- |
| 0-10 分钟 | 跑统一验证，建立干净基线 | `npm run verify` 通过 |
| 10-25 分钟 | 选择一个案例并定位 failure probe | 一条 failure taxonomy 记录 |
| 25-45 分钟 | 设计一个“可能遗忘”的更新 | 一条 anti-forgetting checklist |
| 45-65 分钟 | 找到或补充对应回归测试 | 测试命令和覆盖说明 |
| 65-90 分钟 | 重新生成报告并按 Rubric 评分 | 一份 80 分制以上的实验记录 |

## 准备

```bash
npm install
npm run verify
```

如果仓库当前不能通过 `verify`，本实验不能开始。反遗忘审查的前提是已有反馈通道可信；否则你无法判断新失败来自策略更新，还是来自测试、报告或文档结构漂移。

## Step 1：选择一个失败类型

任选一个示例，先不要改代码。用下面表格把它归类：

| 示例 | 失败类型 | probe | 回归问题 |
| --- | --- | --- | --- |
| GridWorld | 局部贪心 | `local_greedy_trap` | 避开陷阱后是否仍能到达目标 |
| Robot Soccer | 动作前提缺失 | `blocked_shot` | 换线后是否仍会在通道安全时射门 |
| VizDoom | 资源时机错误 | `wasted_pickup` | 延迟拾取后是否仍会在低血量拾取 |
| Breakout | 物理预测不足 | `missed_after_wall_reflection` | 反射预测后是否仍能处理直线球 |
| Ant Gait | 控制稳定性退化 | `yaw_drift` | 抑制偏航后是否仍能向前推进 |
| Traffic Grid | 系统容量约束缺失 | `spillback` | 保护下游容量后是否仍保持吞吐 |

记录格式：

```text
案例：
失败类型：
当前 probe：
旧经验：
不能破坏的行为：
```

## Step 2：设计一个坏更新

写出一个看起来能修复当前 probe、但可能造成遗忘的更新。不要真的提交坏策略。

示例：

| 案例 | 坏更新 | 可能遗忘 |
| --- | --- | --- |
| GridWorld | 永远避开某一列 | 可达路径被错误封死 |
| Robot Soccer | 只要有人挡路就停止进攻 | 安全通道也不再射门 |
| VizDoom | 永远推迟 medikit | 低血量错过资源 |
| Breakout | 总是向预测截点移动 | 近距离直线球反应变慢 |
| Ant Gait | 只增大 yaw feedback | 前进速度和稳定性耦合失衡 |
| Traffic Grid | 下游接近容量就永久 hold | 吞吐下降，队列不再释放 |

这一步的产出是一条 anti-forgetting checklist。可以直接使用 `templates/anti-forgetting-checklist.md`，也可以用下面的短格式：

```text
坏更新：
能修复什么：
会破坏什么：
需要哪个测试保护：
需要哪个 report 字段提醒下一轮智能体：
```

## Step 3：检查测试覆盖

先看已有测试：

```bash
npm run examples:test
```

然后打开对应测试文件，确认它是否覆盖了“不能破坏的行为”。如果没有覆盖，补一个最小断言。测试应该短小、确定、能解释失败原因。

常用定位：

| 示例 | 测试文件 |
| --- | --- |
| GridWorld | `tests/test_gridworld.py` |
| Robot Soccer | `tests/test_robot_soccer.py` |
| VizDoom | `tests/test_vizdoom_replay.py` |
| Breakout | `tests/test_breakout_replay.py` |
| Ant Gait | `tests/test_ant_gait_replay.py` |
| Traffic Grid | `tests/test_traffic_grid.py` |

## Step 4：更新反馈报告

重新生成报告：

```bash
npm run examples:feedback
npm run examples:reports:check
```

检查对应 `experiments/*/latest.json`：

- `policies` 是否仍保留 baseline 与 heuristic 对照。
- `feedback` 是否说明当前规则的维护边界。
- `candidate_update.target` 是否指向真实可维护文件。
- `candidate_update.verification` 是否仍能指导下一轮智能体运行测试。

## Step 5：按 Rubric 自评

用 [课程评分与验收 Rubric](/zh-cn/appendix/rubric) 打分。Lab 2 的重点是最后两项：

| 模块 | 本实验最低要求 |
| --- | --- |
| Probe 与 baseline | 能说明旧 probe 为什么必须保留 |
| Heuristic patch | 能指出坏更新会破坏什么 |
| 反馈报告 | `candidate_update` 能提醒维护边界 |
| 回归验证与学习复盘 | `npm run verify` 通过，且有一段反遗忘记录 |

## 提交记录模板

```text
案例：
失败类型：
旧经验：
模拟坏更新：
新增或确认的回归测试：
反馈报告路径：
Rubric 自评分：
verify 结果：
剩余风险：
```

如果要把结果提交回仓库，建议把完整记录写成 `templates/anti-forgetting-checklist.md` 的结构：先列出旧经验，再列出坏更新、回归保护和 review 结论。这样助教或下一轮编码智能体可以直接判断这次 HL 更新是否只是修复了当前 probe，还是保留了旧行为。

## 验收标准

本 lab 完成的标准：

- 能解释“修复当前 probe”和“保留旧经验”的区别。
- 能指出至少一个工程型遗忘路径。
- 已确认或补充一个回归测试。
- `npm run examples:reports:check` 通过。
- `npm run verify` 通过。

进一步阅读：[研究框架](/zh-cn/theory/research-framework)、[研究路线图](/zh-cn/appendix/research-roadmap)。
可布置的反遗忘练习见 [练习集](/zh-cn/appendix/exercises) 的 C4 和 D4。
