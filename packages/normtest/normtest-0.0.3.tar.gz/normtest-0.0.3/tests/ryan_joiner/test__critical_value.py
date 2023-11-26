"""Tests if  ``_critical_value`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test__critical_value.py
    or
    python -m unittest -b tests/ryan_joiner/test__critical_value.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random

### FUNCTION IMPORT ###
from normtest.ryan_joiner import _critical_value

os.system("cls")


class Test__critical_value(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = random.randrange(4, 200)
        cls.alpha = 0.05

    def test_outputs(self):
        result = _critical_value(self.n, self.alpha)
        self.assertIsInstance(
            result, float, msg=f"not a float when alpha={self.alpha} and n={self.n}"
        )

    def test_statext(self):
        # https://www.statext.com/practice/NormalityTest03.php
        # critical_0_01 = 0.8880
        # critical_0_05 = 0.9230
        # critical_0_10 = 0.9387
        x_data = np.array([148, 154, 158, 160, 161, 162, 166, 170, 182, 195, 236])
        result = _critical_value(x_data.size, 0.01)
        self.assertAlmostEqual(
            result,
            0.8880,
            places=3,
            msg=f"wrong critical for RJ test for statext dataset",
        )
        result = _critical_value(x_data.size, 0.05)
        self.assertAlmostEqual(
            result,
            0.9230,
            places=3,
            msg=f"wrong critical for RJ test for statext dataset",
        )
        result = _critical_value(x_data.size, 0.10)
        self.assertAlmostEqual(
            result,
            0.9387,
            places=3,
            msg=f"wrong critical for RJ test for statext dataset",
        )


if __name__ == "__main__":
    unittest.main()
