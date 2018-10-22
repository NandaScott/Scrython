# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.cards import Autocomplete, Id, Collector, Mtgo, Multiverse, Named, Random, Search, ArenaId
import unittest
import time

class TestCards(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCards, self).__init__(*args, **kwargs)
        self.autocomplete = Autocomplete(q='Thal')
        time.sleep(0.1)
        self.by_scryfall_id = Id(id='e3285e6b-3e79-4d7c-bf96-d920f973b122')
        time.sleep(0.1)
        self.collector = Collector(code='v10', collector_number='1')
        time.sleep(0.1)
        self.mtgo = Mtgo(id='66811')
        time.sleep(0.1)
        self.multiverse = Multiverse(id='212630')
        time.sleep(0.1)
        self.named = Named(fuzzy='Lightning Bolt')
        time.sleep(0.1)
        self.random = Random()
        time.sleep(0.1)
        self.search = Search(q='f:commander')
        time.sleep(0.1)
        self.by_arena_id = ArenaId(id='66975')
        time.sleep(0.1)

    def test_object(self):
        self.assertIsInstance(self.autocomplete.object(), str)
        self.assertIsInstance(self.by_scryfall_id.object(), str)
        self.assertIsInstance(self.collector.object(), str)
        self.assertIsInstance(self.mtgo.object(), str)
        self.assertIsInstance(self.multiverse.object(), str)
        self.assertIsInstance(self.named.object(), str)
        self.assertIsInstance(self.random.object(), str)
        self.assertIsInstance(self.search.object(), str)
        self.assertIsInstance(self.by_arena_id.object(), str)
        self.assertIsInstance(self.named.object(), str)

if __name__ == '__main__':
    unittest.main()