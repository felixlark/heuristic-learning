---
title: 课程评分与验收 Rubric
description: Heuristic Learning 作业、案例和实验贡献的验收标准
---

# 课程评分与验收 Rubric

本页用于判断一份 HL 作业、案例卡或实验贡献是否达到课程仓库标准。它不是考试分数表，而是研究仓库的质量门槛：内容必须可追溯、可运行、可复盘、可维护。

实验设计的 baseline、probe、report 和 regression gate 细则见 [实验协议](/zh-cn/appendix/benchmark-protocol)。Rubric 负责评分，实验协议负责判断证据是否足够稳定。

机器可读评分表见 [`/rubric.json`](/rubric.json)，字段约束见 [`/rubric.schema.json`](/rubric.schema.json)。`npm run rubric:check` 会检查权重总和、评分档位、证据路径和页面文本是否一致。

## 总分结构

| 模块 | 权重 | 最低通过标准 |
| --- | --- | --- |
| 来源与问题定义 | 20 | 有可追溯来源，并能说明它为什么是 HL 问题 |
| Probe 与 baseline | 20 | 能稳定复现一个失败模式，而不是只讲平均表现 |
| Heuristic patch | 20 | 更新对象可审查，且解释了为什么改这个结构 |
| 反馈报告 | 20 | 产物能被下一轮编码智能体读取 |
| 回归验证与课程表达 | 20 | 有测试、命令、文档落点，并通过统一验证 |

建议通过线为 80 分。低于 60 分的材料只能留作线索，不能进入主线课程。

## 来源与问题定义

| 分数 | 标准 |
| --- | --- |
| 0 | 没有来源，只是概念判断 |
| 5 | 有来源，但没有区分一手来源、二手转述或内部线索 |
| 10 | 来源清楚，但没有写入 [来源登记](/zh-cn/appendix/source-registry) |
| 15 | 来源、状态和边界清楚，能说明状态、动作、反馈和更新对象 |
| 20 | 还能说明哪些主张已验证，哪些只是研究假设 |

合格产物：

- `templates/case-card.md` 中的 Source 字段完整。
- 来源登记状态是 `已复现`、`已结构化`、`已定位` 或 `待采集` 之一。
- 未验证主张不会被写成确定结论。

## Probe 与 Baseline

| 分数 | 标准 |
| --- | --- |
| 0 | 只有最终分数或成功截图 |
| 5 | 有失败描述，但不能稳定复现 |
| 10 | 有最小失败场景，但 baseline 行为不清楚 |
| 15 | baseline 能稳定触发 probe，失败原因可解释 |
| 20 | probe 已进入测试或 replay，并能在 feedback report 中被引用 |

合格产物：

- 有明确 failure mode，例如 `yaw_drift`、`spillback`、`blocked_shot`。
- baseline 是自然但不充分的策略，不是随意写坏。
- probe 能通过 `npm run examples:test` 或固定 replay 验证。

## Heuristic Patch

| 分数 | 标准 |
| --- | --- |
| 0 | 只说“改进策略”，没有说明改哪里 |
| 5 | 改了策略，但无法解释更新对象 |
| 10 | 更新对象明确，但没有讨论维护风险 |
| 15 | patch 可审查，并解释了与 baseline failure 的关系 |
| 20 | patch、测试和报告一起更新，且保留旧 probe |

合格产物：

- 能指出目标文件，例如 `examples/breakout-replay/policies.py`。
- 能说明 patch 类型：阈值、几何预测、控制参数、安全约束或动作前检查。
- 不把“更多规则”当成自动进步，必须解释边界。

## 反馈报告

| 分数 | 标准 |
| --- | --- |
| 0 | 没有记录 |
| 5 | 有自然语言日志，但下一轮智能体难以读取 |
| 10 | 有结构化记录，但缺 baseline/heuristic 对照 |
| 15 | 报告包含 policies、feedback 和 candidate update |
| 20 | 报告能通过 `npm run examples:reports:check` |

合格产物：

- `experiments/*/latest.json` 被重新生成。
- `candidate_update.target` 指向下一轮可维护文件。
- `candidate_update.verification` 指向统一测试命令。

## 回归验证与课程表达

| 分数 | 标准 |
| --- | --- |
| 0 | 没有验证命令 |
| 5 | 只跑了单个脚本，没有测试 |
| 10 | 有测试，但文档和课程矩阵没有同步 |
| 15 | 测试、报告、文档和来源登记同步 |
| 20 | `npm run verify` 通过，并且有课程页或讲义落点 |

合格产物：

- 至少能跑 `npm run examples:test`。
- 主线贡献必须通过 `npm run verify`。
- 新增页面必须进入 sidebar、syllabus、source registry 或 structure check 中的相应位置。
- PR 必须通过 GitHub Actions 的 `Verify course repository` workflow。

## 作业提交清单

每次课程练习或研究贡献，至少交付：

```text
1. case card 或 experiment record
2. 运行命令和测试命令
3. baseline failure 的一句话解释
4. heuristic patch 的目标文件和维护风险
5. feedback report 路径
6. verify 结果
```

## 维护者验收顺序

1. 读来源登记，确认没有把线索写成事实。
2. 跑示例命令，确认 baseline 和 heuristic 行为可观察。
3. 读 `experiments/*/latest.json`，确认下一轮智能体能接着维护。
4. 跑 `npm run verify`。
5. 检查课程页是否能让学生复述 signal、probe、patch 和 regression。

这套 Rubric 也适用于未来的 PR review：先看证据链，再看实现风格。
