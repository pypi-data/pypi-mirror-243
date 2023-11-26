"""Tests if  ``dist_plot`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test_dist_plot.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
from matplotlib.axes import SubplotBase
import matplotlib.pyplot as plt
from pathlib import Path

### FUNCTION IMPORT ###
from tests.functions_to_test import functions
from normtest.ryan_joiner import dist_plot

os.system("cls")


class Test_dist_plot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fig, cls.axes = plt.subplots()
        cls.statistic = 0.9225156050800545
        cls.sample_size = 13

    def test_outputs(self):
        result = dist_plot(
            self.axes,
        )
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

        result = dist_plot(
            axes=self.axes,
            critical_range=(4, 50),
            test=(self.statistic, self.sample_size),
        )
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

    def test_basic_plot(self):
        fig1_base_path = Path("tests/ryan_joiner/figs_dist_plot/dist_plot_default.png")

        fig, ax = plt.subplots()
        result = dist_plot(ax)
        fig1_file = Path("tests/ryan_joiner/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_plot_with_test(self):
        fig1_base_path = Path("tests/ryan_joiner/figs_dist_plot/dist_plot_test.png")

        fig, ax = plt.subplots()
        result = dist_plot(ax, test=(self.statistic, self.sample_size))
        fig1_file = Path("tests/ryan_joiner/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_plot_critical_range(self):
        fig1_base_path = Path("tests/ryan_joiner/figs_dist_plot/dist_plot_range.png")

        fig, ax = plt.subplots()
        result = dist_plot(
            ax, test=(self.statistic, self.sample_size), critical_range=(5, 30)
        )
        fig1_file = Path("tests/ryan_joiner/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()


if __name__ == "__main__":
    unittest.main()
