"""Usage tests for scrython.sets.ByCode."""

import scrython.sets


def test_by_code_returns_set_name(stub_response, load_fixture):
    stub_response("sets/code", load_fixture("sets_by_code_lea"))
    set_obj = scrython.sets.ByCode(code="lea")
    assert set_obj.name == "Limited Edition Alpha"


def test_by_code_returns_set_code(stub_response, load_fixture):
    stub_response("sets/code", load_fixture("sets_by_code_lea"))
    set_obj = scrython.sets.ByCode(code="lea")
    assert set_obj.code == "lea"
