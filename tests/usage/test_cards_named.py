"""Usage tests for scrython.cards.Named."""

import scrython.cards


def test_named__exact__returns_correct_name(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
