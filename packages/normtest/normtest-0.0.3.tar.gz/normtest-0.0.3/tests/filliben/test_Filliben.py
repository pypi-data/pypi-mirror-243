"""Tests if  ``Filliben`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/filliben/test_Filliben.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
from scipy import stats
import random
import numpy as np
from matplotlib.axes import SubplotBase
import matplotlib.pyplot as plt
from pathlib import Path

### FUNCTION IMPORT ###
from tests.functions_to_test import functions

### CLASS IMPORT ###
from normtest import Filliben

os.system("cls")


class Test_init(unittest.TestCase):
    def test_default(self):
        teste = Filliben()
        self.assertTrue(teste.safe, msg="wrong safe")
        self.assertEqual(teste.alpha, 0.05, msg="wrong alpha")

    def test_changed(self):
        teste = Filliben(alpha=0.10, safe=False)
        self.assertFalse(teste.safe, msg="wrong safe")
        self.assertEqual(teste.alpha, 0.10, msg="wrong alpha")


class Test_fit_applied(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = stats.norm.rvs(size=random.randint(5, 30))
        alphas = [0.01, 0.05, 0.1]
        cls.alpha = random.sample(alphas, 1)[0]

    def test_not_applied(self):
        teste = Filliben()
        self.assertIsNone(teste.conclusion, msg="wrong conclusion")

    def test_applied(self):
        teste = Filliben()
        teste.fit(self.data)
        self.assertIsInstance(teste.conclusion, str, msg="wrong conclusion type")

    def test_safe(self):
        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when alpha = 0",
        ):
            teste = Filliben(alpha=0)

        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when alpha = 1",
        ):
            teste = Filliben(alpha=1)
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValuError when alpha = 0.004",
        ):
            teste = Filliben(alpha=0.004)
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValuError when alpha = 0.996",
        ):
            teste = Filliben(alpha=0.996)

        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when safe=0.996",
        ):
            teste = Filliben(safe=0.996)


class Test_fit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = np.array([6, 1, -4, 8, -2, 5, 0])
        cls.alpha = 0.05

    def test_applied(self):
        teste = Filliben()
        teste.fit(self.data)
        self.assertAlmostEqual(
            teste.statistic, 0.98538, places=3, msg="wrong statistic"
        )
        self.assertAlmostEqual(teste.critical, 0.899, places=3, msg="wrong critical")
        self.assertEqual(teste.conclusion, "Fail to reject H₀", msg="wrong conclusion")
        self.assertEqual(len(teste.normality), 4, msg="wrong number of outputs")
        self.assertIsInstance(
            teste.normality.statistic, float, msg="wrong type for statistic"
        )
        self.assertIsInstance(
            teste.normality.critical, float, msg="wrong type for critical"
        )
        self.assertIsInstance(
            teste.normality.p_value, float, msg="wrong type for pvalor"
        )
        self.assertIsInstance(
            teste.normality.conclusion, str, msg="wrong type for conclusion"
        )

    def test_safe(self):
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
                teste = Filliben()
                teste.fit(d)

        data = np.array([[1, 2, 3, 4, 5]])
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValueError when n dim is wrong",
        ):
            teste = Filliben()
            teste.fit(data)

        n_values = [
            np.array([1, 2, 3]),
            np.array([1, 2]),
            np.array([1]),
        ]
        for n in n_values:
            with self.assertRaises(
                ValueError,
                msg=f"Does not raised ValueError when sample size is small",
            ):
                teste = Filliben()
                teste.fit(data)


class Test_dist_plot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = np.array([6, 1, -4, 8, -2, 5, 0])

    def test_safe(self):
        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when axes is not axes",
        ):
            teste = Filliben()
            teste.fit(self.data)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = teste.dist_plot(axes=fig)
            plt.close()

        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValueError when alphas is not not allowed",
        ):
            teste = Filliben()
            teste.fit(self.data)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = teste.dist_plot(axes=ax, alphas=[0.01, 0.05, 0.0001])
            plt.close()

    def test_filliben_data(self):
        fig1_base_path = Path("tests/filliben/figs_dist_plot/filliben_paper.png")

        teste = Filliben()
        teste.fit(self.data)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax = teste.dist_plot(axes=ax)
        fig1_file = Path("tests/filliben/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()


class Test_correlation_plot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fig, cls.axes = plt.subplots()
        cls.x_data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )

    def test_safe(self):
        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when axes is not axes",
        ):
            teste = Filliben()
            teste.fit(self.x_data)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = teste.correlation_plot(axes=fig)
            plt.close()

    def test_basic_plot(self):
        fig1_base_path = Path("tests/filliben/figs_correlation_plot/fig1.png")

        teste = Filliben()
        teste.fit(self.x_data)
        fig, ax = plt.subplots()
        result = teste.correlation_plot(ax)
        fig1_file = Path("tests/filliben/figs_correlation_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_plot_filliben(self):
        x = np.array([6, 1, -4, 8, -2, 5, 0])

        fig2_base_path = Path("tests/filliben/figs_correlation_plot/filliben_data.png")

        teste = Filliben()
        teste.fit(x)
        fig, ax = plt.subplots()
        result = teste.correlation_plot(ax)
        fig2_file = Path("tests/filliben/figs_correlation_plot/fig2_test.png")
        plt.savefig(fig2_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig2_base_path, fig2_file),
            msg="figures does not match",
        )
        fig2_file.unlink()


class Test_line_up(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x_data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )

    def test_safe(self):
        corrects = [2, "2", "True"]
        for correct in corrects:
            with self.assertRaises(
                TypeError,
                msg=f"Does not raised TypeError when correct is wrong",
            ):
                teste = Filliben()
                teste.fit(self.x_data)
                ax = teste.line_up(correct=correct)
                plt.close()

        seeds = [2.0, "2", "True"]
        for seed in seeds:
            with self.assertRaises(
                TypeError,
                msg=f"Does not raised TypeError when seed is not wrong",
            ):
                teste = Filliben()
                teste.fit(self.x_data)
                ax = teste.line_up(seed=seed)
                plt.close()

        seeds = [-2, 0, -1000]
        for seed in seeds:
            with self.assertRaises(
                ValueError,
                msg=f"Does not raised ValueError when seed is not wrong",
            ):
                teste = Filliben()
                teste.fit(self.x_data)
                ax = teste.line_up(seed=seed)
                plt.close()

    def test_basic_plot(self):
        fig1_base_path = Path("tests/filliben/figs_line_up/line_up.png")
        teste = Filliben()
        teste.fit(self.x_data)
        result = teste.line_up(seed=42)
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
        teste = Filliben()
        teste.fit(self.x_data)
        result = teste.line_up(correct=True, seed=42)
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
        teste = Filliben()
        teste.fit(self.x_data)
        result = teste.line_up(correct=False, seed=31416)
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
        teste = Filliben()
        teste.fit(self.x_data)
        result = teste.line_up(correct=True, seed=31416)
        fig1_file = Path("tests/filliben/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()


class Test_citation(unittest.TestCase):
    def test_input(self):
        teste = Filliben()
        result = teste.citation()
        self.assertIsInstance(
            result,
            str,
            msg="citation is not a str",
        )
        teste = Filliben()
        result = teste.citation(export=False)
        self.assertIsInstance(
            result,
            str,
            msg="citation is not a str",
        )

    def test_export_true(self):
        file_path = Path("Filliben1975.bib")
        teste = Filliben()
        result = teste.citation(export=True)
        self.assertTrue(file_path.is_file(), msg="citation not found")
        file_path.unlink()


if __name__ == "__main__":
    unittest.main()
