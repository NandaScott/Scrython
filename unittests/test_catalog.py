# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.catalog import ArtifactTypes
import unittest

artifacts = ArtifactTypes()

class TestCatalog(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(artifacts.object(), str)
        self.assertEqual(artifacts.object(), 'catalog')

    def test_uri(self):
        self.assertIsInstance(artifacts.uri(), str)

    def test_total_values(self):
        self.assertIsInstance(artifacts.total_values(), int)

    def test_data(self):
        self.assertIsInstance(artifacts.data(), list)

if __name__ == '__main__':
    unittest.main()