"""Tests for scrython.catalogs module."""

import pytest

from scrython.catalogs import (
    AbilityWords,
    ArtifactTypes,
    ArtistNames,
    BattleTypes,
    CardNames,
    CardTypes,
    Catalogs,
    CreatureTypes,
    EnchantmentTypes,
    FlavorWords,
    KeywordAbilities,
    KeywordActions,
    LandTypes,
    Loyalties,
    PlaneswalkerTypes,
    Powers,
    SpellTypes,
    Supertypes,
    Toughnesses,
    Watermarks,
    WordBank,
)


class TestCardNames:
    """Test CardNames endpoint."""

    def test_get_card_names(self, mock_urlopen):
        """Test getting all card names."""
        mock_urlopen.set_response("catalogs/card_names.json")
        catalog = CardNames()

        assert catalog.object == "catalog"
        assert catalog.total_values == 5
        assert len(catalog.data) == 5
        assert "Black Lotus" in catalog.data

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/card_names.json")
        _catalog = CardNames()

        assert "api.scryfall.com/catalog/card-names" in mock_urlopen.calls[0]["url"]


class TestCreatureTypes:
    """Test CreatureTypes endpoint."""

    def test_get_creature_types(self, mock_urlopen):
        """Test getting all creature types."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = CreatureTypes()

        assert catalog.object == "catalog"
        assert catalog.total_values == 6
        assert "Elf" in catalog.data
        assert "Dragon" in catalog.data

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = CreatureTypes()

        assert "api.scryfall.com/catalog/creature-types" in mock_urlopen.calls[0]["url"]


class TestPlaneswalkerTypes:
    """Test PlaneswalkerTypes endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = PlaneswalkerTypes()

        assert "api.scryfall.com/catalog/planeswalker-types" in mock_urlopen.calls[0]["url"]


class TestCardTypes:
    """Test CardTypes endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = CardTypes()

        assert "api.scryfall.com/catalog/card-types" in mock_urlopen.calls[0]["url"]


class TestKeywordAbilities:
    """Test KeywordAbilities endpoint."""

    def test_get_keyword_abilities(self, mock_urlopen):
        """Test getting all keyword abilities."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        catalog = KeywordAbilities()

        assert catalog.object == "catalog"
        assert catalog.total_values == 4
        assert "Flying" in catalog.data
        assert "Trample" in catalog.data

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        _catalog = KeywordAbilities()

        assert "api.scryfall.com/catalog/keyword-abilities" in mock_urlopen.calls[0]["url"]


class TestKeywordActions:
    """Test KeywordActions endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        _catalog = KeywordActions()

        assert "api.scryfall.com/catalog/keyword-actions" in mock_urlopen.calls[0]["url"]


class TestArtifactTypes:
    """Test ArtifactTypes endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = ArtifactTypes()

        assert "api.scryfall.com/catalog/artifact-types" in mock_urlopen.calls[0]["url"]


class TestEnchantmentTypes:
    """Test EnchantmentTypes endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = EnchantmentTypes()

        assert "api.scryfall.com/catalog/enchantment-types" in mock_urlopen.calls[0]["url"]


class TestLandTypes:
    """Test LandTypes endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = LandTypes()

        assert "api.scryfall.com/catalog/land-types" in mock_urlopen.calls[0]["url"]


class TestSpellTypes:
    """Test SpellTypes endpoint."""

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        _catalog = SpellTypes()

        assert "api.scryfall.com/catalog/spell-types" in mock_urlopen.calls[0]["url"]


