"""Usage tests for list envelope behavior (ScryfallListMixin)."""

import scrython.rulings

# The rulings fixture is Rules Lawyer's; pass its id so the constructed call
# matches the payload being stubbed.
RULES_LAWYER_ID = "6c02c575-5685-44f5-8b47-89d888529d1b"


def test_by_id__rulings__has_more_is_bool(rulings_by_id__rules_lawyer):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert isinstance(rulings.has_more, bool)


def test_by_id__rulings__data_yields_usable_items(rulings_by_id__rules_lawyer):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert len(rulings.data) > 0
    assert rulings.data[0].comment != ""
