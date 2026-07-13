---
title: 练习集
description: Heuristic Learning 课程的概念题、代码题、实验题和 capstone 题库
---

# 练习集

本页把 HL 课程拆成可布置、可验收的练习。每道题都绑定一个课程页面、一个示例或模板，以及一条验证命令。练习的目标不是记住定义，而是能把“失败、反馈、更新、验证”写成可复查的 artifact。

机器可读练习矩阵见 [`/exercise-registry.json`](/exercise-registry.json)，字段约束见 [`/exercise-registry.schema.json`](/exercise-registry.schema.json)。`npm run exercises:check` 会检查练习题、输入材料、示例、验收命令、学习单元和 Rubric 模块是否仍然互相对齐。

## 使用方式

| 难度 | 适合对象 | 产出 | 验收 |
| --- | --- | --- | --- |
| A. 概念题 | 初学者、读书会 | 3-5 行解释或对照表 | 能引用课程页和来源状态 |
| B. 代码题 | 动手练习 | 一个小 patch 或测试 | `npm run examples:test` |
| C. 实验题 | 研究训练、课程作业 | experiment record + report | `npm run verify` |
| D. Capstone | 课程项目、研究 repo 贡献 | case card + runnable example + docs | Rubric 80 分以上 |

所有提交都应参考 [实验协议](/zh-cn/appendix/benchmark-protocol) 和 [课程 Rubric](/zh-cn/appendix/rubric)。

## A. 概念题

| 题目 | 输入材料 | 合格答案 |
| --- | --- | --- |
| A1. 定义 HL | [HL 基础概念](/zh-cn/stage-2/)、[学习闭环](/zh-cn/theory/learning-loop) | 能说明反馈来源、更新对象和验证方式 |
| A2. 对比 RL/DL/HL | [从 RL/DL 到 HL](/zh-cn/stage-3/) | 能指出 HL 不替代 RL/DL，而是更新不同对象 |
| A3. 判断是否属于 HL | [研究框架](/zh-cn/theory/research-framework) | 能用四个最小条件判断一个案例 |
| A4. 来源状态分级 | [来源登记](/zh-cn/appendix/source-registry) | 能区分已复现、已结构化、已定位、待采集 |
| A5. 为什么需要反遗忘 | [第 3 讲](/zh-cn/talk/)、[Lab 2](/zh-cn/theory/learning-loop) | 能给出一个“修复当前失败但破坏旧经验”的例子 |

概念题不需要跑代码，但不能只给口号。答案必须引用一个页面、一个示例或一个来源状态。

## B. 代码题

| 题目 | 示例 | 任务 | 验证 |
| --- | --- | --- | --- |
| B1. GridWorld 新陷阱 | `examples/heuristic-gridworld/` | 增加一个不破坏最短安全路径的陷阱或测试 | `npm run examples:test` |
| B2. Robot Soccer 安全路线 | `examples/robot-soccer/` | 调整 blocked-lane 后的换线策略 | `npm run examples:robot-soccer:feedback` |
| B3. VizDoom 阈值边界 | `examples/vizdoom-replay/` | 解释并测试 `pickup_health` 或 `stage_area` 的边界 | `npm run examples:vizdoom-replay:feedback` |
| B4. Breakout 反射截点 | `examples/breakout-replay/` | 添加一个侧墙反射变体测试 | `npm run examples:breakout-replay:feedback` |
| B5. Ant yaw 反馈 | `examples/ant-gait-replay/` | 调整 yaw feedback 后保持 `stable_stride` | `npm run examples:ant-gait-replay:feedback` |
| B6. Traffic Grid 容量保护 | `examples/traffic-grid/` | 增加一个下游容量临界 probe | `npm run examples:traffic-grid:feedback` |

代码题的最低要求：

```bash
npm run examples:test
npm run examples:feedback
npm run examples:reports:check
```

如果改动会改变主线报告，必须说明为什么报告变化是预期行为。

## C. 实验题

每个实验题提交一份 `templates/experiment-record.md` 风格记录。

| 题目 | 研究问题 | 必填证据 |
| --- | --- | --- |
| C1. Baseline 是否合理 | 当前六个示例任选一个 | 说明 baseline 为什么不是故意写坏 |
| C2. Probe 是否稳定 | 当前六个 probe 任选一个 | 给出测试或 replay 如何稳定触发 failure mode |
| C3. Report 是否足够给下一轮智能体使用 | 任一 `experiments/*/latest.json` | 指出 `candidate_update.target/rule/verification` |
| C4. 反遗忘路径 | 任一 heuristic patch | 按 `templates/anti-forgetting-checklist.md` 写一个坏更新，并说明哪个测试会阻止它 |
| C5. 学习材料一致性 | 任一示例 | 检查 README、课程大纲、案例页和 report 是否一致 |

实验题统一验收：

```bash
npm run verify
```

验收时还要读记录本身。通过命令只能证明仓库当前一致，不能证明读者已经理解 failure mode。

## D. Capstone 题

Capstone 从一个来源线索开始，最终进入课程仓库。

| 题目 | 输入 | 输出 |
| --- | --- | --- |
| D1. X case card | Jiayi 或社区 X 来源；先按 [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook) 区分 “已复核摘要”“待直接复核”“待采集” | 来源登记条目 + case card + 验证状态 |
| D2. 公开 artifact replay | `learning-beyond-gradients` 未复现 artifact | 轻量 replay + feedback report + test |
| D3. 脱敏应用问题最小环境 | 脱敏应用问题 | 不泄露敏感信息的 minimal example |
| D4. 反遗忘扩展 | 现有示例的新 failure mode | 新 probe + 测试 + report 边界说明 |
| D5. 课程讲义扩展 | 一个已验证案例 | lecture 或 lab 页面 + demo 命令 |

Capstone 最小交付：

```text
1. 来源登记状态
2. case card
3. baseline failure
4. heuristic patch
5. feedback report
6. regression test
7. docs 落点
8. npm run verify 结果
```

## 评分建议

| 练习 | 建议权重 |
| --- | --- |
| A 概念题 | 20% |
| B 代码题 | 30% |
| C 实验题 | 30% |
| D Capstone | 20% |

如果是短工作坊，可以只选 A1、B1、C3。完整课程建议每周至少完成一道 B 题或 C 题，最后用 D 题作为项目验收。

## 维护要求

新增练习必须满足：

- 指向一个现有课程页、案例页、示例或模板。
- 包含明确验证命令。
- 不把未验证来源写成事实。
- 如果新增主线示例，必须更新 [课程大纲](/zh-cn/syllabus/)、[来源登记](/zh-cn/appendix/source-registry)、[实验协议](/zh-cn/appendix/benchmark-protocol)、`course-manifest.json` 和结构检查脚本。
