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


def test_by_id__rulings__is_directly_iterable(rulings_by_id__rules_lawyer):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    items = list(rulings)
    assert len(items) > 0
    assert all(item.comment != "" for item in items)


def test_by_id__rulings__iter_all_yields_items_across_pages(rulings_multipage):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    items = list(rulings.iter_all())
    assert len(items) == 2
    assert items[0].comment == "Page one ruling."
    assert items[1].comment == "Page two ruling."
