"""Usage tests for list envelope behavior (ScryfallListMixin)."""

import scrython.rulings

# The rulings fixture is Tarmogoyf's; pass its id so the constructed call
# matches the payload being stubbed.
TARMOGOYF_ID = "69daba76-96e8-4bcc-ab79-2f00189ad8fb"


def test_list_envelope_has_more_is_bool(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id=TARMOGOYF_ID)
    assert isinstance(rulings.has_more, bool)


def test_list_envelope_data_yields_usable_items(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id=TARMOGOYF_ID)
    assert len(rulings.data) > 0
    assert rulings.data[0].comment != ""
