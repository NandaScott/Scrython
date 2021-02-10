# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.rulings import Id
import unittest

rules = Id(id='a985cfb0-6bae-4b1c-902e-d9d7a1aeec61')

class TestRulings(unittest.TestCase):

    def test_data(self):
        self.assertIsInstance(rules.data(), list)

    def test_data_length(self):
        self.assertIsInstance(rules.data_length(), int)

    def test_has_more(self):
        self.assertIsInstance(rules.has_more(), bool)

    def test_object(self):
        self.assertIsInstance(rules.object(), str)


if __name__ == '__main__':
    unittest.main()