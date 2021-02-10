# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.symbology import ParseMana, Symbology
import unittest

parse = ParseMana('URX')

symbology = Symbology()

class TestParseMana(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(parse.object(), str)
        self.assertEqual(parse.object(), 'mana_cost')

    def test_mana_cost(self):
        self.assertIsInstance(parse.mana_cost(), str)
        self.assertEqual(parse.mana_cost(), '{X}{U}{R}')

    def test_cmc(self):
        self.assertIsInstance(parse.cmc(), float)
        self.assertEqual(parse.cmc(), 2.0)

    def test_colors(self):
        self.assertIsInstance(parse.colors(), list)
        self.assertEqual(parse.colors(), ['U', 'R'])

    def test_colorless(self):
        self.assertIsInstance(parse.colorless(), bool)
        self.assertEqual(parse.colorless(), False)

    def test_monocolored(self):
        self.assertIsInstance(parse.monocolored(), bool)
        self.assertEqual(parse.monocolored(), False)

    def test_multicolored(self):
        self.assertIsInstance(parse.multicolored(), bool)
        self.assertEqual(parse.multicolored(), True)

class TestSymbology(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(symbology.object(), str)

    def test_has_more(self):
        self.assertIsInstance(symbology.has_more(), bool)

    def test_data(self):
        self.assertIsInstance(symbology.data(), list)

    def test_data_length(self):
        self.assertIsInstance(symbology.data_length(), int)

if __name__ == '__main__':

    test_classes_to_run = [
        TestParseMana,
        TestSymbology
    ]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)