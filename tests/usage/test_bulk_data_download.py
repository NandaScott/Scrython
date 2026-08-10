"""Usage tests for scrython.bulk_data download."""

import scrython.bulk_data


def test_by_id__download__returns_dataset(bulk_data_by_id__oracle_cards_download):
    bulk = scrython.bulk_data.ById(id="27bf3214-1271-490b-bdfe-c0be6c23d02e")
    result = bulk.download()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(card["name"] == "Black Lotus" for card in result)
