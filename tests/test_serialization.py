"""Tests for serialization methods (to_dict, to_json, from_dict, to_list)."""

import json

from scrython.base import ScrythonRequestHandler
from scrython.cards.cards import Object


class TestSerializationBase:
    """Test serialization methods on ScrythonRequestHandler."""

    def test_to_dict_returns_copy(self, mock_urlopen, sample_card):
        """Test that to_dict returns a copy of the data."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        card_dict = handler.to_dict()

        # Should be equal
        assert card_dict == sample_card
        # But not the same object (copy, not reference)
        assert card_dict is not handler._scryfall_data

    def test_to_dict_modification_doesnt_affect_original(self, mock_urlopen, sample_card):
        """Test that modifying the returned dict doesn't affect the object."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        card_dict = handler.to_dict()

        # Modify the dict
        card_dict["name"] = "Modified Name"

        # Original should be unchanged
        assert handler._scryfall_data["name"] == "Black Lotus"

    def test_to_json_returns_valid_json(self, mock_urlopen, sample_card):
        """Test that to_json returns valid JSON string."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        json_str = handler.to_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed == sample_card

    def test_to_json_with_indent(self, mock_urlopen, sample_card):
        """Test that to_json accepts formatting parameters."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        json_str = handler.to_json(indent=2)

        # Should contain newlines (indicating indentation)
        assert "\n" in json_str
        # Should still be valid JSON
        parsed = json.loads(json_str)
        assert parsed == sample_card

    def test_to_json_with_sort_keys(self, mock_urlopen, sample_card):
        """Test that to_json accepts sort_keys parameter."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        json_str = handler.to_json(sort_keys=True)

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed == sample_card

    def test_from_dict_creates_instance(self, sample_card):
        """Test that from_dict creates an instance without API call."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Create from dict (no mock_urlopen, so would fail if API call attempted)
        handler = TestHandler.from_dict(sample_card)

        assert handler._scryfall_data == sample_card

    def test_from_dict_doesnt_modify_source(self, sample_card):
        """Test that from_dict doesn't modify the source dict."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        original_data = sample_card.copy()
        handler = TestHandler.from_dict(sample_card)

        # Modify the handler's data
        handler._scryfall_data["name"] = "Modified"

        # Original dict should be unchanged
        assert sample_card == original_data

    def test_round_trip_to_dict_from_dict(self, mock_urlopen, sample_card):
        """Test round-trip serialization with to_dict and from_dict."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Create from API
        handler1 = TestHandler(fuzzy="Black Lotus")

        # Export to dict
        card_dict = handler1.to_dict()

        # Create from dict
        handler2 = TestHandler.from_dict(card_dict)

        # Should have same data
        assert handler1._scryfall_data == handler2._scryfall_data

    def test_round_trip_to_json_from_dict(self, mock_urlopen, sample_card):
        """Test round-trip serialization with to_json and from_dict."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Create from API
        handler1 = TestHandler(fuzzy="Black Lotus")

        # Export to JSON
        json_str = handler1.to_json()

        # Parse JSON and create from dict
        card_dict = json.loads(json_str)
        handler2 = TestHandler.from_dict(card_dict)

        # Should have same data
        assert handler1._scryfall_data == handler2._scryfall_data


class TestSerializationObject:
    """Test serialization methods on cards.Object class."""

    def test_object_to_dict(self):
        """Test to_dict on Object class."""
        card_data = {
            "id": "test-id",
            "name": "Test Card",
            "set": "tst",
        }
        obj = Object(card_data)
        result = obj.to_dict()

        assert result == card_data
        assert result is not obj._scryfall_data

    def test_object_to_json(self):
        """Test to_json on Object class."""
        card_data = {
            "id": "test-id",
            "name": "Test Card",
            "set": "tst",
        }
        obj = Object(card_data)
        json_str = obj.to_json()

        parsed = json.loads(json_str)
        assert parsed == card_data

    def test_object_to_json_with_indent(self):
        """Test to_json with formatting on Object class."""
        card_data = {
            "id": "test-id",
            "name": "Test Card",
        }
        obj = Object(card_data)
        json_str = obj.to_json(indent=2)

        assert "\n" in json_str
        parsed = json.loads(json_str)
        assert parsed == card_data

    def test_object_from_dict(self):
        """Test from_dict on Object class."""
        card_data = {
            "id": "test-id",
            "name": "Test Card",
            "set": "tst",
        }
        obj = Object.from_dict(card_data)

        assert obj._scryfall_data == card_data

    def test_object_round_trip(self):
        """Test round-trip serialization on Object class."""
        card_data = {
            "id": "test-id",
            "name": "Test Card",
            "set": "tst",
        }
        obj1 = Object(card_data)
        card_dict = obj1.to_dict()
        obj2 = Object.from_dict(card_dict)

        assert obj1._scryfall_data == obj2._scryfall_data


class TestSerializationList:
    """Test serialization methods on list results."""

    def test_to_list_with_objects(self, mock_urlopen):
        """Test to_list with wrapped Object instances."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "id-1", "name": "Card 1", "set": "tst"},
                {"id": "id-2", "name": "Card 2", "set": "tst"},
                {"id": "id-3", "name": "Card 3", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        from scrython.cards.cards import Search

        results = Search(q="test")
        result_list = results.to_list()

        # Should be a list of dicts
        assert isinstance(result_list, list)
        assert len(result_list) == 3

        # Each item should be a dict
        for item in result_list:
            assert isinstance(item, dict)
            assert "id" in item
            assert "name" in item

    def test_to_list_empty(self, mock_urlopen):
        """Test to_list with empty results."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [],
        }
        mock_urlopen.set_response(data=list_data)

        from scrython.cards.cards import Search

        results = Search(q="nonexistent")
        result_list = results.to_list()

        assert result_list == []

    def test_to_list_doesnt_affect_original(self, mock_urlopen):
        """Test that modifying to_list result doesn't affect original data."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "id-1", "name": "Card 1", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        from scrython.cards.cards import Search

        results = Search(q="test")
        result_list = results.to_list()

        # Modify the list
        result_list[0]["name"] = "Modified Name"

        # Original should be unchanged
        assert results.data[0].name == "Card 1"

    def test_to_list_multiple_calls(self, mock_urlopen):
        """Test that multiple calls to to_list work correctly."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "id-1", "name": "Card 1", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        from scrython.cards.cards import Search

        results = Search(q="test")

        # Call multiple times
        list1 = results.to_list()
        list2 = results.to_list()

        # Should return equivalent data
        assert list1 == list2
        # But different list objects
        assert list1 is not list2
