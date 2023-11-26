"""Tests if  ``test`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/looney_gulledge/test_lg_test.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import random
from scipy import stats

### FUNCTION IMPORT ###
from normtest.looney_gulledge import test

os.system("cls")


class Test_rj_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = stats.norm.rvs(size=random.randint(5, 30))
        alphas = [0.01, 0.05, 0.1]
        cls.alpha = random.sample(alphas, 1)[0]

    def test_inputs(self):
        result = test(
            self.data,
            0.05,
            False,
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
            msg="fnot a float for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[2],
            (float, str),
            msg=f"not a float or forf alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[3],
            str,
            msg=f"not str for alpha={self.alpha}, data={self.data}",
        )

        result = test(
            x_data=self.data,
            alpha=0.05,
            weighted=False,
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
            msg=f"not a float or for alpha={self.alpha}, data={self.data}",
        )
        self.assertIsInstance(
            result[3],
            str,
            msg=f"not str for  alpha={self.alpha}, data={self.data}",
        )


if __name__ == "__main__":
    unittest.main()
