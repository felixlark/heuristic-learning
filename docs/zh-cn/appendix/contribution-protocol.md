---
title: 贡献与研究协议
description: Heuristic Learning 仓库的案例、实验和章节贡献标准
---

# 贡献与研究协议

HL 还处在思想沉淀期，因此课程的贡献标准不是“多写内容”，而是“让每条内容可追溯、可运行或可验证”。

具体评分与验收标准见 [课程评分与验收 Rubric](/zh-cn/appendix/rubric)。本页定义贡献门槛，Rubric 用于判断一份作业或 PR 是否达到课程标准。
实验设计细则见 [实验协议](/zh-cn/appendix/benchmark-protocol)，新增主线实验必须符合其中的 baseline、probe、report 和 regression gate 要求。

GitHub 贡献入口见根目录 `CONTRIBUTING.md`，PR 会使用 `.github/pull_request_template.md` 要求填写来源、失败模式、运行命令、反馈报告、测试路径和统一验证结果。

机器可读贡献契约见 [`/contribution-contract.json`](/contribution-contract.json)，字段约束见 [`/contribution-contract.schema.json`](/contribution-contract.schema.json)。`npm run contribution:contract:check` 会检查贡献类型、证据字段、必备路径、验证命令和禁止材料是否仍与 `CONTRIBUTING.md`、PR 模板和本页一致。

## 新增理论章节

理论章节必须包含：

- 一个清晰问题。
- 一个来自公开源、脱敏应用问题或课程实验的动机。
- 一个最小定义或对照表。
- 至少一个指向案例或 runnable example 的链接。
- 一个对应的 [来源登记](/zh-cn/appendix/source-registry) 状态。

## 新增案例

案例必须回答：

| 字段 | 要求 |
| --- | --- |
| 环境 | 任务发生在哪里，例如 Atari、VizDoom、机器人足球 |
| 状态 | 系统能观察什么 |
| 动作 | 策略能做什么 |
| 反馈 | 奖励、测试、日志、回放或人类评价 |
| 更新对象 | 代码、规则、测试、配置、记忆或文档 |
| 验证 | 如何证明新规则没有破坏旧场景 |
| 来源状态 | 已复现、已结构化、已定位或待采集 |

## 新增实验

实验必须提供：

- 一条运行命令。
- 一条测试命令。
- 一个可读的反馈记录，推荐 JSON 或 Markdown。
- 一个明确的失败场景或 probe，避免只报告平均指标。
- 能通过 `npm run verify`，包括重新生成 feedback report 和报告结构检查。
- 能通过 `npm run course:structure:check`，确认课程矩阵、脚本和实验产物同步。
- 能通过 `npm run contribution:contract:check`，确认贡献路径、证据字段和禁止材料没有漂移。

如果本次贡献只是记录一次运行、解释报告或提出下一轮候选更新，先使用 `templates/experiment-record.md`。实验记录必须说明运行命令、来源状态、结果摘要、反馈、candidate update 和验证命令；它可以升级为 runnable example、ablation plan 或 research logbook，但不能替代测试和反馈报告。

当前主线实验：

| 实验 | 作用 |
| --- | --- |
| `examples/heuristic-gridworld/` | 最小网格世界，展示局部陷阱 probe |
| `examples/ant-gait-replay/` | MuJoCo Ant gait replay，展示连续控制 heuristic 如何转成轻量回归实验 |
| `examples/breakout-replay/` | Atari Breakout wall-reflection replay，展示几何预测如何转成轻量回归实验 |
| `examples/robot-soccer/` | 机器人足球 blocked-lane probe，展示应用案例如何转成可测试规则 |
| `examples/vizdoom-replay/` | VizDoom D1 medikit-staging replay，展示视觉游戏 artifact 如何转成轻量回归实验 |
| `examples/traffic-grid/` | 交通模拟 downstream spillback probe，展示工程规则如何用 replay 和测试维护 |

## 新增复现记录

复现记录用于把公开 artifact、X 来源或脱敏应用问题转成研究仓库可以审查的证据。它不等同于“已经完全复现真实环境”，而是把当前能验证的范围、不能验证的缺口和下一步实验分开。

使用 `templates/reproduction-note.md` 时必须填写：

| 字段 | 要求 |
| --- | --- |
| 来源状态 | 已复核摘要、待直接复核、待采集、已定位或已复现，不能越级声明 |
| 复现范围 | 当前是文章理解、代码 artifact 阅读、轻量 replay、固定 probe 还是高保真环境 |
| 缺失保真度 | 真实环境、视觉检测、物理接触、随机种子、控制接口或数据来源中的具体缺口 |
| 反驳路径 | 什么结果会推翻当前 heuristic 解释 |
| 下一步实验 | 一个最小可执行动作，优先绑定案例、示例、指标或 artifact gap |

复现记录必须至少运行：

```bash
npm run source:registry:check
npm run artifact:gap:check
npm run research:logbook:check
npm run source:case:check
```

如果复现记录进一步升级为主线案例或示例，还要补齐 case card、example registry、feedback report、test 和 `npm run verify`。

统一验证入口：

```bash
npm run verify
```

这个命令会重新生成主线实验的 `experiments/*/latest.json`，并用 `scripts/check-experiment-reports.py` 检查每个报告是否包含 baseline/heuristic 对照、feedback 和下一轮可维护的 candidate update。
同时，`scripts/check-course-structure.py` 会检查课程页面、示例目录、package scripts、测试文件和课程大纲矩阵是否一致。
GitHub Actions 的 `Verify course repository` workflow 和 Pages 部署也会运行同一条验证命令，因此 PR、主分支和发布站点使用同一套课程门槛。

## 禁止事项

- 不把未验证的 X/脱敏应用问题写成确定事实。
- 不提交只有叙述、没有来源或实验入口的“研究结论”。
- 不新增无法在本地验证的示例作为主线课程内容。
- 不跳过来源登记直接把案例写进主线章节。
