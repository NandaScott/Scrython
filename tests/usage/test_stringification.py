"""Usage tests for __str__ and __repr__ of Scrython objects."""

import scrython.cards
import scrython.catalogs
import scrython.rulings
import scrython.sets

RULES_LAWYER_ID = "6c02c575-5685-44f5-8b47-89d888529d1b"


def test_card__str__name_set_format(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert str(card) == "Black Lotus (VMA)"


def test_card__repr__class_id_name_format(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    r = repr(card)
    assert "Named" in r
    assert "id=" in r
    assert "Black Lotus" in r


def test_set__str__name_code_format(sets_by_code__lea):
    s = scrython.sets.ByCode(code="lea")
    assert str(s) == "Limited Edition Alpha (LEA)"


def test_set__repr__class_id_name_format(sets_by_code__lea):
    s = scrython.sets.ByCode(code="lea")
    r = repr(s)
    assert "ByCode" in r
    assert "id=" in r
    assert "Limited Edition Alpha" in r


def test_list__str__list_count_format(stub_response):
    stub_response(
        "cards/id/rulings",
        {"object": "list", "has_more": False, "data": [], "total_cards": 5},
    )
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert str(rulings) == "List with 5 items"


def test_list__repr__class_name_format(rulings_by_id__rules_lawyer):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert "ById" in repr(rulings)


def test_catalog__str__catalog_count_format(stub_response):
    stub_response(
        "catalog/creature-types",
        {
            "object": "catalog",
            "uri": "https://api.scryfall.com/catalog/creature-types",
            "total_values": 3,
            "data": ["Advisor", "Aetherborn", "Alien"],
        },
    )
    catalog = scrython.catalogs.CreatureTypes()
    assert str(catalog) == "Catalog with 3 items"


def test_catalog__repr__class_name_format(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert "CreatureTypes" in repr(catalog)
