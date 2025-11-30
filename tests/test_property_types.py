"""Comprehensive property type testing for all Scrython mixins.

This module tests that all properties across Cards, Sets, and BulkData endpoints
return the expected types and handle nullable fields correctly.
"""

import pytest

from scrython.bulk_data import ByType
from scrython.cards import Named
from scrython.sets import ByCode

# Card Properties Test Data
# Format: (property_name, expected_type, nullable, test_description)
CORE_FIELDS_PROPERTIES = [
    ("arena_id", (int, type(None)), True, "Arena ID"),
    ("card_id", str, False, "Scryfall UUID"),
    ("lang", str, False, "Language code"),
    ("mtgo_id", (int, type(None)), True, "MTGO ID"),
    ("mtgo_foil_id", (int, type(None)), True, "MTGO foil ID"),
    ("multiverse_ids", (list, type(None)), True, "Multiverse IDs array"),
    ("tcgplayer_id", (int, type(None)), True, "TCGPlayer ID"),
    ("tcgplayer_etched_id", (int, type(None)), True, "TCGPlayer etched ID"),
    ("cardmarket_id", (int, type(None)), True, "Cardmarket ID"),
    ("object", str, False, "Object type (always 'card')"),
    ("layout", str, False, "Card layout"),
    ("oracle_id", str, False, "Oracle ID"),
    ("prints_search_uri", str, False, "Prints search URI"),
    ("rulings_uri", str, False, "Rulings URI"),
    ("scryfall_uri", str, False, "Scryfall URI"),
    ("uri", str, False, "API URI"),
]

GAMEPLAY_FIELDS_PROPERTIES = [
    ("all_parts", (list, type(None)), True, "All card parts"),
    ("card_faces", (list, type(None)), True, "Card faces"),
    ("cmc", (int, float), False, "Converted mana cost"),
    ("color_identity", list, False, "Color identity"),
    ("color_indicator", (list, type(None)), True, "Color indicator"),
    ("colors", (list, type(None)), True, "Colors"),
    ("defense", (str, type(None)), True, "Defense value"),
    ("edhrec_rank", (int, type(None)), True, "EDHREC rank"),
    ("hand_modifier", (str, type(None)), True, "Hand modifier (Vanguard)"),
    ("keywords", list, False, "Keywords array"),
    ("legalities", dict, False, "Legalities object"),
    ("life_modifier", (str, type(None)), True, "Life modifier (Vanguard)"),
    ("loyalty", (str, type(None)), True, "Loyalty value"),
    ("mana_cost", (str, type(None)), True, "Mana cost"),
    ("name", str, False, "Card name"),
    ("oracle_text", (str, type(None)), True, "Oracle text"),
    ("penny_rank", (int, type(None)), True, "Penny Dreadful rank"),
    ("power", (str, type(None)), True, "Power value"),
    ("produced_mana", (list, type(None)), True, "Produced mana colors"),
    ("reserved", bool, False, "Reserved list status"),
    ("toughness", (str, type(None)), True, "Toughness value"),
    ("type_line", str, False, "Type line"),
]

PRINT_FIELDS_PROPERTIES = [
    ("artist", (str, type(None)), True, "Artist name"),
    ("artist_ids", (list, type(None)), True, "Artist IDs"),
    ("attraction_lights", (list, type(None)), True, "Attraction lights"),
    ("booster", bool, False, "In boosters"),
    ("border_color", str, False, "Border color"),
    ("card_back_id", (str, type(None)), True, "Card back ID"),
    ("collector_number", str, False, "Collector number"),
    ("content_warning", (bool, type(None)), True, "Content warning"),
    ("digital", bool, False, "Digital availability"),
    ("finishes", list, False, "Finishes array"),
    ("flavor_name", (str, type(None)), True, "Flavor name"),
    ("flavor_text", (str, type(None)), True, "Flavor text"),
    ("frame_effects", (list, type(None)), True, "Frame effects"),
    ("frame", str, False, "Frame version"),
    ("full_art", bool, False, "Full art status"),
    ("games", list, False, "Games array"),
    ("highres_image", bool, False, "High-res image availability"),
    ("illustration_id", (str, type(None)), True, "Illustration ID"),
    ("image_status", str, False, "Image status"),
    ("image_uris", (dict, type(None)), True, "Image URIs"),
    ("oversized", bool, False, "Oversized status"),
    # Skip preview - complex nested object with multiple sub-properties
    ("prices", dict, False, "Prices object"),
    ("printed_name", (str, type(None)), True, "Printed name"),
    ("printed_text", (str, type(None)), True, "Printed text"),
    ("printed_type_line", (str, type(None)), True, "Printed type line"),
    ("promo", bool, False, "Promo status"),
    ("promo_types", (list, type(None)), True, "Promo types"),
    ("purchase_uris", (dict, type(None)), True, "Purchase URIs"),
    ("rarity", str, False, "Rarity"),
    ("related_uris", dict, False, "Related URIs"),
    ("released_at", str, False, "Release date"),
    ("reprint", bool, False, "Reprint status"),
    ("security_stamp", (str, type(None)), True, "Security stamp"),
    ("set_name", str, False, "Set name"),
    ("set_search_uri", str, False, "Set search URI"),
    ("set_type", str, False, "Set type"),
    ("set_uri", str, False, "Set URI"),
    ("set", str, False, "Set code"),  # Fixed: property is "set" not "set_code"
    ("story_spotlight", bool, False, "Story spotlight"),
    ("textless", bool, False, "Textless status"),
    ("variation", bool, False, "Variation status"),
    ("variation_of", (str, type(None)), True, "Variation of ID"),
    ("watermark", (str, type(None)), True, "Watermark"),
]


