# Deployment

## Local Preview

```bash
npm install
npm run dev
npm run build
npm run preview
```

The default GitHub Pages base is `/heuristic-learning/`. Override it when needed:

```bash
BASE=/ npm run build
SITE_URL=https://example.com BASE=/ npm run build
```

## Verification Before Publishing

```bash
npm run verify
```

`npm run verify` is the publishing preflight gate. It lints the VitePress theme, runs all Python example tests, regenerates feedback reports, checks report schemas, checks the code tour, checks the benchmark summary, checks the ablation plan, checks the artifact gap analysis, checks the troubleshooting tree, checks the source-to-case playbook, checks source, case, and X registries, checks claims, teaching materials, slide deck structure, speaker notes, rubric, exercise registry, contribution contract, reproducibility checklist, course patterns, concept graph, learning units, learning outcomes, checkpoints, evaluation metrics, paper blueprint, teaching packs, research projects, visual verification matrix, completion audit, the course manifest, course structure, route reachability, and builds the VitePress site.

`npm run release:readiness:check` is the final release readiness gate. It should fail while official Browser/IAB evidence is still `required-before-release` or `/visual-acceptance-log.json` contains `not-run` / `blocked` entries, and pass only after the visual acceptance matrix has real browser evidence.

Do not publish from a local HTTP check or a successful build alone. The runnable examples, reports, benchmark summary, ablation plan, troubleshooting tree, source-to-case playbook, source registry, case registry, X source registry, learning outcomes, checkpoints, evaluation metrics, paper blueprint, manifest, structure checker, and docs build must pass together.

After local checks pass, use the official Codex Browser plugin / in-app browser or official Chrome plugin to run the public-page acceptance matrix in `docs/zh-cn/appendix/visual-verification.md`. Do not substitute Playwright, Chrome for Testing, or plain HTTP checks for that final visual route.

Release bookkeeping lives in `CHANGELOG.md` and `docs/zh-cn/appendix/release-checklist.md`.
