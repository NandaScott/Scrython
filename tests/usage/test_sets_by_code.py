"""Usage tests for scrython.sets.ByCode."""

import scrython.sets


def test_by_code__code__returns_set_name(sets_by_code__lea):
    set_obj = scrython.sets.ByCode(code="lea")
    assert set_obj.name == "Limited Edition Alpha"


def test_by_code__code__returns_set_code(sets_by_code__lea):
    set_obj = scrython.sets.ByCode(code="lea")
    assert set_obj.code == "lea"
