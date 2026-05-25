# Changelog

All notable changes to the Heuristic Learning course repository are recorded here.

This repository is both a course site and a research artifact. Each release entry should describe the course surface, runnable examples, source traceability, and verification evidence.

## [0.1.0] - 2026-05-24

### Added

- VitePress Chinese course structure inspired by EasyVibe.
- Theory pages for HL concepts, RL/DL/HL comparison, the learning loop, and the research framework.
- Six runnable Python examples:
  - `examples/heuristic-gridworld/`
  - `examples/robot-soccer/`
  - `examples/vizdoom-replay/`
  - `examples/traffic-grid/`
  - `examples/breakout-replay/`
  - `examples/ant-gait-replay/`
- Feedback reports under `experiments/*/latest.json`.
- Unit tests covering all runnable examples.
- Code tour registry that maps each runnable example to reading order, edit target, commands, and tests.
- Source registry, case registry, experiment report schema, course manifest, and structure checker.
- Benchmark summary, ablation plan, X source registry, claims registry, teaching registry, speaker notes registry, exercise registry, contribution contract, reproducibility checklist, course pattern registry, case registry, concept graph, learning units registry, learning outcomes registry, checkpoint registry, evaluation metrics registry, paper blueprint registry, teaching pack registry, and research projects registry.
- Artifact gap analysis registry for tracking lightweight replay to source artifact fidelity gaps and next experiments.
- Troubleshooting tree registry for mapping verification failures to diagnostic commands, fix actions, and recheck commands.
- Source-to-case playbook registry for turning X threads, public artifacts, internal signals, and hypotheses into bounded case cards.
- Visual verification registry for official Browser/IAB and Chrome plugin release acceptance.
- Release readiness checker that stays separate from `npm run verify` and blocks release until official Browser/IAB evidence is marked passed.
- Lecture, lab, instructor guide, exercises, research projects, experiment protocol, citation, and license material.
- GitHub Actions verification and Pages deployment workflows.

### Verification

- Run `npm run verify` before publishing.
- Run `npm run release:readiness:check` after official Browser/IAB visual acceptance; it should fail while visual evidence is still `required-before-release`.
- Current verification gate covers linting, example tests, feedback report generation, report checks, code tour checks, benchmark summary checks, ablation plan checks, artifact gap checks, troubleshooting tree checks, source-to-case playbook checks, source, case, and X registry checks, claims checks, teaching registry checks, speaker notes checks, exercise checks, contribution contract checks, reproducibility checks, course pattern checks, concept graph checks, learning unit checks, learning outcome checks, checkpoint checks, evaluation metrics checks, paper blueprint checks, teaching pack checks, research project checks, visual verification matrix checks, course manifest checks, route checks, structure checks, and VitePress build.

### Source Boundary

- Jiayi Weng's `Learning Beyond Gradients` article and `learning-beyond-gradients` repository remain the highest-signal public sources.
- Lightweight replay examples are teaching reproductions, not full Atari, VizDoom, or MuJoCo reproductions.
- X/FieldTheory and Feishu-derived items must retain explicit source status in the source registry.
