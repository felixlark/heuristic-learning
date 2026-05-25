# Breakout Replay Experiment Records

This directory stores generated feedback reports for the lightweight Atari Breakout wall-reflection example.

Generate the latest report:

```bash
npm run examples:breakout-replay:feedback
```

The example is derived from `Trinkle23897/learning-beyond-gradients/atari/breakout/heuristic_breakout.py`. It keeps the core policy lesson dependency-free: estimate ball velocity, reflect the trajectory against side walls, and move the paddle toward the predicted intercept point.