class TestCardCoreFields:
    """Test CoreFieldsMixin properties."""

    @pytest.mark.parametrize("prop,expected_type,nullable,desc", CORE_FIELDS_PROPERTIES)
    def test_core_field_type(self, mock_urlopen, prop, expected_type, nullable, desc):
        """Test that each core field returns the expected type."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        value = getattr(card, prop)

        # If nullable and value is None, that's acceptable
        if nullable and value is None:
            return

        # Otherwise, check the type
        assert isinstance(value, expected_type), (
            f"Property '{prop}' ({desc}) returned {type(value).__name__} "
            f"instead of {expected_type}"
        )


class TestCardGameplayFields:
    """Test GameplayFieldsMixin properties."""

    @pytest.mark.parametrize("prop,expected_type,nullable,desc", GAMEPLAY_FIELDS_PROPERTIES)
    def test_gameplay_field_type(self, mock_urlopen, prop, expected_type, nullable, desc):
        """Test that each gameplay field returns the expected type."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        value = getattr(card, prop)

        # If nullable and value is None, that's acceptable
        if nullable and value is None:
            return

        # Otherwise, check the type
        assert isinstance(value, expected_type), (
            f"Property '{prop}' ({desc}) returned {type(value).__name__} "
            f"instead of {expected_type}"
        )


class TestCardPrintFields:
    """Test PrintFieldsMixin properties."""

    @pytest.mark.parametrize("prop,expected_type,nullable,desc", PRINT_FIELDS_PROPERTIES)
    def test_print_field_type(self, mock_urlopen, prop, expected_type, nullable, desc):
        """Test that each print field returns the expected type."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        value = getattr(card, prop)

        # If nullable and value is None, that's acceptable
        if nullable and value is None:
            return

        # Otherwise, check the type
        assert isinstance(value, expected_type), (
            f"Property '{prop}' ({desc}) returned {type(value).__name__} "
            f"instead of {expected_type}"
        )


# Sets Properties Test Data
SETS_OBJECT_PROPERTIES = [
    ("object", str, False, "Object type (always 'set')"),
    ("id", str, False, "Set UUID"),  # Fixed: property is "id" not "set_id"
    ("code", str, False, "Set code"),
    ("mtgo_code", (str, type(None)), True, "MTGO code"),
    ("arena_code", (str, type(None)), True, "Arena code"),
    ("tcgplayer_id", (int, type(None)), True, "TCGPlayer ID"),
    ("name", str, False, "Set name"),
    ("set_type", str, False, "Set type"),
    ("released_at", (str, type(None)), True, "Release date"),
    ("block_code", (str, type(None)), True, "Block code"),
    ("block", (str, type(None)), True, "Block name"),
    ("parent_set_code", (str, type(None)), True, "Parent set code"),
    ("card_count", int, False, "Card count"),
    ("printed_size", (int, type(None)), True, "Printed size"),
    ("digital", bool, False, "Digital availability"),
    ("foil_only", bool, False, "Foil only"),
    ("nonfoil_only", bool, False, "Nonfoil only"),
    ("scryfall_uri", str, False, "Scryfall URI"),
    ("uri", str, False, "API URI"),
    ("icon_svg_uri", str, False, "Icon SVG URI"),
    ("search_uri", str, False, "Search URI"),
]


class TestSetsObjectFields:
    """Test SetsObjectMixin properties."""

    @pytest.mark.parametrize("prop,expected_type,nullable,desc", SETS_OBJECT_PROPERTIES)
    def test_sets_field_type(self, mock_urlopen, prop, expected_type, nullable, desc):
        """Test that each sets field returns the expected type."""
        mock_urlopen.set_response("sets/by_code.json")
        set_obj = ByCode(code="lea")

        value = getattr(set_obj, prop)

        # If nullable and value is None, that's acceptable
        if nullable and value is None:
            return

        # Otherwise, check the type
        assert isinstance(value, expected_type), (
            f"Property '{prop}' ({desc}) returned {type(value).__name__} "
            f"instead of {expected_type}"
        )


# Bulk Data Properties Test Data
BULK_DATA_OBJECT_PROPERTIES = [
    ("object", str, False, "Object type (always 'bulk_data')"),
    ("id", str, False, "Bulk data UUID"),
    ("uri", str, False, "API URI"),
    ("type", str, False, "Bulk data type"),
    ("name", str, False, "Bulk data name"),
    ("description", str, False, "Description"),
    ("download_uri", str, False, "Download URI"),
    ("updated_at", str, False, "Last updated timestamp"),
    ("size", int, False, "File size in bytes"),
    ("content_type", str, False, "MIME type"),
    ("content_encoding", str, False, "Content encoding"),
]


class TestBulkDataObjectFields:
    """Test BulkDataObjectMixin properties."""

    @pytest.mark.parametrize("prop,expected_type,nullable,desc", BULK_DATA_OBJECT_PROPERTIES)
    def test_bulk_data_field_type(self, mock_urlopen, prop, expected_type, nullable, desc):
        """Test that each bulk data field returns the expected type."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        value = getattr(bulk, prop)

        # If nullable and value is None, that's acceptable
        if nullable and value is None:
            return

        # Otherwise, check the type
        assert isinstance(value, expected_type), (
            f"Property '{prop}' ({desc}) returned {type(value).__name__} "
            f"instead of {expected_type}"
        )
