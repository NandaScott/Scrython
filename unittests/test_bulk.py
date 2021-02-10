# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.bulk_data import BulkData
import unittest

bulk = BulkData()

class TestBulk(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(bulk.object(), str)

    def test_has_more(self):
        self.assertIsInstance(bulk.has_more(), bool)

    def test_data(self):
        self.assertIsInstance(bulk.data(), list)

    def test_bulk_object(self):
        self.assertIsInstance(bulk.bulk_object(0), str)

    def test_bulk_id(self):
        self.assertIsInstance(bulk.bulk_id(0), str)

    def test_bulk_type(self):
        self.assertIsInstance(bulk.bulk_type(0), str)

    def test_bulk_updated_at(self):
        self.assertIsInstance(bulk.bulk_updated_at(0), str)

    def test_bulk_name(self):
        self.assertIsInstance(bulk.bulk_name(0), str)

    def test_bulk_description(self):
        self.assertIsInstance(bulk.bulk_description(0), str)

    def test_bulk_compressed_size(self):
        self.assertIsInstance(bulk.bulk_compressed_size(0), int)
        self.assertIsInstance(bulk.bulk_compressed_size(0, True), str)

    def test_bulk_uri(self):
        self.assertIsInstance(bulk.bulk_uri(0), str)

    def test_bulk_content_type(self):
        self.assertIsInstance(bulk.bulk_content_type(0), str)

    def test_bulk_content_encoding(self):
        self.assertIsInstance(bulk.bulk_content_encoding(0), str)

if __name__ == '__main__':
    unittest.main()