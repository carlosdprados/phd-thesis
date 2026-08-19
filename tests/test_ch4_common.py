import sys
import unittest
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from ch4_common import (  # noqa: E402
    average_ranks,
    curation_for,
    holm_adjust,
    is_true_flag,
    row_is_excluded,
    spearman,
)


class Chapter4ScreeningTests(unittest.TestCase):
    def test_database_boolean_encodings(self):
        for value in ("Y", "y", "yes", "TRUE", "1", "t"):
            self.assertTrue(is_true_flag(value))
        for value in ("N", "false", "0", "", None):
            self.assertFalse(is_true_flag(value))

    def test_broken_y_row_is_excluded(self):
        row = {
            "device_name": "NM_v001",
            "day": "2",
            "pixel": "L1",
            "is broken": "Y",
        }
        self.assertTrue(
            row_is_excluded(
                row,
                "HYST",
                flags=set(),
                curation={},
                broken_fields=("is broken",),
            )
        )

    def test_curation_uses_full_key_and_fallback(self):
        registry = {
            ("NM_v001", "DELAYTIME", "", ""): ("use", None),
            ("NM_v001", "DELAYTIME", "4", ""): ("discard", None),
            ("NM_v001", "DELAYTIME", "4", "R2"): (
                "clean",
                frozenset({1.0, 2.0}),
            ),
        }
        self.assertEqual(
            curation_for(registry, "NM_v001", "DELAYTIME", "4", "R2")[0],
            "clean",
        )
        self.assertEqual(
            curation_for(registry, "NM_v001", "DELAYTIME", "4", "L1")[0],
            "discard",
        )
        self.assertEqual(
            curation_for(registry, "NM_v001", "DELAYTIME", "5", "L1")[0],
            "use",
        )


class Chapter4StatisticsTests(unittest.TestCase):
    def test_average_ranks_preserve_ties(self):
        np.testing.assert_allclose(
            average_ranks([0.3, 0.3, 0.6, 1.2, 1.2]),
            [1.5, 1.5, 3.0, 4.5, 4.5],
        )

    def test_spearman_is_tie_aware(self):
        x = [0.3, 0.3, 0.6, 1.2, 1.2]
        y = [5.0, 4.0, 3.0, 2.0, 1.0]
        expected = np.corrcoef(
            [1.5, 1.5, 3.0, 4.5, 4.5],
            [5.0, 4.0, 3.0, 2.0, 1.0],
        )[0, 1]
        self.assertAlmostEqual(spearman(x, y), expected)

    def test_holm_adjustment_is_monotone_in_sorted_order(self):
        adjusted = holm_adjust([0.01, 0.04, 0.03, np.nan])
        np.testing.assert_allclose(adjusted[:3], [0.03, 0.06, 0.06])
        self.assertTrue(np.isnan(adjusted[3]))


if __name__ == "__main__":
    unittest.main()
