"""Tests if  ``LooneyGulledge`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/looney_gulledge/test_LooneyGulledge.py
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
from normtest import LooneyGulledge

os.system("cls")


class Test_init(unittest.TestCase):
    def test_default(self):
        teste = LooneyGulledge()
        self.assertTrue(teste.safe, msg="wrong safe")
        self.assertEqual(teste.alpha, 0.05, msg="wrong alpha")
        self.assertFalse(teste.weighted, msg="wrong weighted")

    def test_changed(self):
        teste = LooneyGulledge(alpha=0.10, safe=False, weighted=True)
        self.assertFalse(teste.safe, msg="wrong safe")
        self.assertEqual(teste.alpha, 0.10, msg="wrong alpha")
        self.assertTrue(teste.weighted, msg="wrong weighted")

    def test_alpha_not_allowed(self):
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValueError when alpha is not allowed",
        ):
            teste = LooneyGulledge(alpha=0.101)

    def test_weighted_not_allowed(self):
        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when weighted is not bool",
        ):
            teste = LooneyGulledge(weighted="ponderado")


class Test_fit_applied(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = stats.norm.rvs(size=random.randint(5, 30))
        alphas = [0.01, 0.05, 0.1]
        cls.alpha = random.sample(alphas, 1)[0]

    def test_not_applied(self):
        teste = LooneyGulledge()
        self.assertIsNone(teste.conclusion, msg="wrong conclusion")

    def test_applied(self):
        teste = LooneyGulledge()
        teste.fit(self.data)
        self.assertIsInstance(teste.conclusion, str, msg="wrong conclusion type")

    def test_safe(self):
        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when alpha = 0",
        ):
            teste = LooneyGulledge(alpha=0)

        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when alpha = 1",
        ):
            teste = LooneyGulledge(alpha=1)
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValuError when alpha = 0.004",
        ):
            teste = LooneyGulledge(alpha=0.004)
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValuError when alpha = 0.996",
        ):
            teste = LooneyGulledge(alpha=0.996)

        with self.assertRaises(
            TypeError,
            msg=f"Does not raised TypeError when safe=0.996",
        ):
            teste = LooneyGulledge(safe=0.996)


class Test_fit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x_data = np.array([44.1, -33.1, 243.1, -25.2, 11])
        cls.alpha = 0.05

    def test_applied(self):
        teste = LooneyGulledge()
        teste.fit(self.x_data)
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
        self.assertAlmostEqual(teste.statistic, 0.878, places=3, msg="wrong statistic")
        # self.assertAlmostEqual(teste.p_value, 0.048, places=2, msg="wrong p-value")
        self.assertEqual(teste.conclusion, "Reject H₀", msg="wrong conclusion")
        self.assertEqual(len(teste.normality), 4, msg="wrong number of outputs")

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
                teste = LooneyGulledge()
                teste.fit(d)

        data = np.array([[1, 2, 3, 4, 5]])
        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValueError when n dim is wrong",
        ):
            teste = LooneyGulledge()
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
                teste = LooneyGulledge()
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
            teste = LooneyGulledge()
            teste.fit(self.data)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = teste.dist_plot(axes=fig)
            plt.close()

        with self.assertRaises(
            ValueError,
            msg=f"Does not raised ValueError when alphas is not not allowed",
        ):
            teste = LooneyGulledge()
            teste.fit(self.data)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = teste.dist_plot(axes=ax, alphas=[0.01, 0.05, 0.0001])
            plt.close()

    def test_filliben_data(self):
        fig1_base_path = Path(
            "tests/looney_gulledge/figs_dist_plot/filliben_from_class.png"
        )

        teste = LooneyGulledge()
        teste.fit(self.data)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax = teste.dist_plot(axes=ax)
        fig1_file = Path("tests/looney_gulledge/figs_dist_plot/fig1_test.png")
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
            teste = LooneyGulledge()
            teste.fit(self.x_data)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = teste.correlation_plot(axes=fig)
            plt.close()

    def test_basic_plot(self):
        fig1_base_path = Path("tests/looney_gulledge/figs_correlation_plot/fig1.png")

        teste = LooneyGulledge()
        teste.fit(self.x_data)
        fig, ax = plt.subplots()
        result = teste.correlation_plot(ax)
        fig1_file = Path("tests/looney_gulledge/figs_correlation_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_plot_filliben(self):
        x = np.array(
            [43.5, 125.1, 166.3, 38.1, 116.7, 25.4, 40, 38.1, 253.7, 81.1, 96.7]
        )

        fig2_base_path = Path("tests/looney_gulledge/figs_correlation_plot/fig2.png")

        teste = LooneyGulledge(weighted=True)
        teste.fit(x)
        fig, ax = plt.subplots()
        result = teste.correlation_plot(ax)
        fig2_file = Path("tests/looney_gulledge/figs_correlation_plot/fig2_test.png")
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
                teste = LooneyGulledge()
                teste.fit(self.x_data)
                ax = teste.line_up(correct=correct)
                plt.close()

        seeds = [2.0, "2", "True"]
        for seed in seeds:
            with self.assertRaises(
                TypeError,
                msg=f"Does not raised TypeError when seed is not wrong",
            ):
                teste = LooneyGulledge()
                teste.fit(self.x_data)
                ax = teste.line_up(seed=seed)
                plt.close()

        seeds = [-2, 0, -1000]
        for seed in seeds:
            with self.assertRaises(
                ValueError,
                msg=f"Does not raised ValueError when seed is not wrong",
            ):
                teste = LooneyGulledge()
                teste.fit(self.x_data)
                ax = teste.line_up(seed=seed)
                plt.close()

    def test_basic_plot(self):
        fig1_base_path = Path("tests/looney_gulledge/figs_line_up/line_up.png")
        teste = LooneyGulledge()
        teste.fit(self.x_data)
        result = teste.line_up(seed=42)
        fig1_file = Path("tests/looney_gulledge/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

        fig1_base_path = Path("tests/looney_gulledge/figs_line_up/line_up_true.png")
        teste = LooneyGulledge()
        teste.fit(self.x_data)
        result = teste.line_up(correct=True, seed=42)
        fig1_file = Path("tests/looney_gulledge/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_seed(self):
        fig1_base_path = Path("tests/looney_gulledge/figs_line_up/line_up_pi.png")
        teste = LooneyGulledge()
        teste.fit(self.x_data)
        result = teste.line_up(correct=False, seed=31416)
        fig1_file = Path("tests/looney_gulledge/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

        fig1_base_path = Path("tests/looney_gulledge/figs_line_up/line_up_true_pi.png")
        teste = LooneyGulledge()
        teste.fit(self.x_data)
        result = teste.line_up(correct=True, seed=31416)
        fig1_file = Path("tests/looney_gulledge/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

    def test_weighted(self):
        fig1_base_path = Path("tests/looney_gulledge/figs_line_up/line_up_weighted.png")
        teste = LooneyGulledge(weighted=True)
        teste.fit(self.x_data)
        result = teste.line_up(correct=False, seed=42)
        fig1_file = Path("tests/looney_gulledge/figs_line_up/fig1_test.png")
        result.tight_layout()
        plt.savefig(fig1_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()

        fig1_base_path = Path(
            "tests/looney_gulledge/figs_line_up/line_up_true_weighted.png"
        )
        teste = LooneyGulledge(weighted=True)
        teste.fit(self.x_data)
        result = teste.line_up(correct=True, seed=42)
        fig1_file = Path("tests/looney_gulledge/figs_line_up/fig1_test.png")
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
        teste = LooneyGulledge()
        result = teste.citation()
        self.assertIsInstance(
            result,
            str,
            msg="citation is not a str",
        )
        teste = LooneyGulledge()
        result = teste.citation(export=False)
        self.assertIsInstance(
            result,
            str,
            msg="citation is not a str",
        )

    def test_export_true(self):
        file_path = Path("LooneyGulledge1985.bib")
        teste = LooneyGulledge()
        result = teste.citation(export=True)
        self.assertTrue(file_path.is_file(), msg="citation not found")
        file_path.unlink()


if __name__ == "__main__":
    unittest.main()
