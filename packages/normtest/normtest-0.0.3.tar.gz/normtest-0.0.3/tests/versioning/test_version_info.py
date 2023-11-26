"""Tests if  the version matchs in pyproject and paramcheck (documentation)

--------------------------------------------------------------------------------
Command to run at the prompt:

    python -m unittest -v tests/versioning/test_version_info.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest
import toml


### FUNCTION IMPORT ###
import normtest
from packaging import version

os.system("cls")


class Test_version(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_version(self):
        doc_version = normtest.__version__
        pyproject_version = toml.load("pyproject.toml")["project"]["version"]
        self.assertTrue(
            version.parse(doc_version) == version.parse(pyproject_version),
            msg="versions doesn't match",
        )

    def test_author(self):
        doc_author = normtest.__author__
        pyproject_author = toml.load("pyproject.toml")["project"]["authors"][0]["name"]
        self.assertEqual(doc_author, pyproject_author, msg="main author doesn't match")

    def test_email(self):
        doc_email = normtest.__email__
        pyproject_email = toml.load("pyproject.toml")["project"]["authors"][0]["email"]
        self.assertEqual(doc_email, pyproject_email, msg="main email doesn't match")

    def test_name(self):
        doc_name = normtest.__name__
        pyproject_name = toml.load("pyproject.toml")["project"]["name"]
        self.assertEqual(doc_name, pyproject_name, msg="main name doesn't match")


if __name__ == "__main__":
    unittest.main()
