"""Usage tests for card price-selection and image URL convenience methods."""

import scrython.cards


def test_named__exact__lowest_price__all_prices_present(cards_named__prices_mixed):
    card = scrython.cards.Named(exact="Prices Mixed Card")
    assert card.lowest_price() == 2.5


def test_named__exact__highest_price__all_prices_present(cards_named__prices_mixed):
    card = scrython.cards.Named(exact="Prices Mixed Card")
    assert card.highest_price() == 10.0


def test_named__exact__lowest_price__partial_null_prices(cards_named__prices_partial):
    card = scrython.cards.Named(exact="Prices Partial Card")
    assert card.lowest_price() == 7.0


def test_named__exact__highest_price__partial_null_prices(cards_named__prices_partial):
    card = scrython.cards.Named(exact="Prices Partial Card")
    assert card.highest_price() == 7.0


def test_named__exact__lowest_price__all_null_prices(cards_named__prices_all_null):
    card = scrython.cards.Named(exact="Prices All Null Card")
    assert card.lowest_price() is None


def test_named__exact__highest_price__all_null_prices(cards_named__prices_all_null):
    card = scrython.cards.Named(exact="Prices All Null Card")
    assert card.highest_price() is None


def test_named__exact__get_image_url__normal_card(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.get_image_url() is not None


def test_by_id__id__get_image_url__dfc_returns_front_face_url(cards_by_id__dfc_front_image):
    card_id, front_face_url = cards_by_id__dfc_front_image

    card = scrython.cards.ById(id=card_id)

    assert card.get_image_url() == front_face_url


def test_named__exact__get_image_url__no_image_returns_none(cards_named__image_none):
    card = scrython.cards.Named(exact="No Image Card")
    assert card.get_image_url() is None
