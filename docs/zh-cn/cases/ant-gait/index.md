---
title: Ant Gait 案例
description: 从 MuJoCo Ant heuristic artifact 抽取 CPG、stance duty 与 yaw feedback
---

# Ant Gait 案例

案例定位：

| 维度 | 内容 |
| --- | --- |
| 类型 | 公开 artifact 案例 |
| 对应示例 | `examples/ant-gait-replay/` |
| Failure mode | `yaw_drift` |
| 学习重点 | 连续控制中的可审计控制结构如何被维护 |

运行：

```bash
npm run examples:ant-gait-replay
npm run examples:ant-gait-replay:feedback
```

对应文件：

```text
examples/ant-gait-replay/
experiments/ant-gait-replay/latest.json
tests/test_ant_gait_replay.py
```

## 来源

本案例改写自 [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) 中的 `mujoco/ant/heuristic_ant.py`。原始 artifact 使用手写 rhythmic CPG、PD tracking、速度自适应、姿态/航向反馈，并可叠加短时域 MuJoCo rollout 搜索 residual action。

课程版暂不引入 MuJoCo，而是保留最可教学的策略对象：固定节律遇到持续 yaw 扰动会漂移；heuristic policy 同时调节 `phase_increment`、`stance_duty` 和 `yaw_feedback`，把 gait 维持在稳定前进区间。

## Probe

| 对象 | 内容 |
| --- | --- |
| baseline failure | `yaw_drift`：固定开环节律不能吸收持续偏航扰动 |
| heuristic patch | 用速度误差调节 cadence/stance duty，用 yaw/yaw-rate 反馈修正 gait |
| 可维护边界 | 先维护 gait controller 的可解释参数，再考虑 MPC residual |
| 验证 | `tests/test_ant_gait_replay.py` |

## 研究提示

这个案例适合放在 RL/DL 对照章节：它不是“无学习”，而是把学习对象从神经网络权重改成可审计的控制结构。后续如果接入真实 MuJoCo，需要保留同一份 replay report，让重型环境只作为更高保真验证，而不是替代最小 probe。
