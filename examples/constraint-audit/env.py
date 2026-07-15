from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    subject: str
    relation: str
    value: str


@dataclass(frozen=True)
class ConstraintWorld:
    """A closed-world audit fixture, not a real-world fact checker."""

    catalog: dict[tuple[str, str], str]

    def audit(self, claim: Claim) -> str:
        expected = self.catalog.get((claim.subject, claim.relation))
        if expected is None:
            return "needs_external_evidence"
        if expected != claim.value:
            return "constraint_violation"
        return "supported_by_catalog"


def default_world() -> ConstraintWorld:
    return ConstraintWorld(
        catalog={
            ("Halley_comet", "next_perihelion"): "2061",
            ("water_at_standard_pressure", "freezing_point_celsius"): "0",
            ("Earth", "natural_moon_count"): "1",
        }
    )


def adversarial_claims() -> tuple[Claim, ...]:
    return (
        Claim("Halley_comet", "next_perihelion", "2024"),
        Claim("water_at_standard_pressure", "freezing_point_celsius", "100"),
        Claim("Earth", "natural_moon_count", "1"),
        Claim("unlisted_object", "launch_year", "2027"),
    )
