# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.cards import Autocomplete, Id, Collector, Mtgo, Multiverse, Named, Random, Search, ArenaId
import unittest
import time

class TestCards(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCards, self).__init__(*args, **kwargs)
        self.non_online_card = Id(id='b52d516f-d425-49f1-99cc-17f743aa41b2')
        self.mtgo_card = Id(id='e3285e6b-3e79-4d7c-bf96-d920f973b122')
        self.catalog = Autocomplete(q='Thal')

    def test_object(self):
        self.assertIsInstance(self.non_online_card.object(), str)
        self.assertEqual(self.non_online_card.object(), 'card')

    def test_id(self):
        self.assertIsInstance(self.non_online_card.id(), str)
        self.assertEqual(self.non_online_card.id(), 'b52d516f-d425-49f1-99cc-17f743aa41b2')

    def test_multiverse_ids(self):
        self.assertIsInstance(self.non_online_card.multiverse_ids(), list)

    def test_mtgo_id(self):
        self.assertRaises(KeyError, self.non_online_card.mtgo_id)
        self.assertIsInstance(self.mtgo_card.mtgo_id(), int)
        self.assertEqual(self.mtgo_card.mtgo_id(), 67196)

    def test_mtgo_foil_id(self):
        self.assertRaises(KeyError, self.non_online_card.mtgo_foil_id)
        self.assertIsInstance(self.mtgo_card.mtgo_foil_id(), int)
        self.assertEqual(self.mtgo_card.mtgo_foil_id(), 67197)

    def test_name(self):
        self.assertRaises(AttributeError, self.catalog.name)
        self.assertIsInstance(self.non_online_card.name(), str)
        self.assertEqual(self.non_online_card.name(), 'Impulsive Return')

    def test_uri(self):
        self.assertRaises(AttributeError, self.catalog.uri)
        self.assertIsInstance(self.non_online_card.uri(), str)
        self.assertEqual(self.non_online_card.uri(), 'https://api.scryfall.com/cards/b52d516f-d425-49f1-99cc-17f743aa41b2')

    def test_scryfall_uri(self):
        self.assertRaises(AttributeError, self.catalog.scryfall_uri)
        self.assertIsInstance(self.non_online_card.scryfall_uri(), str)
        self.assertEqual(self.non_online_card.scryfall_uri(), 'https://scryfall.com/card/tdag/10/impulsive-return?utm_source=api')

    def test_layout(self):
        self.skipTest('Test not set up.')
        self.assertRaises(AttributeError, self.catalog.layout)
        self.assertIsInstance(self.non_online_card.layout(), str)
        self.assertEqual(self.non_online_card.layout(), 'normal')

    def test_highres_image(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.highres_image)
        self.assertIsInstance(self.non_online_card.highres_image(), )
        self.assertEqual(self.non_online_card.highres_image(), )

    def test_image_uris(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.image_uris)
        self.assertIsInstance(self.non_online_card.image_uris(), )
        self.assertEqual(self.non_online_card.image_uris(), )

    def test_cmc(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.cmc)
        self.assertIsInstance(self.non_online_card.cmc(), )
        self.assertEqual(self.non_online_card.cmc(), )

    def test_type_line(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.type_line)
        self.assertIsInstance(self.non_online_card.type_line(), )
        self.assertEqual(self.non_online_card.type_line(), )

    def test_oracle_text(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.oracle_text)
        self.assertIsInstance(self.non_online_card.oracle_text(), )
        self.assertEqual(self.non_online_card.oracle_text(), )

    def test_mana_cost(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.mana_cost)
        self.assertIsInstance(self.non_online_card.mana_cost(), )
        self.assertEqual(self.non_online_card.mana_cost(), )

    def test_colors(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.colors)
        self.assertIsInstance(self.non_online_card.colors(), )
        self.assertEqual(self.non_online_card.colors(), )

    def test_color_identity(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.color_identity)
        self.assertIsInstance(self.non_online_card.color_identity(), )
        self.assertEqual(self.non_online_card.color_identity(), )

    def test_legalities(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.legalities)
        self.assertIsInstance(self.non_online_card.legalities(), )
        self.assertEqual(self.non_online_card.legalities(), )

    def test_reserved(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.reserved)
        self.assertIsInstance(self.non_online_card.reserved(), )
        self.assertEqual(self.non_online_card.reserved(), )

    def test_reprint(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.reprint)
        self.assertIsInstance(self.non_online_card.reprint(), )
        self.assertEqual(self.non_online_card.reprint(), )

    def test_set_code(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.set_code)
        self.assertIsInstance(self.non_online_card.set_code(), )
        self.assertEqual(self.non_online_card.set_code(), )

    def test_set_name(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.set_name)
        self.assertIsInstance(self.non_online_card.set_name(), )
        self.assertEqual(self.non_online_card.set_name(), )

    def test_set_uri(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.set_uri)
        self.assertIsInstance(self.non_online_card.set_uri(), )
        self.assertEqual(self.non_online_card.set_uri(), )

    def test_set_search_uri(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.set_search_uri)
        self.assertIsInstance(self.non_online_card.set_search_uri(), )
        self.assertEqual(self.non_online_card.set_search_uri(), )

    def test_scryfall_set_uri(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.scryfall_set_uri)
        self.assertIsInstance(self.non_online_card.scryfall_set_uri(), )
        self.assertEqual(self.non_online_card.scryfall_set_uri(), )

    def test_rulings_uri(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.rulings_uri)
        self.assertIsInstance(self.non_online_card.rulings_uri(), )
        self.assertEqual(self.non_online_card.rulings_uri(), )

    def test_prints_search_uri(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.prints_search_uri)
        self.assertIsInstance(self.non_online_card.prints_search_uri(), )
        self.assertEqual(self.non_online_card.prints_search_uri(), )

    def test_collector_number(self):
        self.skipTest('Test not set up.')
        self.assertRaises(AttributeError, self.catalog.collector_number)
        self.assertIsInstance(self.non_online_card.collector_number(), )
        self.assertEqual(self.non_online_card.collector_number(), )

    def test_digital(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.digital)
        self.assertIsInstance(self.non_online_card.digital(), )
        self.assertEqual(self.non_online_card.digital(), )

    def test_rarity(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.rarity)
        self.assertIsInstance(self.non_online_card.rarity(), )
        self.assertEqual(self.non_online_card.rarity(), )

    def test_illuStringation_id(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.illuStringation_id)
        self.assertIsInstance(self.non_online_card.illuStringation_id(), )
        self.assertEqual(self.non_online_card.illuStringation_id(), )

    def test_artist(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.artist)
        self.assertIsInstance(self.non_online_card.artist(), )
        self.assertEqual(self.non_online_card.artist(), )

    def test_frame(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.frame)
        self.assertIsInstance(self.non_online_card.frame(), )
        self.assertEqual(self.non_online_card.frame(), )

    def test_full_art(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.full_art)
        self.assertIsInstance(self.non_online_card.full_art(), )
        self.assertEqual(self.non_online_card.full_art(), )

    def test_border_color(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.border_color)
        self.assertIsInstance(self.non_online_card.border_color(), )
        self.assertEqual(self.non_online_card.border_color(), )

    def test_timeshifted(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.timeshifted)
        self.assertIsInstance(self.non_online_card.timeshifted(), )
        self.assertEqual(self.non_online_card.timeshifted(), )

    def test_colorshifted(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.colorshifted)
        self.assertIsInstance(self.non_online_card.colorshifted(), )
        self.assertEqual(self.non_online_card.colorshifted(), )

    def test_futureshifted(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.futureshifted)
        self.assertIsInstance(self.non_online_card.futureshifted(), )
        self.assertEqual(self.non_online_card.futureshifted(), )

    def test_edhrec_rank(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.edhrec_rank)
        self.assertIsInstance(self.non_online_card.edhrec_rank(), )
        self.assertEqual(self.non_online_card.edhrec_rank(), )

    def test_currency(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.currency)
        self.assertIsInstance(self.non_online_card.currency(), )
        self.assertEqual(self.non_online_card.currency(), )

    def test_related_uris(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.related_uris)
        self.assertIsInstance(self.non_online_card.related_uris(), )
        self.assertEqual(self.non_online_card.related_uris(), )

    def test_purchase_uris(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.purchase_uris)
        self.assertIsInstance(self.non_online_card.purchase_uris(), )
        self.assertEqual(self.non_online_card.purchase_uris(), )

    def test_life_modifier(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.life_modifier)
        self.assertIsInstance(self.non_online_card.life_modifier(), )
        self.assertEqual(self.non_online_card.life_modifier(), )

    def test_hand_modifier(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.hand_modifier)
        self.assertIsInstance(self.non_online_card.hand_modifier(), )
        self.assertEqual(self.non_online_card.hand_modifier(), )

    def test_color_indicator(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.color_indicator)
        self.assertIsInstance(self.non_online_card.color_indicator(), )
        self.assertEqual(self.non_online_card.color_indicator(), )

    def test_all_parts(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.all_parts)
        self.assertIsInstance(self.non_online_card.all_parts(), )
        self.assertEqual(self.non_online_card.all_parts(), )

    def non_online_card_faces(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.card_faces)
        self.assertIsInstance(self.non_online_card.card_faces(), )
        self.assertEqual(self.non_online_card.card_faces(), )

    def test_watermark(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.watermark)
        self.assertIsInstance(self.non_online_card.watermark(), )
        self.assertEqual(self.non_online_card.watermark(), )

    def test_story_spotlight(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.story_spotlight)
        self.assertIsInstance(self.non_online_card.story_spotlight(), )
        self.assertEqual(self.non_online_card.story_spotlight(), )

    def test_power(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.power)
        self.assertIsInstance(self.non_online_card.power(), )
        self.assertEqual(self.non_online_card.power(), )

    def test_toughness(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.toughness)
        self.assertIsInstance(self.non_online_card.toughness(), )
        self.assertEqual(self.non_online_card.toughness(), )

    def test_flavor_text(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.flavor_text)
        self.assertIsInstance(self.non_online_card.flavor_text(), )
        self.assertEqual(self.non_online_card.flavor_text(), )

    def test_arena_id(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.arena_id)
        self.assertIsInstance(self.non_online_card.arena_id(), )
        self.assertEqual(self.non_online_card.arena_id(), )

    def test_lang(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.lang)
        self.assertIsInstance(self.non_online_card.lang(), )
        self.assertEqual(self.non_online_card.lang(), )

    def test_printed_name(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.printed_name)
        self.assertIsInstance(self.non_online_card.printed_name(), )
        self.assertEqual(self.non_online_card.printed_name(), )

    def test_printed_type_line(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.printed_type_line)
        self.assertIsInstance(self.non_online_card.printed_type_line(), )
        self.assertEqual(self.non_online_card.printed_type_line(), )

    def test_printed_text(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.printed_text)
        self.assertIsInstance(self.non_online_card.printed_text(), )
        self.assertEqual(self.non_online_card.printed_text(), )

    def test_oracle_id(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.oracle_id)
        self.assertIsInstance(self.non_online_card.oracle_id(), )
        self.assertEqual(self.non_online_card.oracle_id(), )

    def test_foil(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.foil)
        self.assertIsInstance(self.non_online_card.foil(), )
        self.assertEqual(self.non_online_card.foil(), )

    def test_loyalty(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.loyalty)
        self.assertIsInstance(self.non_online_card.loyalty(), )
        self.assertEqual(self.non_online_card.loyalty(), )

    def test_non_foil(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.non_foil)
        self.assertIsInstance(self.non_online_card.non_foil(), )
        self.assertEqual(self.non_online_card.non_foil(), )

    def test_oversized(self):
        self.skipTest('Test not set up.')
        self.assertRaises(KeyError, self.catalog.oversized)
        self.assertIsInstance(self.non_online_card.oversized(), )
        self.assertEqual(self.non_online_card.oversized(), )

if __name__ == '__main__':
    unittest.main()
