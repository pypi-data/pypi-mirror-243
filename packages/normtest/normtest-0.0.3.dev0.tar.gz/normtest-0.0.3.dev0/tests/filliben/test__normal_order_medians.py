"""Tests if  ``_normal_order_medians`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test__normal_order_medians.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np

### FUNCTION IMPORT ###
from normtest.filliben import _normal_order_medians

os.system("cls")


class Test__normal_order_medians(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uniform = np.array(
            [0.0943, 0.2284, 0.3642, 0.5, 0.6358, 0.7716, 0.9057]
        )  # Filliben example
        cls.normal = np.array(
            [-1.31493, -0.74388, -0.34681, 0, 0.34681, 0.74388, 1.31493]
        )

    def test_outputs(self):
        result = _normal_order_medians(self.uniform)
        self.assertTrue(isinstance(result, np.ndarray), msg=f"not numpy type")

        result = _normal_order_medians(mi=self.uniform)
        self.assertTrue(isinstance(result, np.ndarray), msg=f"not numpy type")


if __name__ == "__main__":
    unittest.main()
