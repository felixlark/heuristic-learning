---
title: 实验协议
description: Heuristic Learning 示例、案例和课程项目的实验设计协议
---

# 实验协议

本页定义 HL 仓库的最小实验协议。它的作用类似教学型深度学习仓库里的 benchmark 说明：不是为了追求统一分数榜，而是保证每个案例都能被复查、复跑、比较和维护。

六个主线示例的当前结果摘要见 [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)，机器可读入口为 [`/benchmark-summary.json`](/benchmark-summary.json)。

## 实验单元

一个 HL 实验单元至少包含：

| 部分 | 要求 | 仓库落点 |
| --- | --- | --- |
| case signal | 来源、任务和失败线索 | [来源登记](/zh-cn/appendix/source-registry)、案例页 |
| environment 或 replay | 可复现状态转移或固定轨迹 | `examples/*/env.py`、`examples/*/replay_env.py` |
| baseline | 自然但不充分的策略 | `examples/*/policies.py` |
| failure mode | 能稳定触发的 probe | 测试、报告、案例页 |
| heuristic patch | 可审查的软件结构更新 | policy、阈值、检测器、配置或测试 |
| feedback report | 给下一轮智能体读取的记录 | `experiments/*/latest.json` |
| regression gate | 防止旧经验退化 | `tests/test_*.py`、`npm run verify` |

如果某个实验缺少 baseline failure，它只能算 demo，不能算 HL 主线实验。

## Baseline 设计

baseline 不能故意写坏。它应该是一个合理但局部不足的策略，让 failure mode 有研究意义。

| 类型 | 合格 baseline | 不合格 baseline |
| --- | --- | --- |
| 贪心策略 | GridWorld 中靠近目标但忽略陷阱 | 随机乱走 |
| 直接动作 | Robot Soccer 中拿球后直接射门 | 永远不射门 |
| 当前观测追踪 | Breakout 中追当前球 x | 固定不移动 |
| 固定阈值 | VizDoom 中看到 medikit 就拾取 | 忽略所有 medikit |
| 固定控制参数 | Ant 中固定节律面对 yaw 扰动 | 输出无意义动作 |
| 局部队列优先 | Traffic Grid 中优先放行最大上游队列 | 不放行任何车辆 |

好的 baseline 应该让读者理解：heuristic patch 修复的是一个具体判断缺口，而不是修复人为制造的坏代码。

## Probe 设计

每个 probe 需要满足四个条件：

1. 能稳定复现 failure mode。
2. 能被测试或 replay 捕获。
3. 能说明 baseline 为什么失败。
4. 能暴露 heuristic patch 的维护边界。

主线 probe 当前包括：

| Probe | 示例 | 验证入口 |
| --- | --- | --- |
| `local_greedy_trap` | GridWorld | `npm run examples:test` |
| `blocked_shot` | Robot Soccer | `npm run examples:robot-soccer:feedback` |
| `wasted_pickup` | VizDoom Replay | `npm run examples:vizdoom-replay:feedback` |
| `spillback` | Traffic Grid | `npm run examples:traffic-grid:feedback` |
| `missed_after_wall_reflection` | Breakout Replay | `npm run examples:breakout-replay:feedback` |
| `yaw_drift` | Ant Gait Replay | `npm run examples:ant-gait-replay:feedback` |

新增 probe 时，优先把它写进测试，再改策略。这样可以把“学习前的失败”保留下来，避免后续只能看到最终成功。

## Report 协议

主线 `experiments/*/latest.json` 至少要让下一轮智能体回答：

- 这个实验的环境或 replay 是什么？
- baseline 和 heuristic 的结果分别是什么？
- failure mode 是如何被隔离的？
- 本轮反馈要求下一轮维护什么？
- 下一轮修改应该跑哪条验证命令？

因此报告必须保留：

```text
policies
feedback
candidate_update.target
candidate_update.rule
candidate_update.verification
```

字段约束见 [`/experiment-report.schema.json`](/experiment-report.schema.json)，结构检查由 `npm run examples:reports:check` 执行。

## 对照与消融

当一个项目从课程练习升级为研究贡献时，至少补一个对照：

| 对照 | 问题 | 示例 |
| --- | --- | --- |
| 无 patch | baseline failure 是否真实存在？ | `baseline` vs `heuristic` |
| 单规则移除 | 哪条规则真正关键？ | 移除 Breakout 侧墙反射预测 |
| 阈值扰动 | patch 是否只对单一数值有效？ | VizDoom pickup health threshold |
| 旧 probe 回放 | 新规则是否破坏旧场景？ | `npm run examples:test` |
| 文档对照 | 课程解释是否匹配代码行为？ | syllabus、case page、README 同步 |

不要求每个课程示例都做完整消融，但研究型项目和 capstone 至少要说明为什么当前对照足以支撑结论。六个主线示例的下一步变量对照见 [消融计划](/zh-cn/appendix/ablation-plan)，机器入口为 `/ablation-plan.json`，更新后运行 `npm run ablation:plan:check`。

## 负结果记录

HL 仓库允许保留负结果。一个失败 patch 有价值，只要它能说明：

- 它试图修复哪个 failure mode。
- 它破坏了哪个旧 probe。
- 它暴露了什么规则冲突或状态检测缺口。
- 后续应该补什么测试、检测器或来源。

负结果不能直接覆盖 `latest.json` 作为主线成功报告，但可以进入 `templates/experiment-record.md` 风格的实验记录、案例页的“失败变体”段落或研究路线图待办。

## 验收顺序

维护者审查一个实验时按这个顺序：

```bash
npm run examples:test
npm run examples:feedback
npm run examples:reports:check
npm run benchmark:summary:check
npm run source:registry:check
npm run course:structure:check
npm run verify
```

局部命令用于定位问题，`npm run verify` 是最终门槛。通过单个脚本不等于实验完成；只有来源、示例、报告、测试和课程页面都对齐，才算进入主线课程。

## 与课程材料的关系

- [研究框架](/zh-cn/theory/research-framework) 定义什么问题属于 HL。
- [研究课题](/zh-cn/appendix/research-projects) 给出可选项目。
- [课程 Rubric](/zh-cn/appendix/rubric) 给出评分标准。
- 本页定义实验怎么设计和验收。

四者必须一起使用：没有实验协议，Rubric 会变成主观评分；没有 Rubric，实验协议会变成机械检查；没有来源登记，实验结果会失去可追溯性。
