"""Usage tests for scrython.symbology.All."""

import scrython.symbology


def test_all__symbols__includes_white_mana(symbology_all):
    symbols = scrython.symbology.All()
    assert "{W}" in {symbol.symbol for symbol in symbols.data}


def test_all__symbols__white_mana_has_english_gloss(symbology_all):
    symbols = scrython.symbology.All()
    white = next(symbol for symbol in symbols.data if symbol.symbol == "{W}")
    assert white.english == "one white mana"
