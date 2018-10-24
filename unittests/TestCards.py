# This workaround makes sure that we can import from the parent dir
import sys
sys.path.append('..')

from scrython.cards import Id, Autocomplete, Search, Collector
import unittest
import time

# Cards for TestCardObjects
mtgo_card = Id(id='e3285e6b-3e79-4d7c-bf96-d920f973b122'); time.sleep(0.1)
non_online_card = Id(id='15016e8e-2f6b-4470-865a-ec13da3cb968'); time.sleep(0.1)
arena_card = Id(id='5aa75f2b-53c5-47c5-96d2-ab796358a96f'); time.sleep(0.1)
augment = Id(id='abe9fdfa-c361-465e-9639-097d441a3f74'); time.sleep(0.1)
meld = Id(id='0900e494-962d-48c6-8e78-66a489be4bb2'); time.sleep(0.1)
transform = Id(id='aae6fb12-b252-453b-bca7-1ea2a0d6c8dc'); time.sleep(0.1)
vanguard = Id(id='87c1234b-3834-4bba-bef2-05707bb1e8e2'); time.sleep(0.1)
alt_lang_card = Collector(code='ths', collector_number='75', lang='ja'); time.sleep(0.1)
planeswalker = Id(id='4c565076-5db2-47ea-8ee0-4a4fd7bb353d'); time.sleep(0.1)

autocomplete = Autocomplete(q='Thal'); time.sleep(0.1)

search = Search(q='f:commander')

