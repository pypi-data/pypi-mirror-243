"""Tests if  ``_make_line_up_data`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test__make_line_up_data.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random
from scipy import stats

### FUNCTION IMPORT ###
from normtest.ryan_joiner import _make_line_up_data

os.system("cls")


class Test_make_line_up_data(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x_data = np.array([5.1, 4.9, 4.7, 4.6, 5, 5.4, 4.6, 5, 4.4, 4.9, 5.4])
        cls.sorted_data = np.array(
            [4.4, 4.6, 4.6, 4.7, 4.9, 4.9, 5.0, 5.0, 5.1, 5.4, 5.4]
        )
        cls.zi = np.array(
            [
                -1.59322,
                -1.06056,
                -0.72791,
                -0.46149,
                -0.22469,
                0.00000,
                0.22469,
                0.46149,
                0.72791,
                1.06056,
                1.59322,
            ]
        )
        cls.y_pred = np.array(
            [
                4.37881,
                4.55610,
                4.66681,
                4.75549,
                4.83431,
                4.90909,
                4.98388,
                5.06269,
                5.15137,
                5.26208,
                5.43937,
            ]
        )

    def test_inputs(self):
        result = _make_line_up_data(
            self.x_data,
            weighted=False,
            cte_alpha="3/8",
        )
        self.assertEqual(len(result), 3, msg="Incorrect number of outputs")
        self.assertIsInstance(result[0], np.ndarray, msg=f"not a numpy array")
        self.assertIsInstance(result[1], np.ndarray, msg=f"not a numpy array")
        self.assertIsInstance(result[2], np.ndarray, msg=f"not a numpy array")

    def test_result_x_data(self):
        result = _make_line_up_data(
            self.x_data,
            weighted=False,
            cte_alpha="3/8",
        )
        for pair in zip(result[0], self.sorted_data):
            self.assertAlmostEqual(pair[0], pair[1], places=5, msg=f"pair not match")

    def test_result_zi(self):
        result = _make_line_up_data(
            self.x_data,
            weighted=False,
            cte_alpha="3/8",
        )
        for pair in zip(result[1], self.zi):
            self.assertAlmostEqual(pair[0], pair[1], places=5, msg=f"pair not match")

    def test_result_y_pred(self):
        result = _make_line_up_data(
            self.x_data,
            weighted=False,
            cte_alpha="3/8",
        )
        for pair in zip(result[2], self.y_pred):
            self.assertAlmostEqual(pair[0], pair[1], places=5, msg=f"pair not match")


if __name__ == "__main__":
    unittest.main()
