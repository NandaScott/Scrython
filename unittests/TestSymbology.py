# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.symbology import ParseMana, Symbology
import unittest
import time

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

    def test_symbol_symbol(self):
        self.assertIsInstance(symbology.symbol_symbol(0), str)

    def test_symbol_loose_variant(self):
        self.assertIsInstance(symbology.symbol_loose_variant(5), str)

    def test_symbol_transposable(self):
        self.assertIsInstance(symbology.symbol_transposable(0), bool)

    def test_symbol_represents_mana(self):
        self.assertIsInstance(symbology.symbol_represents_mana(0), bool)

    def test_symbol_cmc(self):
        self.assertIsInstance(symbology.symbol_cmc(0), float)

    def test_symbol_appears_in_mana_costs(self):
        self.assertIsInstance(symbology.symbol_appears_in_mana_costs(0), bool)

    def test_symbol_funny(self):
        self.assertIsInstance(symbology.symbol_funny(0), bool)

    def test_symbol_colors(self):
        self.assertIsInstance(symbology.symbol_colors(0), list)

    def test_symbol_english(self):
        self.assertIsInstance(symbology.symbol_english(0), str)

    def test_symbol_gatherer_alternates(self):
        self.assertIsInstance(symbology.symbol_gatherer_alternates(0), list)

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