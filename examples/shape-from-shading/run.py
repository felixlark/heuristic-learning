from __future__ import annotations

import argparse
import json
from pathlib import Path

from model import ShadingObservation, infer_shape, render_svg


def build_probe() -> dict[str, object]:
    upright = ShadingObservation("top")
    rotated = upright.rotated_180()
    return {
        "model_boundary": "toy inference rule; not a human-vision simulator",
        "scenarios": [
            {
                "name": "upright_with_top_light_prior",
                "bright_edge": upright.bright_edge,
                "assumed_light": "top",
                "inferred_shape": infer_shape(upright, assumed_light="top"),
            },
            {
                "name": "rotated_with_same_prior",
                "bright_edge": rotated.bright_edge,
                "assumed_light": "top",
                "inferred_shape": infer_shape(rotated, assumed_light="top"),
            },
            {
                "name": "upright_with_bottom_light_cue",
                "bright_edge": upright.bright_edge,
                "assumed_light": "bottom",
                "inferred_shape": infer_shape(upright, assumed_light="bottom"),
            },
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg", type=Path, help="optionally write the visual probe as SVG")
    args = parser.parse_args()

    print(json.dumps(build_probe(), ensure_ascii=False, indent=2))
    if args.svg:
        args.svg.parent.mkdir(parents=True, exist_ok=True)
        args.svg.write_text(render_svg(), encoding="utf-8")


if __name__ == "__main__":
    main()
