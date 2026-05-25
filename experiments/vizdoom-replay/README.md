# VizDoom Replay Experiment Records

This directory stores generated feedback reports for the lightweight VizDoom D1 medikit-staging example.

Generate the latest report:

```bash
npm run examples:vizdoom-replay:feedback
```

The example is intentionally dependency-light. It mirrors the policy lesson from `Trinkle23897/learning-beyond-gradients/vizdoom/heuristic_vizdoom_d1_cv.py`: do not pick up the medikit while health is still too high for the reward to matter.