class TestCardObjects(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCardObjects, self).__init__(*args, **kwargs)

    def test_object(self):
        self.assertIsInstance(non_online_card.object(), str)
        self.assertEqual(non_online_card.object(), 'card')

    def test_id(self):
        self.assertIsInstance(non_online_card.id(), str)
        self.assertEqual(non_online_card.id(), '15016e8e-2f6b-4470-865a-ec13da3cb968')

    def test_multiverse_ids(self):
        self.assertIsInstance(non_online_card.multiverse_ids(), list)

    def test_mtgo_id(self):
        self.assertRaises(KeyError, non_online_card.mtgo_id)
        self.assertIsInstance(mtgo_card.mtgo_id(), int)
        self.assertEqual(mtgo_card.mtgo_id(), 67196)

    def test_mtgo_foil_id(self):
        self.assertIsInstance(mtgo_card.mtgo_foil_id(), int)
        self.assertEqual(mtgo_card.mtgo_foil_id(), 67197)

    def test_name(self):
        self.assertIsInstance(non_online_card.name(), str)
        self.assertEqual(non_online_card.name(), 'Magical Hack')

    def test_uri(self):
        self.assertIsInstance(non_online_card.uri(), str)
        self.assertEqual(non_online_card.uri(), 'https://api.scryfall.com/cards/15016e8e-2f6b-4470-865a-ec13da3cb968')

    def test_scryfall_uri(self):
        self.assertIsInstance(non_online_card.scryfall_uri(), str)
        self.assertEqual(non_online_card.scryfall_uri(), 'https://scryfall.com/card/ced/64/magical-hack?utm_source=api')

    def test_layout(self):
        self.assertIsInstance(non_online_card.layout(), str)
        self.assertEqual(non_online_card.layout(), 'normal')

    def test_highres_image(self):
        self.assertIsInstance(non_online_card.highres_image(), bool)
        self.assertEqual(non_online_card.highres_image(), True)

    def test_image_uris(self):
        self.assertIsInstance(non_online_card.image_uris(), dict)
        self.assertEqual(non_online_card.image_uris(), {
            "small": "https://img.scryfall.com/cards/small/en/ced/64.jpg?1517813031",
            "normal": "https://img.scryfall.com/cards/normal/en/ced/64.jpg?1517813031",
            "large": "https://img.scryfall.com/cards/large/en/ced/64.jpg?1517813031",
            "png": "https://img.scryfall.com/cards/png/en/ced/64.png?1517813031",
            "art_crop": "https://img.scryfall.com/cards/art_crop/en/ced/64.jpg?1517813031",
            "border_crop": "https://img.scryfall.com/cards/border_crop/en/ced/64.jpg?1517813031"
        })

    def test_cmc(self):
        self.assertIsInstance(non_online_card.cmc(), float)
        self.assertEqual(non_online_card.cmc(), 1.0)

    def test_type_line(self):
        self.assertIsInstance(non_online_card.type_line(), str)
        self.assertEqual(non_online_card.type_line(), 'Instant')

    def test_oracle_text(self):
        self.assertIsInstance(non_online_card.oracle_text(), str)
        self.assertEqual(non_online_card.oracle_text(), 'Change the text of target spell or permanent by replacing all instances of one basic land type with another. (For example, you may change \"swampwalk\" to \"plainswalk.\" This effect lasts indefinitely.)')

    def test_mana_cost(self):
        self.assertIsInstance(non_online_card.mana_cost(), str)
        self.assertEqual(non_online_card.mana_cost(), '{U}')

    def test_colors(self):
        self.assertIsInstance(non_online_card.colors(), list)
        self.assertEqual(non_online_card.colors(), [
            "U"
        ])

    def test_color_identity(self):
        self.assertIsInstance(non_online_card.color_identity(), list)
        self.assertEqual(non_online_card.color_identity(), [
            "U"
        ])

    def test_legalities(self):
        self.assertIsInstance(non_online_card.legalities(), dict)
        self.assertEqual(non_online_card.legalities(), {
            "standard": "not_legal",
            "future": "not_legal",
            "frontier": "not_legal",
            "modern": "not_legal",
            "legacy": "legal",
            "pauper": "not_legal",
            "vintage": "legal",
            "penny": "not_legal",
            "commander": "legal",
            "1v1": "not_legal",
            "duel": "legal",
            "brawl": "not_legal"
        })

    def test_reserved(self):
        self.assertIsInstance(non_online_card.reserved(), bool)
        self.assertEqual(non_online_card.reserved(), False)

    def test_reprint(self):
        self.assertIsInstance(non_online_card.reprint(), bool)
        self.assertEqual(non_online_card.reprint(), True)

    def test_set_code(self):
        self.assertIsInstance(non_online_card.set_code(), str)
        self.assertEqual(non_online_card.set_code(), 'ced')

    def test_set_name(self):
        self.assertIsInstance(non_online_card.set_name(), str)
        self.assertEqual(non_online_card.set_name(), 'Collectors\u2019 Edition')

    def test_set_uri(self):
        self.assertIsInstance(non_online_card.set_uri(), str)
        self.assertEqual(non_online_card.set_uri(), 'https://api.scryfall.com/sets/ced')

    def test_set_search_uri(self):
        self.assertIsInstance(non_online_card.set_search_uri(), str)
        self.assertEqual(non_online_card.set_search_uri(), 'https://api.scryfall.com/cards/search?order=set&q=e%3Aced&unique=prints')

    def test_scryfall_set_uri(self):
        self.assertIsInstance(non_online_card.scryfall_set_uri(), str)
        self.assertEqual(non_online_card.scryfall_set_uri(), 'https://scryfall.com/sets/ced?utm_source=api')

    def test_rulings_uri(self):
        self.assertIsInstance(non_online_card.rulings_uri(), str)
        self.assertEqual(non_online_card.rulings_uri(), 'https://api.scryfall.com/cards/15016e8e-2f6b-4470-865a-ec13da3cb968/rulings')

    def test_prints_search_uri(self):
        self.assertIsInstance(non_online_card.prints_search_uri(), str)
        self.assertEqual(non_online_card.prints_search_uri(), 'https://api.scryfall.com/cards/search?order=set&q=%21%E2%80%9CMagical+Hack%E2%80%9D+include%3Aextras&unique=prints')

    def test_collector_number(self):
        self.assertIsInstance(non_online_card.collector_number(), str)
        self.assertEqual(non_online_card.collector_number(), '64')

    def test_digital(self):
        self.assertIsInstance(non_online_card.digital(), bool)
        self.assertEqual(non_online_card.digital(), False)

    def test_rarity(self):
        self.assertIsInstance(non_online_card.rarity(), str)
        self.assertEqual(non_online_card.rarity(), 'rare')

    def test_illuStringation_id(self):
        self.assertIsInstance(non_online_card.illustration_id(), str)
        self.assertEqual(non_online_card.illustration_id(), 'ac51706f-d485-4d91-822f-bdf9eca67a48')

    def test_artist(self):
        self.assertIsInstance(non_online_card.artist(), str)
        self.assertEqual(non_online_card.artist(), 'Julie Baroh')

    def test_frame(self):
        self.assertIsInstance(non_online_card.frame(), str)
        self.assertEqual(non_online_card.frame(), '1993')

    def test_full_art(self):
        self.assertIsInstance(non_online_card.full_art(), bool)
        self.assertEqual(non_online_card.full_art(), False)

    def test_border_color(self):
        self.assertIsInstance(non_online_card.border_color(), str)
        self.assertEqual(non_online_card.border_color(), 'black')

    def test_timeshifted(self):
        self.assertIsInstance(non_online_card.timeshifted(), bool)
        self.assertEqual(non_online_card.timeshifted(), False)

    def test_colorshifted(self):
        self.assertIsInstance(non_online_card.colorshifted(), bool)
        self.assertEqual(non_online_card.colorshifted(), False)

    def test_futureshifted(self):
        self.assertIsInstance(non_online_card.futureshifted(), bool)
        self.assertEqual(non_online_card.futureshifted(), False)

    def test_edhrec_rank(self):
        self.assertIsInstance(non_online_card.edhrec_rank(), int)

    def test_currency(self):
        self.assertIsInstance(non_online_card.currency('eur'), str)

    def test_related_uris(self):
        self.assertIsInstance(non_online_card.related_uris(), dict)
        self.assertEqual(non_online_card.related_uris(), {
            "tcgplayer_decks": "http://decks.tcgplayer.com/magic/deck/search?contains=Magical+Hack&page=1&partner=Scryfall",
            "edhrec": "http://edhrec.com/route/?cc=Magical+Hack",
            "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Magical+Hack"
        })

    def test_purchase_uris(self):
        self.assertIsInstance(non_online_card.purchase_uris(), dict)
        self.assertEqual(non_online_card.purchase_uris(), {
            "amazon": "https://www.amazon.com/gp/search?ie=UTF8&index=toys-and-games&keywords=Magical+Hack&tag=scryfall-20",
            "ebay": "http://rover.ebay.com/rover/1/711-53200-19255-0/1?campid=5337966903&icep_catId=19107&icep_ff3=10&icep_sortBy=12&icep_uq=Magical+Hack&icep_vectorid=229466&ipn=psmain&kw=lg&kwid=902099&mtid=824&pub=5575230669&toolid=10001",
            "tcgplayer": "https://scryfall.com/s/tcgplayer/97547",
            "magiccardmarket": "https://scryfall.com/s/mcm/17013",
            "cardhoarder": "https://www.cardhoarder.com/cards?affiliate_id=scryfall&data%5Bsearch%5D=Magical+Hack&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall",
            "card_kingdom": "https://www.cardkingdom.com/catalog/search?filter%5Bname%5D=Magical+Hack&partner=scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "mtgo_traders": "http://www.mtgotraders.com/store/search.php?q=Magical+Hack&referral=scryfall",
            "coolstuffinc": "https://scryfall.com/s/coolstuffinc/1677222"
        })

    def test_life_modifier(self):
        self.assertIsInstance(vanguard.life_modifier(), str)
        self.assertEqual(vanguard.life_modifier(), '+18')

    def test_hand_modifier(self):
        self.assertIsInstance(vanguard.hand_modifier(), str)
        self.assertEqual(vanguard.hand_modifier(), '-2')

    def test_color_indicator(self):
        self.assertIsInstance(transform.color_indicator(1), list)
        self.assertEqual(transform.color_indicator(1), [
                "G",
                "R"
            ])

    def test_all_parts(self):
        self.assertIsInstance(transform.all_parts(), list)
        self.assertEqual(transform.all_parts(), [
            {
                "object": "related_card",
                "id": "aae6fb12-b252-453b-bca7-1ea2a0d6c8dc",
                "name": "Huntmaster of the Fells // Ravager of the Fells",
                "uri": "https://api.scryfall.com/cards/dka/140"
            },
            {
                "object": "related_card",
                "id": "a53f8031-aaa8-424c-929a-5478538a8cc6",
                "name": "Wolf",
                "uri": "https://api.scryfall.com/cards/tisd/12"
            }
        ])

    def non_online_card_faces(self):
        self.assertIsInstance(transform.card_faces(), list)
        self.assertEqual(transform.card_faces(), [
            {
                "object": "card_face",
                "name": "Huntmaster of the Fells",
                "mana_cost": "{2}{R}{G}",
                "type_line": "Creature \u2014 Human Werewolf",
                "oracle_text": "Whenever this creature enters the battlefield or transforms into Huntmaster of the Fells, create a 2/2 green Wolf creature token and you gain 2 life.\nAt the beginning of each upkeep, if no spells were cast last turn, transform Huntmaster of the Fells.",
                "colors": [
                    "G",
                    "R"
                ],
                "power": "2",
                "toughness": "2",
                "artist": "Chris Rahn",
                "illustration_id": "8ce1bfa2-7cd6-4f4f-b23e-c5d985acec48",
                "image_uris": {
                    "small": "https://img.scryfall.com/cards/small/en/dka/140a.jpg?1518205189",
                    "normal": "https://img.scryfall.com/cards/normal/en/dka/140a.jpg?1518205189",
                    "large": "https://img.scryfall.com/cards/large/en/dka/140a.jpg?1518205189",
                    "png": "https://img.scryfall.com/cards/png/en/dka/140a.png?1518205189",
                    "art_crop": "https://img.scryfall.com/cards/art_crop/en/dka/140a.jpg?1518205189",
                    "border_crop": "https://img.scryfall.com/cards/border_crop/en/dka/140a.jpg?1518205189"
                }
            },
            {
                "object": "card_face",
                "name": "Ravager of the Fells",
                "mana_cost": "",
                "type_line": "Creature \u2014 Werewolf",
                "oracle_text": "Trample\nWhenever this creature transforms into Ravager of the Fells, it deals 2 damage to target opponent or planeswalker and 2 damage to up to one target creature that player or that planeswalker's controller controls.\nAt the beginning of each upkeep, if a player cast two or more spells last turn, transform Ravager of the Fells.",
                "colors": [
                    "G",
                    "R"
                ],
                "color_indicator": [
                    "G",
                    "R"
                ],
                "power": "4",
                "toughness": "4",
                "artist": "Chris Rahn",
                "illustration_id": "a26de848-cc6a-4f49-9d43-72afa3c80b3e",
                "image_uris": {
                    "small": "https://img.scryfall.com/cards/small/en/dka/140b.jpg?1518205189",
                    "normal": "https://img.scryfall.com/cards/normal/en/dka/140b.jpg?1518205189",
                    "large": "https://img.scryfall.com/cards/large/en/dka/140b.jpg?1518205189",
                    "png": "https://img.scryfall.com/cards/png/en/dka/140b.png?1518205189",
                    "art_crop": "https://img.scryfall.com/cards/art_crop/en/dka/140b.jpg?1518205189",
                    "border_crop": "https://img.scryfall.com/cards/border_crop/en/dka/140b.jpg?1518205189"
                }
            }
        ])

    def test_watermark(self):
        self.assertIsInstance(mtgo_card.watermark(), str)
        self.assertEqual(mtgo_card.watermark(), 'set')

    def test_story_spotlight(self):
        self.assertIsInstance(non_online_card.story_spotlight(), bool)
        self.assertEqual(non_online_card.story_spotlight(), False)

    def test_power(self):
        self.assertIsInstance(augment.power(), str)
        self.assertEqual(augment.power(), '+4')

    def test_toughness(self):
        self.assertIsInstance(augment.toughness(), str)
        self.assertEqual(augment.toughness(), '+4')

    def test_flavor_text(self):
        self.assertIsInstance(meld.flavor_text(), str)
        self.assertEqual(meld.flavor_text(), "\"We're ready for anything!\"")

    def test_arena_id(self):
        self.assertIsInstance(arena_card.arena_id(), int)
        self.assertEqual(arena_card.arena_id(), 66975)

    def test_lang(self):
        self.assertIsInstance(non_online_card.lang(), str)
        self.assertEqual(non_online_card.lang(), 'en')

    def test_printed_name(self):
        self.assertIsInstance(alt_lang_card.printed_name(), str)
        self.assertEqual(alt_lang_card.printed_name(), '忌まわしき首領')

    def test_printed_type_line(self):
        self.assertIsInstance(alt_lang_card.printed_type_line(), str)
        self.assertEqual(alt_lang_card.printed_type_line(), 'クリーチャー — デーモン')

    def test_printed_text(self):
        self.assertIsInstance(alt_lang_card.printed_text(), str)
        self.assertEqual(alt_lang_card.printed_text(), '飛行\n忌まわしき首領が戦場に出たとき、飛行を持つ黒の１/１のハーピー・クリーチャー・トークンをあなたの黒への信心に等しい数だけ戦場に出す。（あなたの黒への信心は、あなたがコントロールするパーマネントのマナ・コストに含まれる{B}の総数に等しい。）\nあなたのアップキープの開始時に、クリーチャーを１体生け贄に捧げる。')

    def test_oracle_id(self):
        self.assertIsInstance(non_online_card.oracle_id(), str)
        self.assertEqual(non_online_card.oracle_id(), 'cba229fa-9035-405b-b091-3798898a37ee')

    def test_foil(self):
        self.assertIsInstance(non_online_card.foil(), bool)
        self.assertEqual(non_online_card.foil(), False)

    def test_loyalty(self):
        self.assertIsInstance(planeswalker.loyalty(), str)
        self.assertEqual(planeswalker.loyalty(), '4')

    def test_non_foil(self):
        self.assertIsInstance(non_online_card.nonfoil(), bool)
        self.assertEqual(non_online_card.nonfoil(), True)

    def test_oversized(self):
        self.assertIsInstance(non_online_card.oversized(), bool)
        self.assertEqual(non_online_card.oversized(), False)

class TestAutocomplete(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(autocomplete.object(), str)
        self.assertEqual(autocomplete.object(), 'catalog')

    def test_total_items(self):
        self.assertIsInstance(autocomplete.total_values(), int)

    def test_data(self):
        self.assertIsInstance(autocomplete.data(), list)

class TestSearch(unittest.TestCase):

    def test_object(self):
        self.assertIsInstance(search.object(), str)
        self.assertEqual(search.object(), 'list')

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

    def test_data_tuple(self):
        self.assertIsInstance(search.data_tuple(0), dict)

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
