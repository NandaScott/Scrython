# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.sets import Code
import unittest

promo_khans = Code('PKTK')

khans = Code('KTK')


class TestSets(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(khans.object(), str)

    def test_code(self):
        self.assertIsInstance(khans.code(), str)

    def test_mtgo_code(self):
        self.assertIsInstance(khans.mtgo_code(), str)

    def test_name(self):
        self.assertIsInstance(khans.name(), str)

    def test_set_type(self):
        self.assertIsInstance(khans.set_type(), str)

    def test_released_at(self):
        self.assertIsInstance(khans.released_at(), str)

    def test_block_code(self):
        self.assertIsInstance(khans.block_code(), str)

    def test_block(self):
        self.assertIsInstance(khans.block(), str)

    def test_parent_set_code(self):
        self.assertIsInstance(promo_khans.parent_set_code(), str)

    def test_card_count(self):
        self.assertIsInstance(khans.card_count(), int)

    def test_digital(self):
        self.assertIsInstance(khans.digital(), bool)

    def test_foil_only(self):
        self.assertIsInstance(khans.foil_only(), bool)

    def test_icon_svg_uri(self):
        self.assertIsInstance(khans.icon_svg_uri(), str)

    def test_search_uri(self):
        self.assertIsInstance(khans.search_uri(), str)

if __name__ == '__main__':
    unittest.main()