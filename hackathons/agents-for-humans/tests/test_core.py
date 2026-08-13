from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from kvassistent_steward.core import (
    checkpoint_delay_hours,
    next_checkpoint_iso,
    normalized_batch_state,
    safety_gate,
)
from kvassistent_steward.store import load_batch, save_batch


class SafetyGateTests(unittest.TestCase):
    def test_mold_stops_without_model_override(self):
        decision = safety_gate(mold_reported=True)
        self.assertEqual("stop", decision.status)
        self.assertIn("mold", decision.reason.lower())

    def test_slime_stops(self):
        self.assertEqual("stop", safety_gate(slime_reported=True).status)

    def test_reported_acetone_smell_stops(self):
        decision = safety_gate(smell_report="a little like acetone")
        self.assertEqual("stop", decision.status)

    def test_overheat_stops_and_cools(self):
        decision = safety_gate(liquid_temp_c=35.0)
        self.assertEqual("stop_and_cool", decision.status)

    def test_unknown_observations_do_not_become_fake_facts(self):
        decision = safety_gate(smell_report="unknown", liquid_temp_c=None)
        self.assertEqual("continue", decision.status)
        self.assertIn("supplied", decision.reason.lower())


class CheckpointTests(unittest.TestCase):
    def test_hot_primary_fermentation_is_checked_earlier(self):
        self.assertEqual(4, checkpoint_delay_hours("primary_fermentation", 28.0))
        self.assertEqual(8, checkpoint_delay_hours("primary_fermentation", 22.0))

    def test_checkpoint_is_deterministic_for_given_time(self):
        start = datetime(2026, 8, 13, 10, 0, tzinfo=timezone.utc)
        self.assertEqual(
            "2026-08-13T14:00:00+00:00",
            next_checkpoint_iso(stage="primary_fermentation", liquid_temp_c=28.0, now=start),
        )


class PersistenceTests(unittest.TestCase):
    def test_saved_batch_can_be_loaded_after_store_is_reopened(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            batch = normalized_batch_state(
                batch_id="demo-1",
                stage="primary_fermentation",
                liquid_temp_c=28.0,
                observation="normal surface reported by human",
                now=datetime(2026, 8, 13, 10, 0, tzinfo=timezone.utc),
            )
            save_batch(batch, path=path)

            reloaded = load_batch("demo-1", path=path)

            self.assertEqual(batch, reloaded)
            self.assertEqual("demo-1", reloaded["batch_id"])
            self.assertEqual("2026-08-13T14:00:00+00:00", reloaded["next_checkpoint_at"])


if __name__ == "__main__":
    unittest.main()
