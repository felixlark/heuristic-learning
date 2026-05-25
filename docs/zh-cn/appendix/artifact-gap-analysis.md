---
title: Artifact 差距分析
description: Heuristic Learning 轻量 replay 与公开/内部来源 artifact 的保真度差距、下一步实验和验证命令
---

# Artifact 差距分析

本页把“当前示例已经跑通”和“真实 artifact 已经复现”分开。它回答一个研究仓库必须面对的问题：每个轻量 replay 到 Jiayi 公开 artifact、脱敏应用问题或教学环境之间还差哪些保真度，下一步应该先补哪个实验。

机器可读矩阵见 [`/artifact-gap-analysis.json`](/artifact-gap-analysis.json)，字段约束见 [`/artifact-gap-analysis.schema.json`](/artifact-gap-analysis.schema.json)。`npm run artifact:gap:check` 会检查本页、示例 registry、来源登记、benchmark、消融计划和研究路线图是否一致。

## 差距矩阵

| Artifact | 当前 replay | 缺失保真度 | 下一步实验 | 验证命令 |
| --- | --- | --- | --- | --- |
| Ant Gait artifact gap | `examples/ant-gait-replay` 把 `yaw_drift` 压缩成 CPG、stance duty 与 yaw feedback | MuJoCo contact dynamics、完整 actuator vector、扰动 sweep | 可选高保真 Ant runner，复用 `yaw_drift` probe | `npm run examples:ant-gait-replay:feedback`、`npm run examples:test` |
| Breakout artifact gap | `examples/breakout-replay` 把 `missed_after_wall_reflection` 压缩成侧墙反射截点 | Atari emulator、RAM/pixel extraction、碰撞与得分动态 | RAM/vision 字段映射表，再接 emulator | `npm run examples:breakout-replay:feedback`、`npm run examples:reports:check` |
| VizDoom artifact gap | `examples/vizdoom-replay` 把 `wasted_pickup`/`valued_pickup` 压缩成 health、area、offset 字段 | VizDoom loop、OpenCV detection、frame timing | detector 输出字段映射和固定帧阈值消融 | `npm run examples:vizdoom-replay:feedback`、`npm run examples:reports:check` |
| Robot Soccer internal gap | `examples/robot-soccer` 把 `blocked_shot` 压缩成 grid lane check | 视觉不确定性、运动约束、对手策略变化 | 脱敏固定 replay，保留 `blocked_shot` 回归 probe | `npm run examples:robot-soccer:feedback`、`npm run cases:check` |
| Traffic Grid internal gap | `examples/traffic-grid` 把 `spillback` 压缩成 downstream capacity 约束 | 真实路网、相位时序、需求分布 | 脱敏固定交通场景，测试下游容量不变量 | `npm run examples:traffic-grid:feedback`、`npm run cases:check` |
| GridWorld teaching gap | `examples/heuristic-gridworld` 把 `local_greedy_trap` 压缩成最小教学环境 | 外部 benchmark、随机转移、地图泛化 | 生成地图测试，避免把启发式规则藏成 planner | `npm run examples:gridworld:feedback`、`npm run examples:test` |

## 使用方式

1. 先运行对应示例的 feedback 命令，确认当前 failure probe 没有漂移。
2. 查 `/artifact-gap-analysis.json` 的 `missing_fidelity`，只选择一个保真度维度推进。
3. 如果新增高保真 runner，保留当前轻量 replay 作为教学和回归测试入口。
4. 如果来源来自私有来源或其他内部系统，只能发布脱敏后的失败模式、字段和不变量。
5. 如果结果要进入论文或技术报告，同步更新 [论文蓝图](/zh-cn/appendix/paper-blueprint) 和 [研究路线图](/zh-cn/appendix/research-roadmap)。

## 边界

本页不能把轻量 replay 提升成真实环境复现。它的作用是让读者、研究者和维护者清楚知道：现在已经能教学和回归测试什么，后续要验证真实系统时必须补哪些环境、传感、动力学或数据采集层。

```bash
npm run artifact:gap:check
npm run ablation:plan:check
npm run examples:reports:check
npm run cases:check
npm run verify
```
