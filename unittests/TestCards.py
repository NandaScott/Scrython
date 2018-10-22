# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.cards import Autocomplete, Id, Collector, Mtgo, Multiverse, Named, Random, Search, ArenaId
import unittest
import time

class TestCards(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCards, self).__init__(*args, **kwargs)
        self.test_card = Id(id='b52d516f-d425-49f1-99cc-17f743aa41b2')
        self.bolt = Named(fuzzy='Lightning Bolt')
        self.catalog = Autocomplete(q='Thal')

    def test_object(self):
        self.assertIsInstance(self.test_card.object(), str)
        self.assertEqual(self.test_card.object(), 'card')

    def test_id(self):
        self.assertIsInstance(self.test_card.id(), str)
        self.assertEqual(self.test_card.id(), 'b52d516f-d425-49f1-99cc-17f743aa41b2')

    def test_multiverse_ids(self):
        self.assertIsInstance(self.test_card.multiverse_ids(), list)

    def test_mtgo_id(self):
        self.assertRaises(KeyError, self.test_card.mtgo_id)
        self.assertIsInstance(self.bolt.mtgo_id(), int)
        self.assertEqual(self.bolt.mtgo_id(), 67196)

    def test_mtgo_foil_id(self):
        self.assertRaises(KeyError, self.test_card.mtgo_foil_id)
        self.assertIsInstance(self.bolt.mtgo_foil_id(), int)
        self.assertEqual(self.bolt.mtgo_foil_id(), 67197)

    def test_name(self):
        self.assertRaises(KeyError, self.catalog.name)
        self.assertIsInstance(self.test_card.name(), str)
        self.assertEqual(self.test_card.name(), 'Impulsive Return')

    def test_uri(self):
        self.assertRaises(KeyError, self.catalog.uri)
        self.assertIsInstance(self.test_card.uri(), str)
        self.assertEqual(self.test_card.uri(), 'https://api.scryfall.com/cards/b52d516f-d425-49f1-99cc-17f743aa41b2')

    def test_scryfall_uri(self):
        self.assertRaises(KeyError, self.catalog.scryfall_uri)
        self.assertIsInstance(self.test_card.scryfall_uri(), str)
        self.assertEqual(self.test_card.scryfall_uri(), 'https://scryfall.com/card/tdag/10/impulsive-return?utm_source=api')

    def test_layout(self):
        self.assertRaises(KeyError, self.catalog.layout)
        self.assertIsInstance(self.test_card.layout(), str)
        self.assertEqual(self.test_card.layout(), 'normal')

    def test_highres_image(self):
        self.assertRaises(KeyError, self.catalog.highres_image)
        self.assertIsInstance(self.test_card.highres_image(), )
        self.assertEqual(self.test_card.highres_image(), )

    def test_image_uris(self):
        self.assertRaises(KeyError, self.catalog.image_uris)
        self.assertIsInstance(self.test_card.image_uris(), )
        self.assertEqual(self.test_card.image_uris(), )

    def test_cmc(self):
        self.assertRaises(KeyError, self.catalog.cmc)
        self.assertIsInstance(self.test_card.cmc(), )
        self.assertEqual(self.test_card.cmc(), )

    def test_type_line(self):
        self.assertRaises(KeyError, self.catalog.type_line)
        self.assertIsInstance(self.test_card.type_line(), )
        self.assertEqual(self.test_card.type_line(), )

    def test_oracle_text(self):
        self.assertRaises(KeyError, self.catalog.oracle_text)
        self.assertIsInstance(self.test_card.oracle_text(), )
        self.assertEqual(self.test_card.oracle_text(), )

    def test_mana_cost(self):
        self.assertRaises(KeyError, self.catalog.mana_cost)
        self.assertIsInstance(self.test_card.mana_cost(), )
        self.assertEqual(self.test_card.mana_cost(), )

    def test_colors(self):
        self.assertRaises(KeyError, self.catalog.colors)
        self.assertIsInstance(self.test_card.colors(), )
        self.assertEqual(self.test_card.colors(), )

    def test_color_identity(self):
        self.assertRaises(KeyError, self.catalog.color_identity)
        self.assertIsInstance(self.test_card.color_identity(), )
        self.assertEqual(self.test_card.color_identity(), )

    def test_legalities(self):
        self.assertRaises(KeyError, self.catalog.legalities)
        self.assertIsInstance(self.test_card.legalities(), )
        self.assertEqual(self.test_card.legalities(), )

    def test_reserved(self):
        self.assertRaises(KeyError, self.catalog.reserved)
        self.assertIsInstance(self.test_card.reserved(), )
        self.assertEqual(self.test_card.reserved(), )

    def test_reprint(self):
        self.assertRaises(KeyError, self.catalog.reprint)
        self.assertIsInstance(self.test_card.reprint(), )
        self.assertEqual(self.test_card.reprint(), )

    def test_set_code(self):
        self.assertRaises(KeyError, self.catalog.set_code)
        self.assertIsInstance(self.test_card.set_code(), )
        self.assertEqual(self.test_card.set_code(), )

    def test_set_name(self):
        self.assertRaises(KeyError, self.catalog.set_name)
        self.assertIsInstance(self.test_card.set_name(), )
        self.assertEqual(self.test_card.set_name(), )

    def test_set_uri(self):
        self.assertRaises(KeyError, self.catalog.set_uri)
        self.assertIsInstance(self.test_card.set_uri(), )
        self.assertEqual(self.test_card.set_uri(), )

    def test_set_search_uri(self):
        self.assertRaises(KeyError, self.catalog.set_search_uri)
        self.assertIsInstance(self.test_card.set_search_uri(), )
        self.assertEqual(self.test_card.set_search_uri(), )

    def test_scryfall_set_uri(self):
        self.assertRaises(KeyError, self.catalog.scryfall_set_uri)
        self.assertIsInstance(self.test_card.scryfall_set_uri(), )
        self.assertEqual(self.test_card.scryfall_set_uri(), )

    def test_rulings_uri(self):
        self.assertRaises(KeyError, self.catalog.rulings_uri)
        self.assertIsInstance(self.test_card.rulings_uri(), )
        self.assertEqual(self.test_card.rulings_uri(), )

    def test_prints_search_uri(self):
        self.assertRaises(KeyError, self.catalog.prints_search_uri)
        self.assertIsInstance(self.test_card.prints_search_uri(), )
        self.assertEqual(self.test_card.prints_search_uri(), )

    def test_collector_number(self):
        self.assertRaises(KeyError, self.catalog.collector_number)
        self.assertIsInstance(self.test_card.collector_number(), )
        self.assertEqual(self.test_card.collector_number(), )

    def test_digital(self):
        self.assertRaises(KeyError, self.catalog.digital)
        self.assertIsInstance(self.test_card.digital(), )
        self.assertEqual(self.test_card.digital(), )

    def test_rarity(self):
        self.assertRaises(KeyError, self.catalog.rarity)
        self.assertIsInstance(self.test_card.rarity(), )
        self.assertEqual(self.test_card.rarity(), )

    def test_illuStringation_id(self):
        self.assertRaises(KeyError, self.catalog.illuStringation_id)
        self.assertIsInstance(self.test_card.illuStringation_id(), )
        self.assertEqual(self.test_card.illuStringation_id(), )

    def test_artist(self):
        self.assertRaises(KeyError, self.catalog.artist)
        self.assertIsInstance(self.test_card.artist(), )
        self.assertEqual(self.test_card.artist(), )

    def test_frame(self):
        self.assertRaises(KeyError, self.catalog.frame)
        self.assertIsInstance(self.test_card.frame(), )
        self.assertEqual(self.test_card.frame(), )

    def test_full_art(self):
        self.assertRaises(KeyError, self.catalog.full_art)
        self.assertIsInstance(self.test_card.full_art(), )
        self.assertEqual(self.test_card.full_art(), )

    def test_border_color(self):
        self.assertRaises(KeyError, self.catalog.border_color)
        self.assertIsInstance(self.test_card.border_color(), )
        self.assertEqual(self.test_card.border_color(), )

    def test_timeshifted(self):
        self.assertRaises(KeyError, self.catalog.timeshifted)
        self.assertIsInstance(self.test_card.timeshifted(), )
        self.assertEqual(self.test_card.timeshifted(), )

    def test_colorshifted(self):
        self.assertRaises(KeyError, self.catalog.colorshifted)
        self.assertIsInstance(self.test_card.colorshifted(), )
        self.assertEqual(self.test_card.colorshifted(), )

    def test_futureshifted(self):
        self.assertRaises(KeyError, self.catalog.futureshifted)
        self.assertIsInstance(self.test_card.futureshifted(), )
        self.assertEqual(self.test_card.futureshifted(), )

    def test_edhrec_rank(self):
        self.assertRaises(KeyError, self.catalog.edhrec_rank)
        self.assertIsInstance(self.test_card.edhrec_rank(), )
        self.assertEqual(self.test_card.edhrec_rank(), )

    def test_currency(self):
        self.assertRaises(KeyError, self.catalog.currency)
        self.assertIsInstance(self.test_card.currency(), )
        self.assertEqual(self.test_card.currency(), )

    def test_related_uris(self):
        self.assertRaises(KeyError, self.catalog.related_uris)
        self.assertIsInstance(self.test_card.related_uris(), )
        self.assertEqual(self.test_card.related_uris(), )

    def test_purchase_uris(self):
        self.assertRaises(KeyError, self.catalog.purchase_uris)
        self.assertIsInstance(self.test_card.purchase_uris(), )
        self.assertEqual(self.test_card.purchase_uris(), )

    def test_life_modifier(self):
        self.assertRaises(KeyError, self.catalog.life_modifier)
        self.assertIsInstance(self.test_card.life_modifier(), )
        self.assertEqual(self.test_card.life_modifier(), )

    def test_hand_modifier(self):
        self.assertRaises(KeyError, self.catalog.hand_modifier)
        self.assertIsInstance(self.test_card.hand_modifier(), )
        self.assertEqual(self.test_card.hand_modifier(), )

    def test_color_indicator(self):
        self.assertRaises(KeyError, self.catalog.color_indicator)
        self.assertIsInstance(self.test_card.color_indicator(), )
        self.assertEqual(self.test_card.color_indicator(), )

    def test_all_parts(self):
        self.assertRaises(KeyError, self.catalog.all_parts)
        self.assertIsInstance(self.test_card.all_parts(), )
        self.assertEqual(self.test_card.all_parts(), )

    def test_card_faces(self):
        self.assertRaises(KeyError, self.catalog.card_faces)
        self.assertIsInstance(self.test_card.card_faces(), )
        self.assertEqual(self.test_card.card_faces(), )

    def test_watermark(self):
        self.assertRaises(KeyError, self.catalog.watermark)
        self.assertIsInstance(self.test_card.watermark(), )
        self.assertEqual(self.test_card.watermark(), )

    def test_story_spotlight(self):
        self.assertRaises(KeyError, self.catalog.story_spotlight)
        self.assertIsInstance(self.test_card.story_spotlight(), )
        self.assertEqual(self.test_card.story_spotlight(), )

    def test_power(self):
        self.assertRaises(KeyError, self.catalog.power)
        self.assertIsInstance(self.test_card.power(), )
        self.assertEqual(self.test_card.power(), )

    def test_toughness(self):
        self.assertRaises(KeyError, self.catalog.toughness)
        self.assertIsInstance(self.test_card.toughness(), )
        self.assertEqual(self.test_card.toughness(), )

    def test_flavor_text(self):
        self.assertRaises(KeyError, self.catalog.flavor_text)
        self.assertIsInstance(self.test_card.flavor_text(), )
        self.assertEqual(self.test_card.flavor_text(), )

    def test_arena_id(self):
        self.assertRaises(KeyError, self.catalog.arena_id)
        self.assertIsInstance(self.test_card.arena_id(), )
        self.assertEqual(self.test_card.arena_id(), )

    def test_lang(self):
        self.assertRaises(KeyError, self.catalog.lang)
        self.assertIsInstance(self.test_card.lang(), )
        self.assertEqual(self.test_card.lang(), )

    def test_printed_name(self):
        self.assertRaises(KeyError, self.catalog.printed_name)
        self.assertIsInstance(self.test_card.printed_name(), )
        self.assertEqual(self.test_card.printed_name(), )

    def test_printed_type_line(self):
        self.assertRaises(KeyError, self.catalog.printed_type_line)
        self.assertIsInstance(self.test_card.printed_type_line(), )
        self.assertEqual(self.test_card.printed_type_line(), )

    def test_printed_text(self):
        self.assertRaises(KeyError, self.catalog.printed_text)
        self.assertIsInstance(self.test_card.printed_text(), )
        self.assertEqual(self.test_card.printed_text(), )

    def test_oracle_id(self):
        self.assertRaises(KeyError, self.catalog.oracle_id)
        self.assertIsInstance(self.test_card.oracle_id(), )
        self.assertEqual(self.test_card.oracle_id(), )

    def test_foil(self):
        self.assertRaises(KeyError, self.catalog.foil)
        self.assertIsInstance(self.test_card.foil(), )
        self.assertEqual(self.test_card.foil(), )

    def test_loyalty(self):
        self.assertRaises(KeyError, self.catalog.loyalty)
        self.assertIsInstance(self.test_card.loyalty(), )
        self.assertEqual(self.test_card.loyalty(), )

    def test_non_foil(self):
        self.assertRaises(KeyError, self.catalog.non_foil)
        self.assertIsInstance(self.test_card.non_foil(), )
        self.assertEqual(self.test_card.non_foil(), )

    def test_oversized(self):
        self.assertRaises(KeyError, self.catalog.oversized)
        self.assertIsInstance(self.test_card.oversized(), )
        self.assertEqual(self.test_card.oversized(), )

if __name__ == '__main__':
    unittest.main(verbosity=2)