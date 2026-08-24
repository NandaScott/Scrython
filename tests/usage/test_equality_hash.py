"""Usage tests for equality, hash, and identity of Scrython objects."""

import scrython.cards
import scrython.catalogs

DUMMY_ID = "00000000-0000-0000-0000-000000000000"


def test_card__same_id__is_equal(cards_named__black_lotus):
    card_a = scrython.cards.Named(exact="Black Lotus")
    card_b = scrython.cards.Named(exact="Black Lotus")
    assert card_a == card_b


def test_card__different_id__is_not_equal(cards_named__black_lotus_factory):
    cards_named__black_lotus_factory()
    card_a = scrython.cards.Named(exact="Black Lotus")
    cards_named__black_lotus_factory(DUMMY_ID)
    card_b = scrython.cards.Named(exact="Black Lotus")
    assert card_a != card_b


def test_card__non_handler_object__is_not_equal(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card != "Black Lotus"
    assert card != 42
    assert card != {"id": "bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd"}


def test_card__usable_as_set_member(cards_named__black_lotus_factory):
    cards_named__black_lotus_factory()
    card_a = scrython.cards.Named(exact="Black Lotus")
    cards_named__black_lotus_factory()
    card_b = scrython.cards.Named(exact="Black Lotus")
    cards_named__black_lotus_factory(DUMMY_ID)
    card_c = scrython.cards.Named(exact="Black Lotus")
    unique = {card_a, card_b, card_c}
    assert len(unique) == 2


def test_card__usable_as_dict_key(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    lookup = {card: "owned"}
    assert lookup[card] == "owned"


def test_catalog__id_less__same_instance_is_equal(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert catalog == catalog


def test_catalog__id_less__different_instances_not_equal(catalogs_creature_types):
    catalog_a = scrython.catalogs.CreatureTypes()
    catalog_b = scrython.catalogs.CreatureTypes()
    assert catalog_a != catalog_b
