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


def test_manifest__same_printing__row_equals_full_card(
    cards_manifest__row_and_card_same_printing,
):
    row = scrython.cards.Manifest().data[0]
    card = scrython.cards.Search(q="Black Lotus").data[0]
    assert row == card


def test_manifest__same_printing__full_card_equals_row(
    cards_manifest__row_and_card_same_printing,
):
    row = scrython.cards.Manifest().data[0]
    card = scrython.cards.Search(q="Black Lotus").data[0]
    assert card == row


def test_manifest__same_printing__collapses_in_a_set(
    cards_manifest__row_and_card_same_printing,
):
    row = scrython.cards.Manifest().data[0]
    card = scrython.cards.Search(q="Black Lotus").data[0]
    assert len({row, card}) == 1


def test_manifest__different_printing__row_not_equal_to_full_card(
    cards_manifest__row_and_card_different_printings,
):
    row = scrython.cards.Manifest().data[0]
    card = scrython.cards.Search(q="Black Lotus").data[0]
    assert row != card


def test_manifest__distinct_rows__same_id_are_equal(cards_manifest__page_one):
    row_a = scrython.cards.Manifest().data[0]
    row_b = scrython.cards.Manifest().data[0]
    # Guards the premise: instance identity must not be what makes them equal.
    assert row_a is not row_b
    assert row_a == row_b


def test_manifest__row__usable_as_dict_key(cards_manifest__page_one):
    row = scrython.cards.Manifest().data[0]
    lookup = {row: "seen"}
    assert lookup[row] == "seen"


def test_catalog__id_less__same_instance_is_equal(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert catalog == catalog


def test_catalog__id_less__different_instances_not_equal(catalogs_creature_types):
    catalog_a = scrython.catalogs.CreatureTypes()
    catalog_b = scrython.catalogs.CreatureTypes()
    assert catalog_a != catalog_b
