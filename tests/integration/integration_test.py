#!/usr/bin/env python3
"""
Scrython Integration Test Suite

This script performs live API integration tests against the Scryfall API
to verify the package works correctly in production conditions.

Unlike the unit tests in tests/, this script:
- Makes REAL HTTP calls to Scryfall's API
- Verifies actual response parsing works
- Detects API drift or breaking changes
- Tests the full request/response cycle

Usage:
    python tests/integration/integration_test.py

    Or via pytest (excluded from normal test runs):
    pytest tests/integration/ -v

Note: This script makes real API calls to Scryfall.
      Please respect their rate limits by not running this script excessively.
      Recommended: Run only before releases or when verifying API compatibility.
"""

import sys
import time
from collections.abc import Callable
from typing import Any

# Test configuration
RATE_LIMIT_DELAY = 0.1  # 100ms between API calls to respect Scryfall rate limits
VERBOSE = True  # Set to False for less output


class TestResults:
    """Tracks test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []

    def record_pass(self, test_name: str):
        self.passed += 1
        if VERBOSE:
            print(f"  ✓ {test_name}")

    def record_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  ✗ {test_name}: {error}")

    def record_skip(self, test_name: str, reason: str):
        self.skipped += 1
        if VERBOSE:
            print(f"  - {test_name}: SKIPPED ({reason})")

    def summary(self):
        total = self.passed + self.failed + self.skipped
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total:   {total}")
        print(f"Passed:  {self.passed}")
        print(f"Failed:  {self.failed}")
        print(f"Skipped: {self.skipped}")

        if self.errors:
            print("\nFailed Tests:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")

        return self.failed == 0


results = TestResults()


def delay():
    """Respect Scryfall rate limits."""
    time.sleep(RATE_LIMIT_DELAY)


def run_test(test_name: str, test_func: Callable[[], Any], skip_reason: str = None):
    """Run a single test and record results."""
    if skip_reason:
        results.record_skip(test_name, skip_reason)
        return None

    try:
        result = test_func()
        results.record_pass(test_name)
        delay()
        return result
    except Exception as exc:
        results.record_fail(test_name, str(exc))
        delay()
        return None


def test_import():
    """Test that scrython can be imported."""
    print("\n" + "=" * 60)
    print("TESTING: Package Import")
    print("=" * 60)

    try:
        import scrython

        results.record_pass("import scrython")
        return scrython
    except ImportError as exc:
        results.record_fail("import scrython", str(exc))
        return None


def test_cards_module(scrython):
    """Test the scrython.cards module."""
    print("\n" + "=" * 60)
    print("TESTING: scrython.cards")
    print("=" * 60)

    # Test Named (fuzzy)
    card = run_test(
        "cards.Named(fuzzy='lightning bolt')", lambda: scrython.cards.Named(fuzzy="lightning bolt")
    )

    if card:
        # Test card properties
        run_test("card.name", lambda: card.name)
        run_test("card.mana_cost", lambda: card.mana_cost)
        run_test("card.cmc", lambda: card.cmc)
        run_test("card.type_line", lambda: card.type_line)
        run_test("card.oracle_text", lambda: card.oracle_text)
        run_test("card.colors", lambda: card.colors)
        run_test("card.color_identity", lambda: card.color_identity)
        run_test("card.legalities", lambda: card.legalities)
        run_test("card.set", lambda: card.set)
        run_test("card.set_name", lambda: card.set_name)
        run_test("card.rarity", lambda: card.rarity)
        run_test("card.prices", lambda: card.prices)
        run_test("card.image_uris", lambda: card.image_uris)
        run_test("card.card_id", lambda: card.card_id)
        run_test("card.oracle_id", lambda: card.oracle_id)

        # Test card methods
        run_test("card.is_legal_in('modern')", lambda: card.is_legal_in("modern"))
        run_test("card.has_color('R')", lambda: card.has_color("R"))
        run_test("card.is_instant", lambda: card.is_instant)
        run_test("card.is_creature", lambda: card.is_creature)
        run_test("card.is_sorcery", lambda: card.is_sorcery)
        run_test("card.to_dict()", lambda: card.to_dict())
        run_test("card.to_json()", lambda: card.to_json())
        run_test("card.lowest_price()", lambda: card.lowest_price())
        run_test("card.highest_price()", lambda: card.highest_price())
        run_test("card.get_image_url('normal')", lambda: card.get_image_url("normal"))

    # Test Named (exact)
    run_test("cards.Named(exact='Black Lotus')", lambda: scrython.cards.Named(exact="Black Lotus"))

    # Test creature card properties
    creature = run_test(
        "cards.Named(exact='Tarmogoyf')", lambda: scrython.cards.Named(exact="Tarmogoyf")
    )

    if creature:
        run_test("creature.power", lambda: creature.power)
        run_test("creature.toughness", lambda: creature.toughness)
        run_test("creature.is_creature", lambda: creature.is_creature)
        run_test("creature.keywords", lambda: creature.keywords)

    # Test double-faced card
    dfc = run_test(
        "cards.Named(exact='Delver of Secrets')",
        lambda: scrython.cards.Named(exact="Delver of Secrets"),
    )

    if dfc:
        run_test("dfc.layout", lambda: dfc.layout)
        run_test("dfc.card_faces", lambda: dfc.card_faces)

    # Test Search
    search_results = run_test(
        "cards.Search(q='c:blue type:instant cmc=1')",
        lambda: scrython.cards.Search(q="c:blue type:instant cmc=1"),
    )

    if search_results:
        run_test("search.data", lambda: search_results.data)
        run_test("search.total_cards", lambda: search_results.total_cards)
        run_test("search.has_more", lambda: search_results.has_more)
        run_test("len(search)", lambda: len(search_results))
        run_test(
            "search.data[0]", lambda: search_results.data[0] if len(search_results) > 0 else None
        )
        run_test("search.to_list()", lambda: search_results.to_list())
        run_test("iteration via for loop", lambda: list(search_results)[:3])
        run_test("search.filter()", lambda: search_results.filter(lambda c: c.cmc > 0))
        run_test("search.map()", lambda: search_results.map(lambda c: c.name))
        run_test("search.as_dict('name')", lambda: search_results.as_dict("name"))

    # Test Autocomplete
    autocomplete = run_test(
        "cards.Autocomplete(q='light')", lambda: scrython.cards.Autocomplete(q="light")
    )

    if autocomplete:
        run_test("autocomplete.data", lambda: autocomplete.data)
        run_test("autocomplete.total_values", lambda: autocomplete.total_values)

    # Test Random
    random_card = run_test("cards.Random()", lambda: scrython.cards.Random())

    if random_card:
        run_test("random_card.name", lambda: random_card.name)

    # Test Random with query
    run_test("cards.Random(q='type:creature')", lambda: scrython.cards.Random(q="type:creature"))

    # Test ByCodeNumber
    card_by_code = run_test(
        "cards.ByCodeNumber(code='m21', number='1')",
        lambda: scrython.cards.ByCodeNumber(code="m21", number="1"),
    )

    if card_by_code:
        run_test("card_by_code.name", lambda: card_by_code.name)
        run_test("card_by_code.collector_number", lambda: card_by_code.collector_number)

    # Test ByCodeNumber with language
    run_test(
        "cards.ByCodeNumber(code='m21', number='1', lang='ja')",
        lambda: scrython.cards.ByCodeNumber(code="m21", number="1", lang="ja"),
    )

    # Test ByMultiverseId
    run_test("cards.ByMultiverseId(id=489712)", lambda: scrython.cards.ByMultiverseId(id=489712))

    # Test ById (UUID)
    run_test(
        "cards.ById(id='bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd')",
        lambda: scrython.cards.ById(id="bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd"),
    )

    # Test ByArenaId
    run_test("cards.ByArenaId(id=67330)", lambda: scrython.cards.ByArenaId(id=67330))

    # Test ByTCGPlayerId (using a known valid ID)
    run_test("cards.ByTCGPlayerId(id=534658)", lambda: scrython.cards.ByTCGPlayerId(id=534658))

    # Test Collection (POST endpoint)
    collection = run_test(
        "cards.Collection(data={'identifiers': [...]})",
        lambda: scrython.cards.Collection(
            data={
                "identifiers": [
                    {"name": "Lightning Bolt"},
                    {"name": "Counterspell"},
                    {"set": "m21", "collector_number": "1"},
                ]
            }
        ),
    )

    if collection:
        run_test("collection.data", lambda: collection.data)
        run_test("len(collection)", lambda: len(collection))


def test_sets_module(scrython):
    """Test the scrython.sets module."""
    print("\n" + "=" * 60)
    print("TESTING: scrython.sets")
    print("=" * 60)

    # Test All
    all_sets = run_test("sets.All()", lambda: scrython.sets.All())

    if all_sets:
        run_test("all_sets.data", lambda: all_sets.data)
        run_test("len(all_sets)", lambda: len(all_sets))

        if len(all_sets) > 0:
            first_set = all_sets.data[0]
            run_test("set.name", lambda: first_set.name)
            run_test("set.code", lambda: first_set.code)
            run_test("set.set_type", lambda: first_set.set_type)
            run_test("set.card_count", lambda: first_set.card_count)
            run_test("set.released_at", lambda: first_set.released_at)
            run_test("set.icon_svg_uri", lambda: first_set.icon_svg_uri)

    # Test ByCode
    set_by_code = run_test("sets.ByCode(code='m21')", lambda: scrython.sets.ByCode(code="m21"))

    if set_by_code:
        run_test("set_by_code.name", lambda: set_by_code.name)
        run_test("set_by_code.code", lambda: set_by_code.code)
        run_test("set_by_code.card_count", lambda: set_by_code.card_count)
        run_test("set_by_code.to_dict()", lambda: set_by_code.to_dict())
        run_test("set_by_code.id", lambda: set_by_code.id)
        run_test("set_by_code.scryfall_uri", lambda: set_by_code.scryfall_uri)

    # Test ById (UUID)
    run_test(
        "sets.ById(id='a4a0db50-8826-4e73-833c-3fd934375f96')",
        lambda: scrython.sets.ById(id="a4a0db50-8826-4e73-833c-3fd934375f96"),
    )


def test_bulk_data_module(scrython):
    """Test the scrython.bulk_data module."""
    print("\n" + "=" * 60)
    print("TESTING: scrython.bulk_data")
    print("=" * 60)

    # Test All
    all_bulk = run_test("bulk_data.All()", lambda: scrython.bulk_data.All())

    if all_bulk:
        run_test("all_bulk.data", lambda: all_bulk.data)
        run_test("len(all_bulk)", lambda: len(all_bulk))

        if len(all_bulk) > 0:
            first_bulk = all_bulk.data[0]
            run_test("bulk.name", lambda: first_bulk.name)
            run_test("bulk.type", lambda: first_bulk.type)
            run_test("bulk.download_uri", lambda: first_bulk.download_uri)
            run_test("bulk.size", lambda: first_bulk.size)
            run_test("bulk.updated_at", lambda: first_bulk.updated_at)

    # Test ByType
    bulk_by_type = run_test(
        "bulk_data.ByType(type='rulings')", lambda: scrython.bulk_data.ByType(type="rulings")
    )

    if bulk_by_type:
        run_test("bulk_by_type.name", lambda: bulk_by_type.name)
        run_test("bulk_by_type.download_uri", lambda: bulk_by_type.download_uri)
        # Note: Not testing download() as it would download large files


def test_rulings_module(scrython):
    """Test the scrython.rulings module."""
    print("\n" + "=" * 60)
    print("TESTING: scrython.rulings")
    print("=" * 60)

    # Test ByCodeNumber - use a card with known rulings (Lightning Bolt has many)
    rulings = run_test(
        "rulings.ByCodeNumber(code='lea', number='161')",
        lambda: scrython.rulings.ByCodeNumber(code="lea", number="161"),
    )

    if rulings:
        run_test("rulings.data", lambda: rulings.data)
        run_test("len(rulings)", lambda: len(rulings))

        if len(rulings) > 0:
            first_ruling = rulings.data[0]
            run_test("ruling.comment", lambda: first_ruling.comment)
            run_test("ruling.source", lambda: first_ruling.source)
            run_test("ruling.published_at", lambda: first_ruling.published_at)

    # Test Rulings factory with multiverse_id
    rulings_factory = run_test(
        "rulings.Rulings(code='m21', number='1')",
        lambda: scrython.rulings.Rulings(code="m21", number="1"),
    )

    if rulings_factory:
        run_test("rulings_factory.data", lambda: rulings_factory.data)


def test_catalogs_module(scrython):
    """Test the scrython.catalogs module."""
    print("\n" + "=" * 60)
    print("TESTING: scrython.catalogs")
    print("=" * 60)

    # Test CreatureTypes
    creature_types = run_test("catalogs.CreatureTypes()", lambda: scrython.catalogs.CreatureTypes())

    if creature_types:
        run_test("creature_types.data", lambda: creature_types.data)
        run_test("creature_types.total_values", lambda: creature_types.total_values)
        run_test("'Elf' in creature_types.data", lambda: "Elf" in creature_types.data)

    # Test CardNames (large catalog, just verify it works)
    card_names = run_test("catalogs.CardNames()", lambda: scrython.catalogs.CardNames())

    if card_names:
        run_test("card_names.total_values > 0", lambda: card_names.total_values > 0)

    # Test KeywordAbilities
    keywords = run_test("catalogs.KeywordAbilities()", lambda: scrython.catalogs.KeywordAbilities())

    if keywords:
        run_test("'Flying' in keywords.data", lambda: "Flying" in keywords.data)
        run_test("'Trample' in keywords.data", lambda: "Trample" in keywords.data)

    # Test LandTypes
    land_types = run_test("catalogs.LandTypes()", lambda: scrython.catalogs.LandTypes())

    if land_types:
        run_test("'Plains' in land_types.data", lambda: "Plains" in land_types.data)

    # Test Supertypes
    supertypes = run_test("catalogs.Supertypes()", lambda: scrython.catalogs.Supertypes())

    if supertypes:
        run_test("'Legendary' in supertypes.data", lambda: "Legendary" in supertypes.data)

    # Test CardTypes
    card_types = run_test("catalogs.CardTypes()", lambda: scrython.catalogs.CardTypes())

    if card_types:
        run_test("'Creature' in card_types.data", lambda: "Creature" in card_types.data)

    # Test ArtifactTypes
    run_test("catalogs.ArtifactTypes()", lambda: scrython.catalogs.ArtifactTypes())

    # Test EnchantmentTypes
    run_test("catalogs.EnchantmentTypes()", lambda: scrython.catalogs.EnchantmentTypes())

    # Test SpellTypes
    run_test("catalogs.SpellTypes()", lambda: scrython.catalogs.SpellTypes())

    # Test PlaneswalkerTypes
    run_test("catalogs.PlaneswalkerTypes()", lambda: scrython.catalogs.PlaneswalkerTypes())

    # Test Powers
    run_test("catalogs.Powers()", lambda: scrython.catalogs.Powers())

    # Test Toughnesses
    run_test("catalogs.Toughnesses()", lambda: scrython.catalogs.Toughnesses())

    # Test Loyalties
    run_test("catalogs.Loyalties()", lambda: scrython.catalogs.Loyalties())

    # Test Watermarks
    run_test("catalogs.Watermarks()", lambda: scrython.catalogs.Watermarks())

    # Test ArtistNames
    run_test("catalogs.ArtistNames()", lambda: scrython.catalogs.ArtistNames())

    # Test KeywordActions
    run_test("catalogs.KeywordActions()", lambda: scrython.catalogs.KeywordActions())

    # Test AbilityWords
    run_test("catalogs.AbilityWords()", lambda: scrython.catalogs.AbilityWords())

    # Test FlavorWords
    run_test("catalogs.FlavorWords()", lambda: scrython.catalogs.FlavorWords())

    # Test WordBank
    run_test("catalogs.WordBank()", lambda: scrython.catalogs.WordBank())

    # Test BattleTypes
    run_test("catalogs.BattleTypes()", lambda: scrython.catalogs.BattleTypes())

    # Test Catalogs factory
    catalog_factory = run_test(
        "catalogs.Catalogs('creature-types')", lambda: scrython.catalogs.Catalogs("creature-types")
    )

    if catalog_factory:
        run_test("catalog_factory.data", lambda: catalog_factory.data)


def test_symbology_module(scrython):
    """Test the scrython.symbology module."""
    print("\n" + "=" * 60)
    print("TESTING: scrython.symbology")
    print("=" * 60)

    # Test All
    all_symbols = run_test("symbology.All()", lambda: scrython.symbology.All())

    if all_symbols:
        run_test("all_symbols.data", lambda: all_symbols.data)
        run_test("len(all_symbols)", lambda: len(all_symbols))

        if len(all_symbols) > 0:
            first_symbol = all_symbols.data[0]
            run_test("symbol.symbol", lambda: first_symbol.symbol)
            run_test("symbol.english", lambda: first_symbol.english)
            run_test("symbol.represents_mana", lambda: first_symbol.represents_mana)
            run_test("symbol.svg_uri", lambda: first_symbol.svg_uri)

    # Test ParseMana
    parsed_mana = run_test(
        "symbology.ParseMana(cost='{2}{U}{U}')",
        lambda: scrython.symbology.ParseMana(cost="{2}{U}{U}"),
    )

    if parsed_mana:
        run_test("parsed_mana.cost", lambda: parsed_mana.cost)
        run_test("parsed_mana.mana_value", lambda: parsed_mana.mana_value)
        run_test("parsed_mana.colors", lambda: parsed_mana.colors)
        run_test("parsed_mana.colorless", lambda: parsed_mana.colorless)
        run_test("parsed_mana.monocolored", lambda: parsed_mana.monocolored)
        run_test("parsed_mana.multicolored", lambda: parsed_mana.multicolored)

    # Test Symbology factory
    run_test(
        "symbology.Symbology(cost='{W}{U}{B}{R}{G}')",
        lambda: scrython.symbology.Symbology(cost="{W}{U}{B}{R}{G}"),
    )


def test_error_handling(scrython):
    """Test error handling for invalid requests."""
    print("\n" + "=" * 60)
    print("TESTING: Error Handling")
    print("=" * 60)

    from scrython.base import ScryfallError

    # Test invalid card name
    def test_invalid_named():
        try:
            scrython.cards.Named(exact="xyznotarealcard12345")
            return False  # Should have raised an error
        except ScryfallError as exc:
            return exc.status == 404
        except Exception:
            return False

    run_test("ScryfallError on invalid card name", test_invalid_named)

    # Test invalid set code
    def test_invalid_set():
        try:
            scrython.sets.ByCode(code="xyznotarealset")
            return False
        except ScryfallError as exc:
            return exc.status == 404
        except Exception:
            return False

    run_test("ScryfallError on invalid set code", test_invalid_set)


def test_utility_methods(scrython):
    """Test utility methods like from_dict and Object construction."""
    print("\n" + "=" * 60)
    print("TESTING: Utility Methods")
    print("=" * 60)

    # Test from_dict
    card_data = {
        "object": "card",
        "name": "Test Card",
        "mana_cost": "{1}{R}",
        "cmc": 2.0,
        "type_line": "Instant",
        "oracle_text": "Test oracle text",
        "colors": ["R"],
        "color_identity": ["R"],
        "legalities": {"standard": "not_legal", "modern": "legal"},
        "set": "test",
        "set_name": "Test Set",
        "rarity": "common",
        "prices": {"usd": "0.10"},
    }

    def test_from_dict():
        card_obj = scrython.cards.Object.from_dict(card_data)
        return card_obj.name == "Test Card" and card_obj.cmc == 2.0

    run_test("cards.Object.from_dict()", test_from_dict)


def main():
    """Run all tests."""
    print("=" * 60)
    print("SCRYTHON PACKAGE TEST SUITE")
    print("=" * 60)
    print("\nThis script tests all modules and methods of the Scrython package.")
    print("Note: Real API calls are made to Scryfall. Please be patient.")
    print(f"Rate limiting: {int(RATE_LIMIT_DELAY * 1000)}ms delay between requests.\n")

    # Test import
    scrython = test_import()
    if scrython is None:
        print("\nFATAL: Could not import scrython. Aborting tests.")
        sys.exit(1)

    # Run all module tests
    test_cards_module(scrython)
    test_sets_module(scrython)
    test_bulk_data_module(scrython)
    test_rulings_module(scrython)
    test_catalogs_module(scrython)
    test_symbology_module(scrython)
    test_error_handling(scrython)
    test_utility_methods(scrython)

    # Print summary
    success = results.summary()

    print("\n" + "=" * 60)
    if success:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED - See details above")
    print("=" * 60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
