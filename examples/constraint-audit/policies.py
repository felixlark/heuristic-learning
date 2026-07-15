from __future__ import annotations

from env import Claim, ConstraintWorld


def baseline_policy(world: ConstraintWorld, claim: Claim) -> str:
    """Accepts fluent claims without comparing them to a constraint source."""
    del world, claim
    return "accept"


def constraint_audit_policy(world: ConstraintWorld, claim: Claim) -> str:
    """Returns an audit state; it never upgrades unknown claims to facts."""
    result = world.audit(claim)
    if result == "supported_by_catalog":
        return "accept"
    if result == "constraint_violation":
        return "block_and_request_revision"
    return "request_external_evidence"
