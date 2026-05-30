"""Usage tests for scrython.symbology.All."""

import scrython.symbology


def test_all_returns_symbol(stub_response, load_fixture):
    stub_response("symbology", load_fixture("symbology_all"))
    symbols = scrython.symbology.All()
    assert symbols.data[0].symbol == "{W}"


def test_all_returns_symbol_english(stub_response, load_fixture):
    stub_response("symbology", load_fixture("symbology_all"))
    symbols = scrython.symbology.All()
    assert symbols.data[0].english == "one white mana"
