import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "shape-from-shading"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("model", "run"):
    sys.modules.pop(module_name, None)

from model import ShadingObservation, infer_shape, render_svg
from run import build_probe


class ShapeFromShadingTests(unittest.TestCase):
    def test_rotation_flips_interpretation_under_same_prior(self):
        upright = ShadingObservation("top")
        self.assertEqual(infer_shape(upright, assumed_light="top"), "convex")
        self.assertEqual(infer_shape(upright.rotated_180(), assumed_light="top"), "concave")

    def test_scene_light_cue_can_flip_interpretation(self):
        observation = ShadingObservation("top")
        self.assertEqual(infer_shape(observation, assumed_light="top"), "convex")
        self.assertEqual(infer_shape(observation, assumed_light="bottom"), "concave")

    def test_probe_keeps_model_boundary_explicit(self):
        probe = build_probe()
        self.assertIn("not a human-vision simulator", probe["model_boundary"])
        self.assertEqual(len(probe["scenarios"]), 3)

    def test_svg_contains_opposite_gradients_and_accessible_text(self):
        svg = render_svg()
        self.assertIn('id="top-bright"', svg)
        self.assertIn('id="bottom-bright"', svg)
        self.assertIn("Shape-from-shading ambiguity probe", svg)


if __name__ == "__main__":
    unittest.main()
