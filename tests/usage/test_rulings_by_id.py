"""Usage tests for scrython.rulings.ById."""

import scrython.rulings


def test_by_id_ruling_source(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id="bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd")
    assert rulings.data[0].source == "wotc"


def test_by_id_ruling_published_at(stub_response, load_fixture):
    stub_response("cards/id/rulings", load_fixture("rulings_by_id"))
    rulings = scrython.rulings.ById(id="bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd")
    assert rulings.data[0].published_at == "1993-10-04"
