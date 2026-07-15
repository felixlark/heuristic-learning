from __future__ import annotations

import argparse
from collections.abc import Callable

from env import Claim, ConstraintWorld, adversarial_claims, default_world
from policies import baseline_policy, constraint_audit_policy


Policy = Callable[[ConstraintWorld, Claim], str]


def run_audit(world: ConstraintWorld, policy: Policy) -> dict[str, object]:
    rows = []
    blocked_violations = 0
    accepted_violations = 0

    for claim in adversarial_claims():
        audit_result = world.audit(claim)
        decision = policy(world, claim)
        rows.append(
            {
                "claim": claim.__dict__,
                "audit_result": audit_result,
                "decision": decision,
            }
        )
        if audit_result == "constraint_violation":
            if decision == "block_and_request_revision":
                blocked_violations += 1
            elif decision == "accept":
                accepted_violations += 1

    if accepted_violations:
        reason = "accepted_constraint_violation"
    elif blocked_violations:
        reason = "blocked_constraint_violation"
    else:
        reason = "no_constraint_probe"

    return {
        "reason": reason,
        "reward": blocked_violations - accepted_violations,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "audit"], default="audit")
    args = parser.parse_args()

    policy = baseline_policy if args.policy == "baseline" else constraint_audit_policy
    result = run_audit(default_world(), policy)
    print(f"policy={args.policy}")
    print(f"reason={result['reason']}")
    print(f"reward={result['reward']}")
    for row in result["rows"]:
        print(f"{row['audit_result']} -> {row['decision']} :: {row['claim']}")


if __name__ == "__main__":
    main()
