---
title: Breakout 案例
description: 用 Atari Breakout 理解轨迹预测型 Heuristic Learning
---

# Breakout 案例

Breakout 是 `learning-beyond-gradients` 公开仓库中的 Atari artifact。课程先把其中最容易教学化的一部分抽成轻量 replay：根据球速预测侧墙反射后的落点，而不是追当前球的 x 坐标。

## 课程可运行版本

```bash
npm run examples:breakout-replay
npm run examples:breakout-replay:feedback
npm run examples:test
```

对应文件：

```text
examples/breakout-replay/
experiments/breakout-replay/latest.json
tests/test_breakout_replay.py
```

它改写自 [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) 中的 `atari/breakout/heuristic_breakout.py`。原始脚本的 RAM/vision policy 会解码球和挡板位置，估计速度，把球轨迹按侧墙反射到挡板高度，并移动挡板到预测截点。

## 案例拆解

| 问题 | 记录 |
| --- | --- |
| 环境 | Atari Breakout 的课程 replay |
| 状态 | 球位置、球速度、挡板位置、场地边界、挡板高度 |
| 动作 | `left`、`right`、`stay` |
| 反馈 | `missed_after_wall_reflection`、`intercepted`、step trace、JSON report |
| 更新对象 | `policies.py` 中的截点预测和挡板控制规则 |
| 验证 | `tests/test_breakout_replay.py` |

## HL 视角

baseline policy 只追当前球的 x 坐标。这个规则在球快要撞墙时会被误导：球当前在右侧，但反射后的落点在左侧。

heuristic policy 维护的是一个可审查的几何模型：

1. 根据当前球速估计到达挡板高度的步数。
2. 把未来 x 坐标按左右边界做弹性反射。
3. 让挡板提前移动到反射后的截点。
4. 用 replay 测试保证这条规则不会退化回“追当前球”。

这个案例说明 HL 不只是“if-else 规则”。它可以维护一个小型世界模型，并把失败轨迹转成可测试的几何约束。

## 与真实 artifact 的边界

课程 replay 不包含 Atari 环境、RGB 分割、RAM 解码、样本效率统计或视频渲染。它只保留一个核心教学点：side-wall reflection prediction。后续接回真实 artifact 时，应保留同一组 probe，确认轻量规则迁移后仍能解释真实回放。
