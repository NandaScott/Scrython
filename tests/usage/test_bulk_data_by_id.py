"""Usage tests for scrython.bulk_data.ById."""

import scrython.bulk_data


def test_by_id_returns_bulk_data_name(stub_response, load_fixture):
    stub_response("bulk-data/id", load_fixture("bulk_data_by_id"))
    bulk = scrython.bulk_data.ById(id="27bf3214-1271-490b-bdfe-c0be6c23d02e")
    assert bulk.name == "Oracle Cards"


def test_by_id_returns_bulk_data_type(stub_response, load_fixture):
    stub_response("bulk-data/id", load_fixture("bulk_data_by_id"))
    bulk = scrython.bulk_data.ById(id="27bf3214-1271-490b-bdfe-c0be6c23d02e")
    assert bulk.type == "oracle_cards"
