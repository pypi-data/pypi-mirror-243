"""Tests if  ``fi_test`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test_fi_test.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random
from scipy import stats

### FUNCTION IMPORT ###
from normtest.filliben import fi_test

os.system("cls")


class Test_rj_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = stats.norm.rvs(size=random.randint(5, 30))
        alphas = [0.01, 0.05, 0.1]
        cls.alpha = random.sample(alphas, 1)[0]

    def test_inputs(self):
        result = fi_test(self.data, self.alpha)
        self.assertIsInstance(result, tuple, msg=f"not a tuple")
        self.assertEqual(len(result), 4, msg="Incorrect number of outputs")
        self.assertIsInstance(
            result[0],
            float,
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[1],
            float,
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[2],
            (float, str),
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[3],
            str,
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )

        result = fi_test(
            x_data=self.data,
            alpha=self.alpha,
        )
        self.assertIsInstance(result, tuple, msg=f"not a tuple")
        self.assertEqual(len(result), 4, msg="Incorrect number of outputs")
        self.assertIsInstance(
            result[0],
            float,
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[1],
            float,
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[2],
            (float, str),
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[3],
            str,
            msg=f"not a float for alpha={self.alpha}, data={self.data}",
        )

    def test_filliben_paper(self):
        data = np.array([6, 1, -4, 8, -2, 5, 0])
        result = fi_test(data, alpha=0.05)
        self.assertAlmostEqual(
            result.statistic, 0.98538, places=3, msg="Wrong statistic"
        )
        self.assertAlmostEqual(result.critical, 0.899, places=3, msg="Wrong critical")
        self.assertEqual(result.conclusion, "Fail to reject H₀", msg="Wrong conclusion")

    def test_datasets_weighted_False(self):
        # dataset 1
        i = 1
        data = np.array([44.1, -33.1, 243.1, -25.2, 11])
        result = fi_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.8769, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 2
        i += 1
        data = np.array(
            [
                65.5,
                59.4,
                1.8,
                222.8,
                114.3,
                180.3,
                23.3,
                2.9,
                44.7,
                122.3,
                48.7,
                15.8,
                109.9,
                7.9,
                56.8,
            ]
        )
        result = fi_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.9465, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

    def test_datasets_weighted_True(self):
        # dataset 6
        i = 6
        data = np.array(
            [43.5, 125.1, 166.3, 38.1, 116.7, 25.4, 40, 38.1, 253.7, 81.1, 96.7]
        )
        result = fi_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.9251, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 8
        i = 8
        data = np.array([0.6, 19.2, 82, 0.1, 10.1, 0.6, 20.9, 74.6])
        result = fi_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.8827, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

    def test_x_data(self):
        data = [
            [148, 154, 158, 160, 161, 162, 166, 170, 182, 195, 236],
            (148, 154, 158, 160, 161, 162, 166, 170, 182, 195, 236),
            148,
            148.5,
            "148",
        ]
        for d in data:
            with self.assertRaises(
                TypeError,
                msg=f"Does not raised ValueError when type = {type(d).__name__}",
            ):
                fi_test(d, safe=True)


if __name__ == "__main__":
    unittest.main()
