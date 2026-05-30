"""Usage tests for scrython.symbology.All."""

import scrython.symbology


def test_all_includes_white_mana_symbol(stub_response, load_fixture):
    stub_response("symbology", load_fixture("symbology_all"))
    symbols = scrython.symbology.All()
    assert "{W}" in {symbol.symbol for symbol in symbols.data}


def test_white_mana_symbol_has_english_gloss(stub_response, load_fixture):
    stub_response("symbology", load_fixture("symbology_all"))
    symbols = scrython.symbology.All()
    white = next(symbol for symbol in symbols.data if symbol.symbol == "{W}")
    assert white.english == "one white mana"
