"""Usage tests for scrython.rulings.ById."""

import datetime

import scrython.rulings

TARMOGOYF_ID = "69daba76-96e8-4bcc-ab79-2f00189ad8fb"


def test_by_id_ruling_source(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id=TARMOGOYF_ID)
    assert rulings.data[0].source == "wotc"


def test_by_id_ruling_published_at_is_iso_date(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id=TARMOGOYF_ID)
    # published_at gets re-dated when WotC revises rulings text; assert shape, not value.
    datetime.date.fromisoformat(rulings.data[0].published_at)
