# Ant Gait Replay Experiment

Generate the latest report with:

```bash
npm run examples:ant-gait-replay:feedback
```

The example is derived from `Trinkle23897/learning-beyond-gradients/mujoco/ant/heuristic_ant.py`. It keeps the course-level policy lesson dependency-free: a fixed CPG rhythm drifts under yaw perturbation, while a speed-adaptive gait with stance-duty and yaw feedback stays stable.
