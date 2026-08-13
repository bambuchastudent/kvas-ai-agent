from datetime import datetime, timezone
import unittest

from kvassistent_steward.core import checkpoint_delay_hours, next_checkpoint_iso, safety_gate


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


if __name__ == "__main__":
    unittest.main()
