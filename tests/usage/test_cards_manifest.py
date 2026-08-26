"""Usage tests for scrython.cards.Manifest."""

import scrython.cards


def test_manifest__cards__yields_thin_card_names(cards_manifest__page_one):
    captured_row, doctored_row = cards_manifest__page_one
    manifest = scrython.cards.Manifest()
    assert [card.name for card in manifest] == [captured_row["name"], doctored_row["name"]]


def test_manifest__cards__exposes_thin_core_fields(cards_manifest__page_one):
    captured_row, _ = cards_manifest__page_one
    card = scrython.cards.Manifest().data[0]
    assert (card.card_id, card.lang) == (captured_row["id"], captured_row["lang"])


def test_manifest__cards__exposes_thin_print_fields(cards_manifest__page_one):
    captured_row, _ = cards_manifest__page_one
    card = scrython.cards.Manifest().data[0]
    assert (card.collector_number, card.image_updated_at) == (
        captured_row["collector_number"],
        captured_row["image_updated_at"],
    )


def test_manifest__cards__exposes_manifest_only_fields(cards_manifest__page_one):
    _, doctored_row = cards_manifest__page_one
    card = scrython.cards.Manifest().data[1]
    assert (card.set_code, card.oracle_id, card.created_at, card.data_updated_at) == (
        doctored_row["set_code"],
        doctored_row["oracle_id"],
        doctored_row["created_at"],
        doctored_row["data_updated_at"],
    )


# Hardcoded rather than read off the payload on purpose: Scryfall sends these
# three as null on every manifest row today, and this test is what says so out
# loud. If a fixture refresh reddens it, Scryfall started populating them and the
# doctored row in conftest is no longer needed to reach these accessors.
def test_manifest__cards__nullable_fields_are_none(cards_manifest__page_one):
    card = scrython.cards.Manifest().data[0]
    assert (card.oracle_id, card.created_at, card.data_updated_at) == (None, None, None)


def test_manifest__cards__omits_full_card_accessors(cards_manifest__page_one):
    manifest = scrython.cards.Manifest()
    assert not hasattr(manifest.data[0], "type_line")
