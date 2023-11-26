"""Tests if  ``_p_value`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test__p_value.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import random

### FUNCTION IMPORT ###
from normtest.ryan_joiner import _p_value

os.system("cls")


class Test__p_value(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = random.randrange(4, 200)
        cls.statistic = random.uniform(0.001, 0.999)

    def test_outputs(self):
        result = _p_value(self.statistic, self.n)
        self.assertIsInstance(
            result,
            (float, str),
            msg=f"not a float when statistic={self.statistic} and n={self.n}",
        )

        result = _p_value(statistic=self.statistic, sample_size=self.n)
        self.assertIsInstance(
            result,
            (float, str),
            msg=f"not a float when statistic={self.statistic} and n={self.n}",
        )

    def test__p_values_minitab(self):
        # dataset 1
        result = _p_value(0.878, 5)
        self.assertAlmostEqual(result, 0.048, places=2, msg=f"wrong p-value")
        # dataset 2
        result = _p_value(0.946, 15)
        self.assertAlmostEqual(result, 0.083, places=2, msg=f"wrong p-value")
        # dataset 3
        result = _p_value(0.931, 11)
        self.assertAlmostEqual(result, 0.076, places=2, msg=f"wrong p-value")
        # dataset 4
        result = _p_value(0.881, 7)
        self.assertAlmostEqual(result, 0.036, places=2, msg=f"wrong p-value")
        # dataset 5
        result = _p_value(0.903, 7)
        self.assertAlmostEqual(result, 0.062, places=2, msg=f"wrong p-value")
        # dataset 6
        result = _p_value(0.929, 11)
        self.assertAlmostEqual(result, 0.068, places=2, msg=f"wrong p-value")
        # dataset 7
        result = _p_value(0.878, 7)
        self.assertAlmostEqual(result, 0.033, places=2, msg=f"wrong p-value")
        # dataset 8
        result = _p_value(0.887, 8)
        self.assertAlmostEqual(result, 0.033, places=2, msg=f"wrong p-value")
        # dataset 9
        result = _p_value(0.908, 6)
        self.assertAlmostEqual(result, 0.091, places=2, msg=f"wrong p-value")
        # dataset 10
        result = _p_value(0.917, 10)
        self.assertAlmostEqual(result, 0.049, places=2, msg=f"wrong p-value")
        # dataset 11
        result = _p_value(0.928, 12)
        self.assertAlmostEqual(result, 0.053, places=2, msg=f"wrong p-value")
        # dataset 12
        result = _p_value(0.937, 16)
        self.assertAlmostEqual(result, 0.043, places=2, msg=f"wrong p-value")
        # dataset 13
        result = _p_value(0.978, 16)
        self.assertEqual(result, "p > 0.100", msg=f"wrong p-value")
        # dataset 14
        result = _p_value(0.867, 16)
        self.assertEqual(result, "p < 0.010", msg=f"wrong p-value")
        # dataset 15
        result = _p_value(0.913, 9)
        self.assertAlmostEqual(result, 0.052, places=2, msg=f"wrong p-value")
        # dataset 16
        result = _p_value(0.903, 8)
        self.assertAlmostEqual(result, 0.048, places=2, msg=f"wrong p-value")
        # dataset 17
        result = _p_value(0.91, 9)
        self.assertAlmostEqual(result, 0.048, places=2, msg=f"wrong p-value")


if __name__ == "__main__":
    unittest.main()
