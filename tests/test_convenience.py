"""Tests for convenience methods."""

from scrython.cards.cards import Named, Search


class TestCardConvenienceMethods:
    """Test convenience methods on card objects."""

    def test_is_legal_in_legal_format(self, mock_urlopen):
        """Test is_legal_in with a legal format."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Lightning Bolt",
            "legalities": {
                "standard": "not_legal",
                "modern": "legal",
                "commander": "legal",
                "vintage": "legal",
            },
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Lightning Bolt")
        assert card.is_legal_in("commander") is True
        assert card.is_legal_in("modern") is True

    def test_is_legal_in_not_legal_format(self, mock_urlopen):
        """Test is_legal_in with a not legal format."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Black Lotus",
            "legalities": {
                "standard": "not_legal",
                "modern": "banned",
                "commander": "banned",
                "vintage": "restricted",
            },
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Black Lotus")
        assert card.is_legal_in("standard") is False
        assert card.is_legal_in("modern") is False
        assert card.is_legal_in("commander") is False

    def test_is_legal_in_case_insensitive(self, mock_urlopen):
        """Test that is_legal_in is case insensitive."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "legalities": {"commander": "legal"},
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.is_legal_in("Commander") is True
        assert card.is_legal_in("COMMANDER") is True

    def test_has_color_single_color(self, mock_urlopen):
        """Test has_color with single color card."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Lightning Bolt",
            "colors": ["R"],
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Lightning Bolt")
        assert card.has_color("R") is True
        assert card.has_color("U") is False

    def test_has_color_multicolor(self, mock_urlopen):
        """Test has_color with multicolor card."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Boros Charm",
            "colors": ["R", "W"],
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Boros Charm")
        assert card.has_color("R") is True
        assert card.has_color("W") is True
        assert card.has_color("U") is False

    def test_has_color_colorless(self, mock_urlopen):
        """Test has_color with colorless card."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Sol Ring",
            "colors": [],
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Sol Ring")
        assert card.has_color("R") is False
        assert card.has_color("U") is False

    def test_has_color_case_insensitive(self, mock_urlopen):
        """Test that has_color is case insensitive."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Lightning Bolt",
            "colors": ["R"],
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Lightning Bolt")
        assert card.has_color("r") is True
        assert card.has_color("R") is True

    def test_is_creature(self, mock_urlopen):
        """Test is_creature property."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Grizzly Bears",
            "type_line": "Creature — Bear",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Grizzly Bears")
        assert card.is_creature is True

    def test_is_instant(self, mock_urlopen):
        """Test is_instant property."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Lightning Bolt",
            "type_line": "Instant",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Lightning Bolt")
        assert card.is_instant is True

    def test_is_sorcery(self, mock_urlopen):
        """Test is_sorcery property."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Demonic Tutor",
            "type_line": "Sorcery",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Demonic Tutor")
        assert card.is_sorcery is True

    def test_is_enchantment(self, mock_urlopen):
        """Test is_enchantment property."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Phyrexian Arena",
            "type_line": "Enchantment",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Phyrexian Arena")
        assert card.is_enchantment is True

    def test_is_artifact(self, mock_urlopen):
        """Test is_artifact property."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Sol Ring",
            "type_line": "Artifact",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Sol Ring")
        assert card.is_artifact is True

    def test_is_planeswalker(self, mock_urlopen):
        """Test is_planeswalker property."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Jace, the Mind Sculptor",
            "type_line": "Legendary Planeswalker — Jace",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Jace")
        assert card.is_planeswalker is True

    def test_type_checks_artifact_creature(self, mock_urlopen):
        """Test type checks with artifact creature."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Solemn Simulacrum",
            "type_line": "Artifact Creature — Golem",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Solemn Simulacrum")
        assert card.is_artifact is True
        assert card.is_creature is True

    def test_lowest_price_with_prices(self, mock_urlopen):
        """Test lowest_price with available prices."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "prices": {"usd": "1.50", "usd_foil": "3.00", "eur": "2.00", "tix": "0.50"},
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.lowest_price() == 0.50

    def test_lowest_price_with_nulls(self, mock_urlopen):
        """Test lowest_price with some null prices."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "prices": {"usd": "1.50", "usd_foil": None, "eur": None, "tix": None},
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.lowest_price() == 1.50

    def test_lowest_price_all_null(self, mock_urlopen):
        """Test lowest_price with all null prices."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "prices": {"usd": None, "usd_foil": None, "eur": None, "tix": None},
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.lowest_price() is None

    def test_highest_price_with_prices(self, mock_urlopen):
        """Test highest_price with available prices."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "prices": {"usd": "1.50", "usd_foil": "10.00", "eur": "5.00", "tix": "0.50"},
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.highest_price() == 10.00

    def test_highest_price_with_nulls(self, mock_urlopen):
        """Test highest_price with some null prices."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "prices": {"usd": "1.50", "usd_foil": None, "eur": None, "tix": None},
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.highest_price() == 1.50

    def test_get_image_url_normal(self, mock_urlopen):
        """Test get_image_url with normal images."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
            "image_uris": {
                "small": "https://example.com/small.jpg",
                "normal": "https://example.com/normal.jpg",
                "large": "https://example.com/large.jpg",
            },
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.get_image_url() == "https://example.com/normal.jpg"
        assert card.get_image_url(size="large") == "https://example.com/large.jpg"

    def test_get_image_url_double_faced(self, mock_urlopen):
        """Test get_image_url with double-faced card."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Delver of Secrets // Insectile Aberration",
            "card_faces": [
                {
                    "name": "Delver of Secrets",
                    "image_uris": {
                        "normal": "https://example.com/delver.jpg",
                        "large": "https://example.com/delver_large.jpg",
                    },
                },
                {
                    "name": "Insectile Aberration",
                    "image_uris": {"normal": "https://example.com/aberration.jpg"},
                },
            ],
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Delver")
        assert card.get_image_url() == "https://example.com/delver.jpg"
        assert card.get_image_url(size="large") == "https://example.com/delver_large.jpg"

    def test_get_image_url_no_images(self, mock_urlopen):
        """Test get_image_url with no images available."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
        }
        mock_urlopen.set_response(data=card_data)

        card = Named(fuzzy="Test Card")
        assert card.get_image_url() is None


