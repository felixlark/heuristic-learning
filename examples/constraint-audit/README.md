# Constraint Audit Research Fixture

This closed-world fixture turns a research hypothesis into a small, falsifiable probe. A baseline accepts every claim. The audit policy checks a supplied constraint catalog, blocks a known contradiction, and requests external evidence for claims absent from that catalog.

It is **not** a general fact checker, a demonstration of Nash-equilibrium convergence, or evidence that an LLM has stopped hallucinating.

## Learning Target

- Failure mode: `accepted_constraint_violation`
- Baseline: accept every fluent claim.
- Heuristic patch: distinguish catalog contradiction from an unknown claim.
- Update target: `examples/constraint-audit/policies.py`

## Run

```bash
npm run examples:constraint-audit
```

## Feedback Report

```bash
npm run examples:constraint-audit:feedback
```

Report path:

```text
experiments/constraint-audit/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_constraint_audit.py
```

## Course Links

- Research note: `docs/zh-cn/appendix/constraint-audit.md`
- Research framework: `docs/zh-cn/theory/research-framework.md`