class TestCatalogsMixin:
    """Test catalog data accessor methods."""

    def test_catalog_properties(self, mock_urlopen):
        """Test that catalog properties are accessible."""
        mock_urlopen.set_response("catalogs/card_names.json")
        catalog = CardNames()

        assert catalog.object == "catalog"
        assert catalog.uri == "https://api.scryfall.com/catalog/card-names"
        assert catalog.total_values == 5
        assert isinstance(catalog.data, list)
        assert len(catalog.data) == 5

    def test_data_content(self, mock_urlopen):
        """Test that catalog data contains expected values."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = CreatureTypes()

        assert "Elf" in catalog.data
        assert "Goblin" in catalog.data
        assert "Human" in catalog.data


class TestCatalogsFactory:
    """Test Catalogs smart factory."""

    def test_factory_routes_to_card_names(self, mock_urlopen):
        """Test that factory routes to CardNames."""
        mock_urlopen.set_response("catalogs/card_names.json")
        catalog = Catalogs("card-names")

        assert isinstance(catalog, CardNames)
        assert "api.scryfall.com/catalog/card-names" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_creature_types(self, mock_urlopen):
        """Test that factory routes to CreatureTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("creature-types")

        assert isinstance(catalog, CreatureTypes)
        assert "api.scryfall.com/catalog/creature-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_planeswalker_types(self, mock_urlopen):
        """Test that factory routes to PlaneswalkerTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("planeswalker-types")

        assert isinstance(catalog, PlaneswalkerTypes)
        assert "api.scryfall.com/catalog/planeswalker-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_card_types(self, mock_urlopen):
        """Test that factory routes to CardTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("card-types")

        assert isinstance(catalog, CardTypes)
        assert "api.scryfall.com/catalog/card-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_keyword_abilities(self, mock_urlopen):
        """Test that factory routes to KeywordAbilities."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        catalog = Catalogs("keyword-abilities")

        assert isinstance(catalog, KeywordAbilities)
        assert "api.scryfall.com/catalog/keyword-abilities" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_keyword_actions(self, mock_urlopen):
        """Test that factory routes to KeywordActions."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        catalog = Catalogs("keyword-actions")

        assert isinstance(catalog, KeywordActions)
        assert "api.scryfall.com/catalog/keyword-actions" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_artifact_types(self, mock_urlopen):
        """Test that factory routes to ArtifactTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("artifact-types")

        assert isinstance(catalog, ArtifactTypes)
        assert "api.scryfall.com/catalog/artifact-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_enchantment_types(self, mock_urlopen):
        """Test that factory routes to EnchantmentTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("enchantment-types")

        assert isinstance(catalog, EnchantmentTypes)
        assert "api.scryfall.com/catalog/enchantment-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_land_types(self, mock_urlopen):
        """Test that factory routes to LandTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("land-types")

        assert isinstance(catalog, LandTypes)
        assert "api.scryfall.com/catalog/land-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_spell_types(self, mock_urlopen):
        """Test that factory routes to SpellTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("spell-types")

        assert isinstance(catalog, SpellTypes)
        assert "api.scryfall.com/catalog/spell-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_artist_names(self, mock_urlopen):
        """Test that factory routes to ArtistNames."""
        mock_urlopen.set_response("catalogs/card_names.json")
        catalog = Catalogs("artist-names")

        assert isinstance(catalog, ArtistNames)
        assert "api.scryfall.com/catalog/artist-names" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_word_bank(self, mock_urlopen):
        """Test that factory routes to WordBank."""
        mock_urlopen.set_response("catalogs/card_names.json")
        catalog = Catalogs("word-bank")

        assert isinstance(catalog, WordBank)
        assert "api.scryfall.com/catalog/word-bank" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_supertypes(self, mock_urlopen):
        """Test that factory routes to Supertypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("supertypes")

        assert isinstance(catalog, Supertypes)
        assert "api.scryfall.com/catalog/supertypes" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_battle_types(self, mock_urlopen):
        """Test that factory routes to BattleTypes."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("battle-types")

        assert isinstance(catalog, BattleTypes)
        assert "api.scryfall.com/catalog/battle-types" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_powers(self, mock_urlopen):
        """Test that factory routes to Powers."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("powers")

        assert isinstance(catalog, Powers)
        assert "api.scryfall.com/catalog/powers" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_toughnesses(self, mock_urlopen):
        """Test that factory routes to Toughnesses."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("toughnesses")

        assert isinstance(catalog, Toughnesses)
        assert "api.scryfall.com/catalog/toughnesses" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_loyalties(self, mock_urlopen):
        """Test that factory routes to Loyalties."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("loyalties")

        assert isinstance(catalog, Loyalties)
        assert "api.scryfall.com/catalog/loyalties" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_watermarks(self, mock_urlopen):
        """Test that factory routes to Watermarks."""
        mock_urlopen.set_response("catalogs/creature_types.json")
        catalog = Catalogs("watermarks")

        assert isinstance(catalog, Watermarks)
        assert "api.scryfall.com/catalog/watermarks" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_ability_words(self, mock_urlopen):
        """Test that factory routes to AbilityWords."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        catalog = Catalogs("ability-words")

        assert isinstance(catalog, AbilityWords)
        assert "api.scryfall.com/catalog/ability-words" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_flavor_words(self, mock_urlopen):
        """Test that factory routes to FlavorWords."""
        mock_urlopen.set_response("catalogs/keyword_abilities.json")
        catalog = Catalogs("flavor-words")

        assert isinstance(catalog, FlavorWords)
        assert "api.scryfall.com/catalog/flavor-words" in mock_urlopen.calls[0]["url"]

    def test_factory_raises_error_for_invalid_type(self, mock_urlopen):
        """Test that factory raises error for invalid catalog type."""
        mock_urlopen.set_response("catalogs/card_names.json")

        with pytest.raises(ValueError, match="Unknown catalog type"):
            Catalogs("invalid-type")
