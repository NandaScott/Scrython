# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.cards import Id, Autocomplete, Search, Collector
import unittest
import time

# Cards for TestCardObjects
mtgo_card = Id(id='e3285e6b-3e79-4d7c-bf96-d920f973b122'); time.sleep(0.1)
non_online_card = Id(id='cfdd00f0-c6aa-4e8b-a035-fb3403711741'); time.sleep(0.1)
frame_effected_card = Id(id='f185a734-a32a-4244-88e8-dabafbfd064f'); time.sleep(0.1)
arena_card = Id(id='5aa75f2b-53c5-47c5-96d2-ab796358a96f'); time.sleep(0.1)
augment = Id(id='abe9fdfa-c361-465e-9639-097d441a3f74'); time.sleep(0.1)
meld = Id(id='0900e494-962d-48c6-8e78-66a489be4bb2'); time.sleep(0.1)
transform = Id(id='aae6fb12-b252-453b-bca7-1ea2a0d6c8dc'); time.sleep(0.1)
vanguard = Id(id='87c1234b-3834-4bba-bef2-05707bb1e8e2'); time.sleep(0.1)
alt_lang_card = Collector(code='ths', collector_number='75', lang='ja'); time.sleep(0.1)
planeswalker = Id(id='4c565076-5db2-47ea-8ee0-4a4fd7bb353d'); time.sleep(0.1)
preview_check = Id(id='fb6b12e7-bb93-4eb6-bad1-b256a6ccff4e'); time.sleep(0.1)

autocomplete = Autocomplete(q='Thal'); time.sleep(0.1)

search = Search(q='f:commander')

