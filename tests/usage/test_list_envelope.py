"""Usage tests for list envelope behavior (ScryfallListMixin)."""

import scrython.rulings

# The rulings fixture is Rules Lawyer's; pass its id so the constructed call
# matches the payload being stubbed.
RULES_LAWYER_ID = "6c02c575-5685-44f5-8b47-89d888529d1b"


def test_list_envelope_has_more_is_bool(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert isinstance(rulings.has_more, bool)


def test_list_envelope_data_yields_usable_items(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert len(rulings.data) > 0
    assert rulings.data[0].comment != ""
