"""Tests if  ``SafeManagement`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/utils/test_SafeManagement.py
--------------------------------------------------------------------------------
"""

### GENERAL IMPORTS ###
import os
import unittest


### CLASS IMPORT ###
from normtest.utils.helpers import SafeManagement

os.system("cls")


class Test_init(unittest.TestCase):
    def test_set_to_false(self):
        teste = SafeManagement(False)
        self.assertFalse(teste.safe, msg="wrong safe")

    def test_default(self):
        teste = SafeManagement()
        self.assertTrue(teste.safe, msg="wrong safe")


class Test_set_safe(unittest.TestCase):
    def test_set_to_false(self):
        teste = SafeManagement()
        teste.set_safe(False)
        self.assertFalse(teste.safe, msg="wrong safe")


class Test_get_safe(unittest.TestCase):
    def test_default(self):
        teste = SafeManagement()
        result = teste.get_safe()
        self.assertTrue(result, msg="wrong safe")


if __name__ == "__main__":
    unittest.main()
