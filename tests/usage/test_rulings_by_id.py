"""Usage tests for scrython.rulings.ById."""

import datetime

import scrython.rulings

RULES_LAWYER_ID = "6c02c575-5685-44f5-8b47-89d888529d1b"


def test_by_id__id__ruling_source(rulings_by_id__rules_lawyer):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    assert rulings.data[0].source == "wotc"


def test_by_id__id__ruling_published_at_is_iso_date(rulings_by_id__rules_lawyer):
    rulings = scrython.rulings.ById(id=RULES_LAWYER_ID)
    # published_at gets re-dated when WotC revises rulings text; assert shape, not value.
    datetime.date.fromisoformat(rulings.data[0].published_at)
