"""Tests if  ``citation`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test_citation.py
    or
    python -m unittest -b tests/ryan_joiner/test_citation.py

--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
from pathlib import Path

### FUNCTION IMPORT ###
from normtest.ryan_joiner import citation

os.system("cls")


class Test_citation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_input(self):
        result = citation()
        self.assertIsInstance(
            result,
            str,
            msg="citation is not a str",
        )

        result = citation(export=False)
        self.assertIsInstance(
            result,
            str,
            msg="citation is not a str",
        )

    def test_export_true(self):
        file_path = Path("RyanJoiner1976.bib")
        result = citation(export=True)
        self.assertTrue(file_path.is_file(), msg="citation not found")
        file_path.unlink()


if __name__ == "__main__":
    unittest.main()
