"""Usage tests for catalog envelope behavior (ScryfallCatalogMixin)."""

import scrython.catalogs


def test_catalog__envelope__total_values_is_int(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert isinstance(catalog.total_values, int)


def test_catalog__envelope__data_yields_strings(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert len(catalog.data) > 0
    assert all(isinstance(item, str) for item in catalog.data)
