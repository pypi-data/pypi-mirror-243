"""Tests if  ``dist_plot`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test_dist_plot.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
from matplotlib.axes import SubplotBase
import matplotlib.pyplot as plt
from pathlib import Path

### FUNCTION IMPORT ###
from tests.functions_to_test import functions
from normtest.filliben import dist_plot

os.system("cls")


class Test_dist_plot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fig, cls.axes = plt.subplots()

    def test_outputs(self):
        result = dist_plot(
            self.axes,
            None,
            [0.10, 0.05, 0.01],
        )
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

        result = dist_plot(
            axes=self.axes,
            test=None,
            alphas=[0.10, 0.05, 0.01],
        )
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

    def test_default(self):
        fig1_base_path = Path("tests/filliben/figs_dist_plot/default.png")

        fig, ax = plt.subplots(figsize=(6, 4))
        result = dist_plot(
            ax,
        )
        fig1_file = Path("tests/filliben/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_filliben_data(self):
        fig1_base_path = Path("tests/filliben/figs_dist_plot/filliben_paper.png")

        fig, ax = plt.subplots(figsize=(6, 4))
        result = dist_plot(axes=ax, test=(0.98538, 7))
        fig1_file = Path("tests/filliben/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()


if __name__ == "__main__":
    unittest.main()
