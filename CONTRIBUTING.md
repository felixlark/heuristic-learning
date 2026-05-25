# Contributing to Heuristic Learning

This repository treats every contribution as course material. A good change must be traceable, runnable, and verifiable.

Machine-readable contribution rules live in `docs/public/contribution-contract.json`; its schema is `docs/public/contribution-contract.schema.json`. Run `npm run contribution:contract:check` after changing contribution paths, PR evidence, forbidden materials, or verification commands.

## Contribution Paths

| Path | Required Evidence |
| --- | --- |
| Theory page | source link, research question, case/example link, source-registry status |
| Case card | `templates/case-card.md`, source status, feedback surface, verification plan |
| Runnable example | `examples/*/README.md`, run script, feedback script, report, test |
| Experiment record | `templates/experiment-record.md`, run command, source status, result summary, feedback, candidate update |
| Claim review | `templates/claim-review.md`, evidence pages, falsification path, verification command |
| Reproduction note | `templates/reproduction-note.md`, source status, reproduction scope, missing fidelity, next experiment |
| Anti-forgetting review | `templates/anti-forgetting-checklist.md`, old behavior, risky update, regression guard |
| Lab or lecture | concrete question, runnable command, review task, course link |

## Opening an Issue

Use the GitHub issue templates before opening a PR:

- `Source signal` for public, X/FieldTheory, or internal clues that need source status.
- `Reproduction note` for bounded reproduction scope, missing fidelity, falsification path, and next experiment.
- `Runnable example` for new examples with baseline failure, heuristic patch, report, and tests.
- `Course material` for theory pages, cases, lectures, labs, exercises, or appendix updates.
- `Experiment record` for run results, feedback interpretation, and next candidate updates.
- `Claim review` for promoting, downgrading, or falsifying a research claim.
- `Anti-forgetting review` for checking that a heuristic patch preserves old probes and behavior.

Issues should preserve the same evidence discipline as PRs: source, failure mode or core question, course target, and verification commands.

Use `templates/experiment-record.md` when a change mainly records a run result, report interpretation, or next candidate update rather than adding a new runnable example.

## Before Opening a PR

Run:

```bash
npm install
npm run verify
```

For a new runnable example, also confirm:

```bash
npm run course:structure:check
npm run source:registry:check
npm run cases:check
npm run x:sources:check
npm run source:case:check
npm run claims:registry:check
npm run slides:check
npm run speaker:notes:check
npm run course:manifest:check
npm run rubric:check
npm run examples:reports:check
npm run examples:registry:check
npm run code:tour:check
npm run benchmark:summary:check
npm run ablation:plan:check
npm run artifact:gap:check
npm run research:logbook:check
npm run source:case:check
npm run teaching:registry:check
npm run exercises:check
npm run contribution:contract:check
npm run troubleshooting:tree:check
npm run patterns:check
npm run learning:units:check
npm run learning:outcomes:check
npm run checkpoints:check
npm run metrics:check
npm run paper:blueprint:check
npm run teaching:pack:check
npm run completion:audit:check
npm run docs:routes:check
```

For public release readiness, run `npm run release:readiness:check` after `npm run verify` and official Browser/IAB visual acceptance. This command is expected to fail while visual checks remain `required-before-release`.

## Source Discipline

- Public claims must link to a public source or be marked as a research hypothesis.
- X/Twitter or Feishu-derived material must stay in `to_collect`, `located`, or `structured` status until the repository contains a reproducible probe or artifact.
- Do not describe an unverified source as reproduced.
- Do not paste secrets, Feishu/Lark raw content, X cookies/API credentials, or private logs into issues, PRs, docs, examples, or reports. See `SECURITY.md`.

## Reproduction Note Checklist

Use `templates/reproduction-note.md` before upgrading a source signal into a case, example, research log entry, or artifact-gap claim.

1. Record the source status without overclaiming uncached X/FieldTheory or private signals.
2. Separate current lightweight replay from missing fidelity.
3. State the falsification path and next experiment.
4. Link the case page, example path, report path, test path, and registry paths when they exist.
5. Run `npm run source:registry:check`, `npm run artifact:gap:check`, `npm run research:logbook:check`, and `npm run source:case:check`.

## New Runnable Example Checklist

1. Add `examples/<name>/run.py`.
2. Add `examples/<name>/feedback_loop.py`.
3. Add `examples/<name>/README.md` with run command, feedback command, report path, test path, and failure mode.
4. Add `tests/test_<name>.py`.
5. Add `experiments/<name>/latest.json` through the feedback script.
6. Add package scripts in `package.json`.
7. Add the example to `docs/zh-cn/syllabus/index.md`, `docs/zh-cn/examples/index.md`, and `docs/public/course-manifest.json`.
8. Add it to `docs/public/example-registry.json`.
9. Add it to `scripts/check-course-structure.py`.
10. Run `npm run source:registry:check`.
11. Run `npm run course:manifest:check`.
12. Run `npm run examples:registry:check`.
13. Run `npm run verify`.

## Quality Bar

Use `docs/zh-cn/appendix/rubric.md` as the acceptance standard. A contribution should explain:

- the baseline failure,
- the heuristic update target,
- the feedback report,
- the regression test,
- the remaining risk.

More detailed rules live in `docs/zh-cn/appendix/contribution-protocol.md`.
