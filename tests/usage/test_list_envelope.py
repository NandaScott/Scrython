"""Usage tests for list envelope behavior (ScryfallListMixin)."""

import scrython.rulings


def test_list_envelope_has_more_is_bool(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id="bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd")
    assert isinstance(rulings.has_more, bool)


def test_list_envelope_data_yields_usable_items(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id="bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd")
    assert len(rulings.data) > 0
    assert rulings.data[0].comment != ""
