"""Tests if  ``line_up`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test_line_up.py
--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

### FUNCTION IMPORT ###
from tests.functions_to_test import functions
from normtest.filliben import line_up

os.system("cls")


class Test_line_up(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x_data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )

    def test_outputs(self):
        result = line_up(
            x_data=self.x_data,
            seed=42,
            correct=False,
        )

        self.assertIsInstance(
            result, matplotlib.figure.Figure, msg="not matplotlib Figure output"
        )

        result = line_up(
            self.x_data,
            42,
            False,
        )

        self.assertIsInstance(
            result, matplotlib.figure.Figure, msg="not matplotlib Figure output"
        )

    def test_basic_plot(self):
        fig1_base_path = Path("tests/filliben/figs_line_up/line_up.png")

        result = line_up(self.x_data, seed=42)
        fig1_file = Path("tests/filliben/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

        fig1_base_path = Path("tests/filliben/figs_line_up/line_up_true.png")

        result = line_up(self.x_data, correct=True, seed=42)
        fig1_file = Path("tests/filliben/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_seed(self):
        fig1_base_path = Path("tests/filliben/figs_line_up/line_up_pi.png")

        result = line_up(self.x_data, correct=False, seed=31416)
        fig1_file = Path("tests/filliben/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

        fig1_base_path = Path("tests/filliben/figs_line_up/line_up_pi_true.png")

        result = line_up(self.x_data, correct=True, seed=31416)
        fig1_file = Path("tests/filliben/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()


if __name__ == "__main__":
    unittest.main()
