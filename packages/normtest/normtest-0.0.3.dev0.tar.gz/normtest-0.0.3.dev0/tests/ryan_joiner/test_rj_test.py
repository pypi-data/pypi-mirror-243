"""Tests if  ``rj_test`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test_rj_test.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random
from scipy import stats

### FUNCTION IMPORT ###
from normtest.ryan_joiner import rj_test

os.system("cls")


class Test_rj_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = stats.norm.rvs(size=random.randint(5, 30))
        alphas = [0.01, 0.05, 0.1]
        cls.alpha = random.sample(alphas, 1)[0]
        cte_alphas = ["0", "3/8", "1/2"]
        cls.cte_alpha = random.sample(cte_alphas, 1)[0]

    def test_inputs(self):
        result = rj_test(
            self.data,
            0.05,
            self.cte_alpha,
            False,
        )
        self.assertIsInstance(result, tuple, msg=f"not a tuple")
        self.assertEqual(len(result), 4, msg="Incorrect number of outputs")
        self.assertIsInstance(
            result[0],
            float,
            msg=f"not a float for cte_alpha={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[1],
            float,
            msg="not a float for met={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[2],
            (float, str),
            msg="not a float or for met={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[3],
            str,
            msg="not str for met={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )

        result = rj_test(
            x_data=self.data,
            alpha=0.05,
            cte_alpha=self.cte_alpha,
            weighted=False,
        )
        self.assertIsInstance(result, tuple, msg=f"not a tuple")
        self.assertEqual(len(result), 4, msg="Incorrect number of outputs")
        self.assertIsInstance(
            result[0],
            float,
            msg=f"not a float for cte_alpha={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[1],
            float,
            msg="not a float for met={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[2],
            (float, str),
            msg="not a float or for met={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[3],
            str,
            msg="not str for met={self.cte_alpha}, alpha={self.alpha}, data={self.data}",
        )

    def test_statext(self):
        # source https://www.statext.com/practice/NormalityTest03.php
        data = np.array([148, 154, 158, 160, 161, 162, 166, 170, 182, 195, 236])
        result = rj_test(data, alpha=0.05)
        self.assertAlmostEqual(
            result.statistic, 0.878284, places=3, msg="Wrong statistic"
        )
        self.assertAlmostEqual(result.critical, 0.9230, places=3, msg="Wrong critical")
        self.assertEqual(result.conclusion, "Reject H₀", msg="Wrong conclusion")

    def test_youtube(self):
        # source https://www.youtube.com/watch?v=XQDhdllaN_o
        data = np.array(
            [
                15.2,
                12.4,
                15.4,
                16.5,
                15.9,
                17.1,
                16.9,
                14.3,
                19.1,
                18.2,
                18.5,
                16.3,
                20.0,
            ]
        )
        result = rj_test(data, alpha=0.05)
        self.assertAlmostEqual(result.statistic, 0.991, places=3, msg="Wrong statistic")
        self.assertEqual(result.conclusion, "Fail to reject H₀", msg="Wrong conclusion")

    def test_tutorial_minitab(self):
        # source https://youtu.be/z7Nv3x_Q9Gw
        data = np.array(
            [
                1.90642,
                2.22488,
                2.10288,
                1.69742,
                1.52229,
                3.15435,
                2.61826,
                1.98492,
                1.42738,
                1.99568,
            ]
        )
        result = rj_test(data, alpha=0.05)
        self.assertAlmostEqual(result.statistic, 0.960, places=3, msg="Wrong statistic")
        self.assertEqual(result.conclusion, "Fail to reject H₀", msg="Wrong conclusion")

    def test_datasets_weighted_False(self):
        # dataset 1
        i = 1
        data = np.array([44.1, -33.1, 243.1, -25.2, 11])
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.878, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.048, places=2, msg=f"wrong p-value for dataset {i}"
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
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.946, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.083, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 3
        i += 1
        data = np.array(
            [10.8, 62, 38, 102.1, 40.7, 30.2, 86.6, 32.6, 191.3, 74.1, 99.9]
        )
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.931, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.076, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 4
        i += 1
        data = np.array([29.5, 59.5, 24.2, 38.3, 31.2, 1.5, 140.5])
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.881, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.036, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 5
        i += 1
        data = np.array([249.3, 51.1, 19.3, 45.3, 109.1, 75.7, 100.5])
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.903, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.062, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 7
        i = 7
        data = np.array([38.4, 91.8, 83.7, 95.8, 32.1, 99.9, 97.2])
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.878, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.033, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 9
        i = 9
        data = np.array([0.371, 0.819, 0, 0.209, 0.052, 0.021])
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.908, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.091, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 10
        i = 10
        data = np.array(
            [0.876, 0.001, 0.704, 0.852, 0.498, 0.12, 0.094, 0.865, 0.069, 0.019]
        )
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.917, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.049, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 11
        i = 11
        data = np.array(
            [
                -1.124,
                -1.999,
                -1.296,
                -1.148,
                -1.502,
                -1.88,
                -1.906,
                -1.135,
                -1.931,
                -1.981,
                -1.225,
                -1.005,
            ]
        )
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.928, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.053, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 12
        i = 12
        data = np.array(
            [
                0.376,
                -0.499,
                0.204,
                0.352,
                -0.002,
                -0.38,
                -0.406,
                0.365,
                -0.431,
                -0.481,
                0.275,
                0.495,
                -0.5,
                0.019,
                0.416,
                0.173,
            ]
        )
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.937, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.043, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 13
        i = 13
        data = np.array(
            [
                0.332,
                -0.285,
                -2.545,
                -1.008,
                -0.379,
                -1.72,
                -0.734,
                -0.891,
                -0.996,
                -1.175,
                -0.567,
                0.203,
                -1.965,
                0.028,
                -0.771,
                -0.555,
            ]
        )
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.978, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertEqual(
            result.p_value, "p > 0.100", msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 14
        i = 14
        data = np.array(
            [
                0.232,
                1.302,
                1.087,
                0.758,
                0.251,
                0.146,
                0.691,
                0.74,
                3.022,
                1.202,
                0.11,
                0.33,
                3.311,
                0.773,
                0.387,
                0.77,
            ]
        )
        result = rj_test(data)
        self.assertAlmostEqual(
            result.statistic, 0.867, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertEqual(
            result.p_value, "p < 0.010", msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

    def test_datasets_weighted_True(self):
        # dataset 6
        i = 6
        data = np.array(
            [43.5, 125.1, 166.3, 38.1, 116.7, 25.4, 40, 38.1, 253.7, 81.1, 96.7]
        )
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.929, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.068, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 8
        i = 8
        data = np.array([0.6, 19.2, 82, 0.1, 10.1, 0.6, 20.9, 74.6])
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.887, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.033, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 15
        i = 15
        data = np.array([1.3, 1, 1, 0, 52.1, 98.3, 87.6, 78.7, 99.5])
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.913, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.052, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 16
        i = 16
        data = np.array([87.5, 7.5, 22, 90.5, 61.6, 87.5, 99.4, 85.7])
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.903, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.048, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 17
        i = 17
        data = np.array([91.5, 41.8, 69.5, 96.6, 74.8, 96.7, 80.9, 74.8, 3.8])
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.91, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.048, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

    def test_datasets_repeated_values_weighted_True(self):
        # dataset 1
        i = 1
        data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.932, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.051, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion,
            "Fail to reject H₀",
            msg=f"Wrong conclusion for dataset {i}",
        )

        # dataset 1
        i = 2
        data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210, 210]
        )
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.934, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.049, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 1
        i = 3
        data = np.array(
            [148, 148, 154, 158, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210, 210]
        )
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.924, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.029, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 1
        i = 4
        data = np.array(
            [
                148,
                148,
                154,
                158,
                158,
                158,
                160,
                161,
                162,
                166,
                170,
                182,
                195,
                210,
                210,
                210,
            ]
        )
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.930, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.033, places=2, msg=f"wrong p-value for dataset {i}"
        )
        self.assertEqual(
            result.conclusion, "Reject H₀", msg=f"Wrong conclusion for dataset {i}"
        )

        # dataset 1
        i = 5
        data = np.array(
            [
                148,
                148,
                154,
                158,
                158,
                158,
                160,
                161,
                162,
                166,
                170,
                182,
                195,
                210,
                210,
                210,
                210,
            ]
        )
        result = rj_test(data, weighted=True)
        self.assertAlmostEqual(
            result.statistic, 0.936, places=3, msg=f"wrong statistic for dataset {i}"
        )
        self.assertAlmostEqual(
            result.p_value, 0.038, places=2, msg=f"wrong p-value for dataset {i}"
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
                rj_test(d, safe=True)


if __name__ == "__main__":
    unittest.main()
