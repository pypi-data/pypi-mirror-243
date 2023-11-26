"""Tests if  ``_critical_value`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test__critical_value.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random

### FUNCTION IMPORT ###
from normtest.filliben import _critical_value

os.system("cls")


class Test__critical_value(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = random.randrange(4, 50)
        cls.alpha = 0.05

    def test_outputs(self):
        result = _critical_value(self.n, self.alpha)
        self.assertIsInstance(
            result, float, msg=f"not a float when alpha={self.alpha} and n={self.n}"
        )

    def test_pass(self):
        sample_sizes = [50, 11, 25, 35, 12, 25, 5, 33, 16, 4, 65, 22, 15]
        alphas = [
            0.005,
            0.01,
            0.025,
            0.05,
            0.1,
            0.25,
            0.5,
            0.75,
            0.9,
            0.95,
            0.975,
            0.99,
            0.995,
        ]
        expecteds = [
            0.959,
            0.883,
            0.950,
            0.968,
            0.941,
            0.976,
            0.960,
            0.991,
            0.989,
            0.996,
            0.997,
            0.995,
            0.995,
        ]
        for sample_size, alpha, expected in zip(sample_sizes, alphas, expecteds):
            result = _critical_value(sample_size, alpha)
            self.assertAlmostEqual(
                result,
                expected,
                places=3,
                msg=f"wrong critical for Filliben test",
            )


if __name__ == "__main__":
    unittest.main()
