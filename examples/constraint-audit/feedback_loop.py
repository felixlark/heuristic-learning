from __future__ import annotations

import argparse
import json
from pathlib import Path

from env import default_world
from policies import baseline_policy, constraint_audit_policy
from run import run_audit


def summarize(name: str) -> dict[str, object]:
    policy = baseline_policy if name == "baseline" else constraint_audit_policy
    result = run_audit(default_world(), policy)
    return {"policy": name, **result}


def build_feedback_report() -> dict[str, object]:
    return {
        "case": "closed_world_constraint_audit",
        "source": {
            "kind": "research_hypothesis",
            "note": "A bounded fixture for studying independent constraint checks; it is not a general hallucination detector.",
        },
        "policies": [summarize("baseline"), summarize("heuristic")],
        "feedback": [
            "A baseline that accepts every claim passes known constraint violations through unchanged.",
            "The audit policy blocks contradictions with the supplied catalog and routes unknown claims to external evidence.",
            "This fixture does not establish factuality outside its closed catalog or show that self-play reaches a Nash equilibrium.",
        ],
        "candidate_update": {
            "target": "examples/constraint-audit/policies.py",
            "rule": "Keep supplied constraints, unknown-claim escalation, and contradiction blocking separate.",
            "verification": "python3 -m unittest discover -s tests",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    payload = json.dumps(build_feedback_report(), ensure_ascii=False, indent=2)
    print(payload)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
