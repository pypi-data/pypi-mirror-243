"""Tests if  ``_statistic`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test__statistic.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np

### FUNCTION IMPORT ###
from normtest.filliben import _statistic

os.system("cls")


class Test__statistic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x_data = np.array([-4, -2, 0, 1, 5, 6, 8])  # Filliben example
        cls.normal = np.array(
            [-1.31493, -0.74388, -0.34681, 0, 0.34681, 0.74388, 1.31493]
        )
        cls.statistic = 0.98538

    def test_outputs(self):
        result = _statistic(self.x_data, self.normal)
        self.assertTrue(isinstance(result, float), msg=f"not float")

        result = _statistic(x_data=self.x_data, zi=self.normal)
        self.assertTrue(isinstance(result, float), msg=f"not float")

    def test_pass(self):
        result = _statistic(x_data=self.x_data, zi=self.normal)
        self.assertAlmostEqual(
            result, self.statistic, msg="statistic does not match", places=4
        )


if __name__ == "__main__":
    unittest.main()
