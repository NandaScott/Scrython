"""Usage tests for catalog envelope behavior (ScryfallCatalogMixin)."""

import scrython.catalogs


def test_catalog_envelope_total_values_is_int(stub_response, load_fixture):
    stub_response("catalog/creature-types", load_fixture("catalogs_creature_types"))
    catalog = scrython.catalogs.CreatureTypes()
    assert isinstance(catalog.total_values, int)


def test_catalog_envelope_data_yields_strings(stub_response, load_fixture):
    stub_response("catalog/creature-types", load_fixture("catalogs_creature_types"))
    catalog = scrython.catalogs.CreatureTypes()
    assert len(catalog.data) > 0
    assert all(isinstance(item, str) for item in catalog.data)
