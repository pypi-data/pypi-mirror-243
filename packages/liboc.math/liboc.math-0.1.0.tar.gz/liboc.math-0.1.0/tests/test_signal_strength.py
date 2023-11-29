from unittest import TestCase as BaseTestCase

from liboc.math import signal_strength


class TestCase(BaseTestCase):
    def test_db_to_percentage(self):
        KNOWN_VALS = (
            (-100, 0),
            (-97, 0),
            (-95, 0),
            (-94, 3),
            (-93, 5),
            (-77, 40),
            (-65, 60),
            (-45, 86),
            (-27, 98),
            (-26, 99),
            (-25, 99),
            (-24, 99),
            (-23, 100),
            (-19, 100),
            (-1, 100),
        )
        for db, pct in KNOWN_VALS:
            assert (
                signal_strength.db_to_percent(db) == pct
            ), f"rssi {db} did not calculate to expected percent of {pct}%."
