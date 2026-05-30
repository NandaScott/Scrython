"""Usage tests for scrython.cards.Named."""

import scrython.cards


def test_named_exact_returns_correct_name(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_named_black_lotus"))
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
