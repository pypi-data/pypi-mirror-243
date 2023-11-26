"""Tests if  ``_order_statistic`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/looney_gulledge/test__order_statistic.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random

### FUNCTION IMPORT ###
from normtest.looney_gulledge import _order_statistic

os.system("cls")


class Test__order_statistic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = random.randrange(4, 200)

    def test_input(self):
        result = _order_statistic(
            self.n,
        )
        self.assertIsInstance(
            result,
            np.ndarray,
            msg=f"not a float when n={self.n}",
        )

        result = _order_statistic(
            sample_size=self.n,
        )
        self.assertIsInstance(
            result,
            np.ndarray,
            msg=f"not a float when n={self.n}",
        )

    def test_outputs(self):
        result = _order_statistic(self.n)
        self.assertIsInstance(
            result,
            np.ndarray,
            msg=f"not a float when n={self.n}",
        )

    def test_3_8_odd(self):
        n = 9
        expected = np.array(
            [
                0.067568,
                0.175676,
                0.283784,
                0.391892,
                0.500000,
                0.608108,
                0.716216,
                0.824324,
                0.932432,
            ]
        )
        result = _order_statistic(n)
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong statisitc order"
            )

    def test_3_8_even(self):
        n = 10
        expected = np.array(
            [
                0.060976,
                0.158537,
                0.256098,
                0.353659,
                0.451220,
                0.548780,
                0.646341,
                0.743902,
                0.841463,
                0.939024,
            ]
        )
        result = _order_statistic(n)
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong statisitc order"
            )


if __name__ == "__main__":
    unittest.main()