class TestListConvenienceMethods:
    """Test convenience methods on list results."""

    def test_as_dict_by_name(self, mock_urlopen):
        """Test as_dict keyed by name."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Lightning Bolt", "set": "lea"},
                {"id": "2", "name": "Black Lotus", "set": "lea"},
                {"id": "3", "name": "Counterspell", "set": "ice"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        by_name = results.as_dict(key="name")

        assert len(by_name) == 3
        assert "Lightning Bolt" in by_name
        assert by_name["Lightning Bolt"].name == "Lightning Bolt"

    def test_as_dict_by_id(self, mock_urlopen):
        """Test as_dict keyed by id."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "id-1", "name": "Card 1", "set": "tst"},
                {"id": "id-2", "name": "Card 2", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        by_id = results.as_dict(key="card_id")

        assert len(by_id) == 2
        assert "id-1" in by_id

    def test_filter_by_set(self, mock_urlopen):
        """Test filter by set."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "lea"},
                {"id": "2", "name": "Card 2", "set": "ice"},
                {"id": "3", "name": "Card 3", "set": "lea"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        lea_cards = results.filter(lambda c: c.set == "lea")

        assert len(lea_cards) == 2
        assert all(c.set == "lea" for c in lea_cards)

    def test_filter_empty_results(self, mock_urlopen):
        """Test filter that returns no results."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "lea"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        filtered = results.filter(lambda c: c.set == "nonexistent")

        assert len(filtered) == 0

    def test_map_to_names(self, mock_urlopen):
        """Test map to extract names."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Lightning Bolt", "set": "lea"},
                {"id": "2", "name": "Black Lotus", "set": "lea"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        names = results.map(lambda c: c.name)

        assert names == ["Lightning Bolt", "Black Lotus"]

    def test_map_to_tuples(self, mock_urlopen):
        """Test map to create tuples."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Lightning Bolt", "set": "lea"},
                {"id": "2", "name": "Black Lotus", "set": "lea"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        tuples = results.map(lambda c: (c.name, c.set))

        assert tuples == [("Lightning Bolt", "lea"), ("Black Lotus", "lea")]

    def test_filter_and_map_chaining(self, mock_urlopen):
        """Test chaining filter and map."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Lightning Bolt", "set": "lea"},
                {"id": "2", "name": "Black Lotus", "set": "ice"},
                {"id": "3", "name": "Counterspell", "set": "lea"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")
        # Filter to LEA, then map to names
        lea_names = [c.name for c in results.filter(lambda c: c.set == "lea")]

        assert lea_names == ["Lightning Bolt", "Counterspell"]
