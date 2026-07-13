---
title: 研究路线图
description: Heuristic Learning 仓库后续实验、案例和课程扩展路线
---

# 研究路线图

本页把散落在案例页和来源登记中的“下一步”整理成可执行路线。每个里程碑都必须能落到来源、示例、报告、测试或课程页，不能只停留在愿望清单。

## v0.1：课程骨架稳定

当前状态：

| 维度 | 已完成证据 |
| --- | --- |
| 理论 | 基础概念、学习闭环、RL/DL/HL 对照、研究框架 |
| 实验 | 6 个纯 Python replay/minimal examples |
| 课程 | 第 1 讲、第 2 讲、第 3 讲、Lab 1、Lab 2、教师指南、研究课题、实验协议、Rubric |
| 追溯 | 来源登记、X 来源案例、course manifest |
| 验证 | `npm run verify`、GitHub Actions、Pages deploy gate |

v0.1 的维护原则是：新增内容必须继续通过 `npm run verify`，并更新 `/course-manifest.json`。

轻量 replay 到真实 artifact 的保真度差距由 [Artifact 差距分析](/zh-cn/appendix/artifact-gap-analysis) 维护，机器入口为 [`/artifact-gap-analysis.json`](/artifact-gap-analysis.json)。每次推进 v0.2 任务前，先运行 `npm run artifact:gap:check`，确认当前缺口、下一步实验和边界没有漂移。

## v0.2：公开 Artifact 对齐

目标：把当前轻量 replay 与 `learning-beyond-gradients` 的真实 artifact 拉近，但不牺牲课程可读性。

| 任务 | 输入 | 输出 | 验证门槛 |
| --- | --- | --- | --- |
| Ant 高保真验证 | `mujoco/ant/heuristic_ant.py` | 保留 `ant-gait-replay`，新增真实环境验证说明或可选脚本 | 轻量 replay 测试仍通过，真实验证独立可选 |
| Breakout RAM/vision 对齐 | `atari/breakout/heuristic_breakout.py` | 增加真实 artifact 边界说明、RAM/vision 字段表 | `missed_after_wall_reflection` probe 不变 |
| VizDoom OpenCV 对齐 | `vizdoom/heuristic_vizdoom_d1_cv.py` | 把 replay frame 映射到真实检测字段 | `wasted_pickup` 与 `valued_pickup` report 不漂移 |
| HalfCheetah 线索整理 | `mujoco/halfcheetah/*` | case card 或轻量 replay 设计文档 | 来源登记从“已定位”推进到“已结构化” |

## v0.3：X 与社区应用

目标：把 X 来源从二手摘要推进到可引用 case card。

| 任务 | 输入 | 输出 | 验证门槛 |
| --- | --- | --- | --- |
| Jiayi 原帖 thread 补全 | 公开 URL、一手原帖、公开文章 | 完整 X case card | 区分一手原帖、转述和推断 |
| 流体控制线索 | `@pg_dons` 被引用原帖 | `fluid-control` case card | 不写成已复现，除非有公开代码或 replay |
| 社区复现记录 | GitHub/论文/博客 | 来源登记条目 | 每条都有状态和落点 |

## v0.4：内部应用升级

目标：把私有来源脱敏应用问题从最小环境推进到真实 replay。

| 任务 | 当前示例 | 下一步 | 验证门槛 |
| --- | --- | --- | --- |
| 机器人足球 | `examples/robot-soccer/` | 接入真实视觉/运动约束的固定 replay | `blocked_shot` 保持为回归 probe |
| 交通模拟 | `examples/traffic-grid/` | 对接东湖交通仿真固定场景 | `spillback` 保持为回归 probe |
| 会议/私有来源资料回流 | 来源登记 | 把新线索转成 case card | 不泄露内部敏感内容，不写未验证事实 |

## v0.5：课程扩展

目标：从三讲两实验扩展成 4 到 5 讲课程，并把 capstone 项目纳入课程验收。

论文或技术报告写作使用 [论文蓝图](/zh-cn/appendix/paper-blueprint) 作为章节约束。新增研究里程碑如果改变研究问题、指标、实验或局限，应同步更新 `/paper-blueprint.json` 并运行 `npm run paper:blueprint:check`。

| 讲次 | 主题 | 必须配套 |
| --- | --- | --- |
| 第 4 讲 | 从 replay 到真实环境 | Ant、Breakout 或 VizDoom 的边界案例 |
| 第 5 讲 | 混合系统：感知模型 + HL | 视觉检测器或日志检测器案例 |
| Capstone | 从来源线索到可验证 HL 项目 | 来源登记、case card、runnable example、feedback report、test |

每新增一讲，必须同步：

- `docs/zh-cn/talk/`
- `docs/zh-cn/syllabus/`
- `docs/public/course-manifest.json`
- `scripts/check-course-structure.py`

## 进入下一版本的 Definition of Done

一个路线图任务完成前，必须同时满足：

1. 来源登记已更新。
2. 有案例页、示例代码、实验报告或讲义落点。
3. 如果声称“已复现”，必须有 runnable example、测试和符合 [实验协议](/zh-cn/appendix/benchmark-protocol) 的 baseline/probe/report。
4. `npm run verify` 通过。
5. `/course-manifest.json` 能反映新增内容。

路线图不是独立文档。它必须随着代码、报告和课程结构一起演进。
