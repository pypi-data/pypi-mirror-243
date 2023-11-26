"""Tests if  ``_normal_order_statistic`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/looney_gulledge/test__normal_order_statistic.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import numpy as np


### FUNCTION IMPORT ###
from normtest.looney_gulledge import _normal_order_statistic

os.system("cls")


class Test__normal_order_statistic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x_data = np.array([1, 1.1, 1.2, 1.3, 1.14, 1.5])
        cls.weighted = False

    def test_input(self):
        result = _normal_order_statistic(self.x_data, self.weighted)
        self.assertIsInstance(
            result,
            np.ndarray,
            msg=f"not a numpy output when correct input",
        )

        result = _normal_order_statistic(
            x_data=self.x_data,
            weighted=self.weighted,
        )
        self.assertIsInstance(
            result,
            np.ndarray,
            msg=f"not a numpy output when correct input",
        )

    def test_datasets_repeated_values_weighted_False(self):
        # dataset 1
        x_data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )
        result = _normal_order_statistic(x_data, False)
        expected = np.array(
            [
                -1.67294,
                -1.16188,
                -0.84838,
                -0.60201,
                -0.38787,
                -0.19032,
                0.00000,
                0.19032,
                0.38787,
                0.60201,
                0.84838,
                1.16188,
                1.67294,
            ]
        )
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

        # dataset 6
        x_data = np.array(
            [43.5, 125.1, 166.3, 38.1, 116.7, 25.4, 40, 38.1, 253.7, 81.1, 96.7]
        )
        result = _normal_order_statistic(
            x_data,
            False,
        )
        expected = np.array(
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
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

    def test_datasets_repeated_values_weighted_True(self):
        # dataset 1
        x_data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )
        result = _normal_order_statistic(
            x_data,
            True,
        )
        expected = np.array(
            [
                -1.37281,
                -1.37281,
                -0.84838,
                -0.49211,
                -0.49211,
                -0.19032,
                0.00000,
                0.19032,
                0.38787,
                0.60201,
                0.84838,
                1.16188,
                1.67294,
            ]
        )
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

        # dataset 6
        x_data = np.array(
            [43.5, 125.1, 166.3, 38.1, 116.7, 25.4, 40, 38.1, 253.7, 81.1, 96.7]
        )
        result = _normal_order_statistic(
            x_data,
            True,
        )
        expected = np.array(
            [
                -1.59322,
                -0.88200,
                -0.88200,
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
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

    def test_datasets_weighted_False(self):
        # dataset 1
        x_data = np.array([44.1, -33.1, 243.1, -25.2, 11])
        result = _normal_order_statistic(
            x_data,
            False,
        )
        expected = np.array(
            [
                -1.17976,
                -0.49720,
                0.00000,
                0.49720,
                1.17976,
            ]
        )
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

        # dataset 10
        x_data = np.array(
            [0.876, 0.001, 0.704, 0.852, 0.498, 0.12, 0.094, 0.865, 0.069, 0.019]
        )
        result = _normal_order_statistic(
            x_data,
            False,
        )
        expected = np.array(
            [
                -1.54664,
                -1.00049,
                -0.65542,
                -0.37546,
                -0.12258,
                0.12258,
                0.37546,
                0.65542,
                1.00049,
                1.54664,
            ]
        )
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

    def test_datasets_weighted_True(self):
        # dataset 1
        x_data = np.array([44.1, -33.1, 243.1, -25.2, 11])
        result = _normal_order_statistic(
            x_data,
            True,
        )
        expected = np.array(
            [
                -1.17976,
                -0.49720,
                0.00000,
                0.49720,
                1.17976,
            ]
        )
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )

        # dataset 10
        x_data = np.array(
            [0.876, 0.001, 0.704, 0.852, 0.498, 0.12, 0.094, 0.865, 0.069, 0.019]
        )
        result = _normal_order_statistic(
            x_data,
            True,
        )
        expected = np.array(
            [
                -1.54664,
                -1.00049,
                -0.65542,
                -0.37546,
                -0.12258,
                0.12258,
                0.37546,
                0.65542,
                1.00049,
                1.54664,
            ]
        )
        for pair in zip(result, expected):
            self.assertAlmostEqual(
                pair[0], pair[1], places=5, msg=f"wrong _normal_order_statistic"
            )


if __name__ == "__main__":
    unittest.main()
