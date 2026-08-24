"""Usage tests for the error Scryfall raises through the public API."""

import pytest

import scrython.cards
from scrython.base import ScryfallError


def test_named__exact__no_match__raises_scryfall_error(cards_named__not_found_error):
    with pytest.raises(ScryfallError):
        scrython.cards.Named(exact="Chandra Nalaar, Pyromaster")


def test_named__exact__no_match__error_carries_scryfall_fields(cards_named__not_found_error):
    with pytest.raises(ScryfallError) as raised:
        scrython.cards.Named(exact="Chandra Nalaar, Pyromaster")

    assert raised.value.status == 404
    assert raised.value.code == "not_found"
    assert raised.value.details.startswith("No cards found matching")
    assert raised.value.warnings == ["Did you mean Chandra Nalaar?"]
