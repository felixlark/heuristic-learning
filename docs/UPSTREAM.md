# Upstream comparison and maintenance notes

Primary upstream: <https://github.com/Trinkle23897/learning-beyond-gradients>

## Division of responsibility

- Upstream is the primary research artifact and the source of the five-environment benchmark.
- This repository is the Chinese Web course, talk surface, beginner laboratory, and bounded reproduction entrypoint.
- Public course pages explain concepts and evidence. Maintenance decisions stay in this file.

## Content adopted as course principles

- Fixed development, holdout, and audit seed splits.
- Append-only trial records, including failures and partial runs.
- Separate structural edits, scalar tuning, teacher distillation, and RL baselines.
- Report cost, provenance, caveats, and negative results alongside scores.

## Content not copied

The upstream repository did not declare a license when reviewed on 2026-07-13. Its code and large generated ledgers are therefore not vendored here. This repository links to upstream evidence and implements original, small teaching experiments.

## Refresh procedure

1. Pull the sibling checkout at `/Users/longbiao/Projects/learning-beyond-gradients`.
2. Review changes under `heuristic_learning/`, especially its README, result reports, environment registry, and tests.
3. Update learner-facing claims only when an upstream report or runnable artifact supports them.
4. Run `npm run verify`, deploy Pages, and verify the live course before publishing the comparison.
