"""Usage tests for scrython.catalogs.CreatureTypes."""

import scrython.catalogs


def test_creature_types__all__contains_known_type(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert "Angel" in catalog.data


def test_creature_types__all__total_values_matches_data_length(catalogs_creature_types):
    catalog = scrython.catalogs.CreatureTypes()
    assert catalog.total_values == len(catalog.data)