class TestCardObjects(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCardObjects, self).__init__(*args, **kwargs)

    def test_object(self):
        self.assertIsInstance(non_online_card.object(), str)

    def test_id(self):
        self.assertIsInstance(non_online_card.id(), str)

    def test_multiverse_ids(self):
        self.assertIsInstance(non_online_card.multiverse_ids(), list)

    def test_mtgo_id(self):
        self.assertRaises(KeyError, non_online_card.mtgo_id)
        self.assertIsInstance(mtgo_card.mtgo_id(), int)

    def test_mtgo_foil_id(self):
        self.assertIsInstance(mtgo_card.mtgo_foil_id(), int)

    def test_name(self):
        self.assertIsInstance(non_online_card.name(), str)

    def test_uri(self):
        self.assertIsInstance(non_online_card.uri(), str)

    def test_scryfall_uri(self):
        self.assertIsInstance(non_online_card.scryfall_uri(), str)

    def test_layout(self):
        self.assertIsInstance(non_online_card.layout(), str)

    def test_highres_image(self):
        self.assertIsInstance(non_online_card.highres_image(), bool)

    def test_image_uris(self):
        self.assertIsInstance(non_online_card.image_uris(), dict)
        self.assertRaises(Exception, non_online_card.image_uris, 'normal')
        self.assertRaises(KeyError, non_online_card.image_uris, 0, 'foo')

    def test_cmc(self):
        self.assertIsInstance(non_online_card.cmc(), float)

    def test_type_line(self):
        self.assertIsInstance(non_online_card.type_line(), str)

    def test_oracle_text(self):
        self.assertIsInstance(non_online_card.oracle_text(), str)

    def test_mana_cost(self):
        self.assertIsInstance(non_online_card.mana_cost(), str)

    def test_colors(self):
        self.assertIsInstance(non_online_card.colors(), list)

    def test_color_identity(self):
        self.assertIsInstance(non_online_card.color_identity(), list)

    def test_legalities(self):
        self.assertIsInstance(non_online_card.legalities(), dict)

    def test_reserved(self):
        self.assertIsInstance(non_online_card.reserved(), bool)

    def test_reprint(self):
        self.assertIsInstance(non_online_card.reprint(), bool)

    def test_set_code(self):
        self.assertIsInstance(non_online_card.set_code(), str)

    def test_set_name(self):
        self.assertIsInstance(non_online_card.set_name(), str)

    def test_set_uri(self):
        self.assertIsInstance(non_online_card.set_uri(), str)

    def test_set_search_uri(self):
        self.assertIsInstance(non_online_card.set_search_uri(), str)

    def test_scryfall_set_uri(self):
        self.assertIsInstance(non_online_card.scryfall_set_uri(), str)

    def test_rulings_uri(self):
        self.assertIsInstance(non_online_card.rulings_uri(), str)

    def test_prints_search_uri(self):
        self.assertIsInstance(non_online_card.prints_search_uri(), str)

    def test_collector_number(self):
        self.assertIsInstance(non_online_card.collector_number(), str)

    def test_digital(self):
        self.assertIsInstance(non_online_card.digital(), bool)

    def test_rarity(self):
        self.assertIsInstance(non_online_card.rarity(), str)

    def test_illuStringation_id(self):
        self.assertIsInstance(non_online_card.illustration_id(), str)

    def test_artist(self):
        self.assertIsInstance(non_online_card.artist(), str)

    def test_frame(self):
        self.assertIsInstance(non_online_card.frame(), str)

    def test_full_art(self):
        self.assertIsInstance(non_online_card.full_art(), bool)

    def test_border_color(self):
        self.assertIsInstance(non_online_card.border_color(), str)

    def test_edhrec_rank(self):
        self.assertIsInstance(non_online_card.edhrec_rank(), int)

    def test_prices(self):
        self.assertIsInstance(non_online_card.prices('eur'), str)

    def test_related_uris(self):
        self.assertIsInstance(non_online_card.related_uris(), dict)

    def test_purchase_uris(self):
        self.assertIsInstance(non_online_card.purchase_uris(), dict)

    def test_life_modifier(self):
        self.assertIsInstance(vanguard.life_modifier(), str)

    def test_hand_modifier(self):
        self.assertIsInstance(vanguard.hand_modifier(), str)

    def test_color_indicator(self):
        self.assertIsInstance(transform.color_indicator(1), list)

    def test_all_parts(self):
        self.assertIsInstance(transform.all_parts(), list)

    def non_online_card_faces(self):
        self.assertIsInstance(transform.card_faces(), list)

    def test_watermark(self):
        self.assertIsInstance(mtgo_card.watermark(), str)

    def test_story_spotlight(self):
        self.assertIsInstance(non_online_card.story_spotlight(), bool)

    def test_power(self):
        self.assertIsInstance(augment.power(), str)

    def test_toughness(self):
        self.assertIsInstance(augment.toughness(), str)

    def test_flavor_text(self):
        self.assertIsInstance(meld.flavor_text(), str)

    def test_arena_id(self):
        self.assertIsInstance(arena_card.arena_id(), int)

    def test_lang(self):
        self.assertIsInstance(non_online_card.lang(), str)

    def test_printed_name(self):
        self.assertIsInstance(alt_lang_card.printed_name(), str)

    def test_printed_type_line(self):
        self.assertIsInstance(alt_lang_card.printed_type_line(), str)

    def test_printed_text(self):
        self.assertIsInstance(alt_lang_card.printed_text(), str)

    def test_oracle_id(self):
        self.assertIsInstance(non_online_card.oracle_id(), str)

    def test_foil(self):
        self.assertIsInstance(non_online_card.foil(), bool)

    def test_loyalty(self):
        self.assertIsInstance(planeswalker.loyalty(), str)

    def test_non_foil(self):
        self.assertIsInstance(non_online_card.nonfoil(), bool)

    def test_oversized(self):
        self.assertIsInstance(non_online_card.oversized(), bool)

    def test_preview(self):
        self.assertIsInstance(preview_check.preview(), dict)
        self.assertIsInstance(preview_check.preview('source'), str)

class TestAutocomplete(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(autocomplete.object(), str)

    def test_total_items(self):
        self.assertIsInstance(autocomplete.total_values(), int)

    def test_data(self):
        self.assertIsInstance(autocomplete.data(), list)

class TestSearch(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(search.object(), str)

    def test_total_cards(self):
        self.assertIsInstance(search.total_cards(), int)

    def test_data(self):
        self.assertIsInstance(search.data(), list)

    def test_has_more(self):
        self.assertIsInstance(search.has_more(), bool)

    def test_next_page(self):
        self.assertIsInstance(search.next_page(), str)

    def test_data_length(self):
        self.assertIsInstance(search.data_length(), int)

    def test_tcgplayer_id(self):
        self.assertIsInstance(non_online_card.tcgplayer_id(), int)

    def test_frame_effects(self):
        self.assertIsInstance(frame_effected_card.frame_effects(), list)

    def test_games(self):
        self.assertIsInstance(non_online_card.games(), list)

    def test_promo(self):
        self.assertIsInstance(non_online_card.promo(), bool)

    def test_released_at(self):
        self.assertIsInstance(non_online_card.released_at(), str)


if __name__ == '__main__':
    test_classes_to_run = [
        TestCardObjects,
        TestSearch,
        TestAutocomplete
    ]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
