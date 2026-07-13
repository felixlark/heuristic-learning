import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "examples/cartpole-benchmark" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


policy = load("cartpole_policy", "policy.py")
runner = load("cartpole_runner", "run.py")


class CartPoleBenchmarkTest(unittest.TestCase):
    def test_seed_splits_do_not_overlap(self):
        splits = [set(runner.seeds_for(name)) for name in ("dev", "holdout", "audit")]
        self.assertFalse(splits[0] & splits[1])
        self.assertFalse(splits[0] & splits[2])
        self.assertFalse(splits[1] & splits[2])

    def test_policy_is_transparent_and_deterministic(self):
        observation = (0.0, 0.1, 0.02, -0.03)
        self.assertIn(policy.baseline(observation), (0, 1))
        self.assertEqual(policy.improved(observation), policy.improved(observation))

    def test_ledger_is_append_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trials.jsonl"
            runner.append_record(path, {"trial": 1})
            runner.append_record(path, {"trial": 2})
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(rows, [{"trial": 1}, {"trial": 2}])


if __name__ == "__main__":
    unittest.main()
