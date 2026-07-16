# Shape-from-Shading Research Probe

This zero-dependency probe turns an ambiguous shading pattern into an explicit,
testable heuristic. It is a teaching model, not a simulator of human vision.

## Learning target

- Observation: which vertical edge of a disc is brighter.
- Heuristic: infer convexity using an assumed light direction.
- Probe: rotate the observation or change the scene-light cue.
- Boundary: real shape perception also uses contours, reflectance, cast shadows,
  binocular disparity, scene context, and experience.

## Run

```bash
npm run examples:shape-from-shading
```

To write the two-disc visual stimulus:

```bash
python3 examples/shape-from-shading/run.py --svg /tmp/shape-from-shading.svg
```

## Test

```bash
python3 -m unittest tests/test_shape_from_shading.py
```

Focused test path: `tests/test_shape_from_shading.py`.

## Course link

- `docs/zh-cn/cases/visual-prior/index.md`
