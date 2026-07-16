from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


VerticalDirection = Literal["top", "bottom"]
Shape = Literal["convex", "concave"]


@dataclass(frozen=True)
class ShadingObservation:
    """A deliberately tiny observation: which edge of a disc is brighter."""

    bright_edge: VerticalDirection

    def rotated_180(self) -> "ShadingObservation":
        return ShadingObservation("bottom" if self.bright_edge == "top" else "top")


def infer_shape(
    observation: ShadingObservation,
    *,
    assumed_light: VerticalDirection = "top",
) -> Shape:
    """Apply a toy shape-from-shading heuristic, not a human-vision simulator.

    Under the simplified model, a convex bump is brightest toward the assumed
    light source. A concavity produces the opposite gradient.
    """

    if observation.bright_edge == assumed_light:
        return "convex"
    return "concave"


def render_svg() -> str:
    """Return a dependency-free visual probe with opposite vertical gradients."""

    return """<svg xmlns="http://www.w3.org/2000/svg" width="720" height="300" viewBox="0 0 720 300" role="img" aria-labelledby="title desc">
  <title id="title">Shape-from-shading ambiguity probe</title>
  <desc id="desc">Two discs have opposite vertical luminance gradients. Their apparent convexity depends on the assumed light direction.</desc>
  <defs>
    <linearGradient id="top-bright" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f8fafc"/>
      <stop offset="1" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="bottom-bright" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#334155"/>
      <stop offset="1" stop-color="#f8fafc"/>
    </linearGradient>
  </defs>
  <rect width="720" height="300" rx="24" fill="#0f172a"/>
  <circle cx="220" cy="130" r="92" fill="url(#top-bright)"/>
  <circle cx="500" cy="130" r="92" fill="url(#bottom-bright)"/>
  <g fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="18" text-anchor="middle">
    <text x="220" y="260">top bright</text>
    <text x="500" y="260">bottom bright</text>
  </g>
</svg>
"""
