---
title: VizDoom 案例
description: 用 VizDoom 理解回放驱动的 Heuristic Learning
---

# VizDoom 案例

VizDoom 是 `learning-beyond-gradients` 公开仓库中的重要 artifact。它适合用来解释 HL 中的回放反馈：系统不只是拿到一个分数，还能通过视频或轨迹看到失败发生在哪里。

## 课程可运行版本

课程先实现一个轻量 replay 版：

```bash
npm run examples:vizdoom-replay
npm run examples:vizdoom-replay:feedback
npm run examples:test
```

对应文件：

```text
examples/vizdoom-replay/
experiments/vizdoom-replay/latest.json
tests/test_vizdoom_replay.py
```

它改写自 [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) 中的 `vizdoom/heuristic_vizdoom_d1_cv.py`。原始脚本的 D1 规则是：通过视觉检测 medikit，血量高时靠近并等待，血量降到阈值后再拾取，让 medikit 的 reward 真正有价值。

## 案例拆解

| 问题 | 记录 |
| --- | --- |
| 环境 | VizDoom D1 Basic 的课程 replay |
| 状态 | 血量、medikit 是否可见、medikit 面积、medikit 相对偏移 |
| 动作 | `wait`、`forward`、`turn_left`、`turn_right` |
| 反馈 | `wasted_pickup`、`valued_pickup`、step trace、JSON report |
| 更新对象 | `vizdoom_policies.py` 中的阈值和动作优先级，外加 replay 回归测试 |

## HL 视角

Deep RL 通常把轨迹转成梯度更新。HL 则把失败轨迹转成代码维护任务：

1. 识别失败模式：血量还高时立刻吃掉 medikit，导致奖励价值被浪费。
2. 编码智能体读取 replay trace 与 `latest.json`。
3. 修改状态检测、阈值或动作优先级。
4. 重新运行命令和测试。
5. 把新失败模式写回实验记录。

## 从课程版走向真实环境

公开仓库中的原始脚本仍然是后续对齐目标。课程版保留两个层次：

- `artifact`：记录原始来源、阈值和策略意图。
- `course`：改写成不依赖 EnvPool/OpenCV 的最小实验，让学生先理解 HL 更新对象。

下一步可以把 replay frame 替换为真实截图检测结果，同时保留同一组 test/probe，验证从轻量 replay 到真实环境时规则没有漂移。
