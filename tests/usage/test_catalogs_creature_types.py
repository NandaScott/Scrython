"""Usage tests for scrython.catalogs.CreatureTypes."""

import scrython.catalogs


def test_creature_types_returns_data(stub_response, load_fixture):
    stub_response("catalog/creature-types", load_fixture("catalogs_creature_types"))
    catalog = scrython.catalogs.CreatureTypes()
    assert "Angel" in catalog.data


def test_creature_types_total_values_matches_data_length(stub_response, load_fixture):
    stub_response("catalog/creature-types", load_fixture("catalogs_creature_types"))
    catalog = scrython.catalogs.CreatureTypes()
    assert catalog.total_values == len(catalog.data)
