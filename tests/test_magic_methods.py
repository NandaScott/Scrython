"""Tests for magic methods (__repr__, __str__, __eq__, __hash__)."""

from scrython.base import ScrythonRequestHandler
from scrython.cards.cards import Object


class TestMagicMethodsBase:
    """Test magic methods on ScrythonRequestHandler."""

    def test_repr_with_card(self, mock_urlopen, sample_card):
        """Test __repr__ returns developer-friendly representation for cards."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        repr_str = repr(handler)

        assert "TestHandler" in repr_str
        assert sample_card["id"] in repr_str
        assert "Black Lotus" in repr_str

    def test_repr_with_set(self, mock_urlopen, sample_set):
        """Test __repr__ returns developer-friendly representation for sets."""
        mock_urlopen.set_response(data=sample_set)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "sets"

        handler = TestHandler()
        repr_str = repr(handler)

        assert "TestHandler" in repr_str
        assert sample_set["id"] in repr_str
        # Should show either name or code
        assert "Limited Edition Alpha" in repr_str or "lea" in repr_str

    def test_repr_without_id_or_name(self, mock_urlopen):
        """Test __repr__ with minimal data."""
        mock_urlopen.set_response(data={"object": "test"})

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "test"

        handler = TestHandler()
        repr_str = repr(handler)

        assert "TestHandler" in repr_str
        assert "()" in repr_str  # Should have empty parens if no data

    def test_str_with_card(self, mock_urlopen, sample_card):
        """Test __str__ returns user-friendly string for cards."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        str_repr = str(handler)

        assert str_repr == "Black Lotus (LEA)"

    def test_str_with_card_no_set(self, mock_urlopen):
        """Test __str__ with card that has no set code."""
        card_data = {
            "object": "card",
            "id": "test-id",
            "name": "Test Card",
        }
        mock_urlopen.set_response(data=card_data)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Test Card")
        str_repr = str(handler)

        assert str_repr == "Test Card"

    def test_str_with_set(self, mock_urlopen, sample_set):
        """Test __str__ returns user-friendly string for sets."""
        mock_urlopen.set_response(data=sample_set)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "sets"

        handler = TestHandler()
        str_repr = str(handler)

        assert str_repr == "Limited Edition Alpha (LEA)"

    def test_str_with_list(self, mock_urlopen):
        """Test __str__ with list objects."""
        list_data = {"object": "list", "total_cards": 42, "has_more": False, "data": []}
        mock_urlopen.set_response(data=list_data)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/search"

        handler = TestHandler(q="bolt")
        str_repr = str(handler)

        assert str_repr == "List with 42 items"

    def test_str_with_catalog(self, mock_urlopen):
        """Test __str__ with catalog objects."""
        catalog_data = {"object": "catalog", "data": ["item1", "item2", "item3"]}
        mock_urlopen.set_response(data=catalog_data)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "catalog"

        handler = TestHandler()
        str_repr = str(handler)

        assert str_repr == "Catalog with 3 items"

    def test_eq_same_card_same_id(self, mock_urlopen, sample_card):
        """Test equality for cards with same ID."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler1 = TestHandler(fuzzy="Black Lotus")

        mock_urlopen.set_response(data=sample_card)
        handler2 = TestHandler(fuzzy="Black Lotus")

        assert handler1 == handler2

    def test_eq_different_cards(self, mock_urlopen, sample_card):
        """Test inequality for cards with different IDs."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler1 = TestHandler(fuzzy="Black Lotus")

        different_card = sample_card.copy()
        different_card["id"] = "different-id-1234"
        different_card["name"] = "Lightning Bolt"
        mock_urlopen.set_response(data=different_card)

        handler2 = TestHandler(fuzzy="Lightning Bolt")

        assert handler1 != handler2

    def test_eq_with_non_handler_object(self, mock_urlopen, sample_card):
        """Test inequality with non-ScrythonRequestHandler objects."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        assert handler != "Black Lotus"
        assert handler != 123
        assert handler is not None
        assert handler != {"id": sample_card["id"]}

    def test_eq_without_ids(self, mock_urlopen):
        """Test equality fallback to identity when no IDs present."""
        data = {"object": "test"}
        mock_urlopen.set_response(data=data)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "test"

        handler1 = TestHandler()

        mock_urlopen.set_response(data=data)
        handler2 = TestHandler()

        # Without IDs, should use identity comparison
        assert handler1 == handler1
        assert handler1 != handler2

    def test_hash_same_card(self, mock_urlopen, sample_card):
        """Test that cards with same ID have same hash."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler1 = TestHandler(fuzzy="Black Lotus")

        mock_urlopen.set_response(data=sample_card)
        handler2 = TestHandler(fuzzy="Black Lotus")

        assert hash(handler1) == hash(handler2)

    def test_hash_different_cards(self, mock_urlopen, sample_card):
        """Test that cards with different IDs have different hashes."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler1 = TestHandler(fuzzy="Black Lotus")

        different_card = sample_card.copy()
        different_card["id"] = "different-id-1234"
        mock_urlopen.set_response(data=different_card)

        handler2 = TestHandler(fuzzy="Lightning Bolt")

        assert hash(handler1) != hash(handler2)

    def test_hash_enables_set_usage(self, mock_urlopen, sample_card):
        """Test that cards can be used in sets."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler1 = TestHandler(fuzzy="Black Lotus")

        mock_urlopen.set_response(data=sample_card)
        handler2 = TestHandler(fuzzy="Black Lotus")

        different_card = sample_card.copy()
        different_card["id"] = "different-id"
        mock_urlopen.set_response(data=different_card)
        handler3 = TestHandler(fuzzy="Lightning Bolt")

        # Should deduplicate based on ID
        card_set = {handler1, handler2, handler3}
        assert len(card_set) == 2  # handler1 and handler2 are same card

    def test_hash_enables_dict_usage(self, mock_urlopen, sample_card):
        """Test that cards can be used as dict keys."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        card_dict = {handler: "owned"}
        assert card_dict[handler] == "owned"


class TestMagicMethodsObject:
    """Test magic methods on cards.Object class."""

    def test_object_repr(self):
        """Test __repr__ for Object class."""
        card_data = {
            "id": "test-id-123",
            "name": "Test Card",
            "set": "tst",
        }
        obj = Object(card_data)
        repr_str = repr(obj)

        assert "Object" in repr_str
        assert "test-id-123" in repr_str
        assert "Test Card" in repr_str

    def test_object_str(self):
        """Test __str__ for Object class."""
        card_data = {
            "name": "Lightning Bolt",
            "set": "lea",
        }
        obj = Object(card_data)
        str_repr = str(obj)

        assert str_repr == "Lightning Bolt (LEA)"

    def test_object_str_no_set(self):
        """Test __str__ for Object with no set."""
        card_data = {
            "name": "Test Card",
        }
        obj = Object(card_data)
        str_repr = str(obj)

        assert str_repr == "Test Card"

    def test_object_eq_same_id(self):
        """Test equality for Objects with same ID."""
        card_data1 = {"id": "same-id", "name": "Card 1"}
        card_data2 = {"id": "same-id", "name": "Card 1"}

        obj1 = Object(card_data1)
        obj2 = Object(card_data2)

        assert obj1 == obj2

    def test_object_eq_different_ids(self):
        """Test inequality for Objects with different IDs."""
        card_data1 = {"id": "id-1", "name": "Card 1"}
        card_data2 = {"id": "id-2", "name": "Card 2"}

        obj1 = Object(card_data1)
        obj2 = Object(card_data2)

        assert obj1 != obj2

    def test_object_eq_non_object(self):
        """Test inequality with non-Object types."""
        card_data = {"id": "test-id", "name": "Test Card"}
        obj = Object(card_data)

        assert obj != "Test Card"
        assert obj != 123
        assert obj is not None

    def test_object_hash_same_id(self):
        """Test that Objects with same ID have same hash."""
        card_data1 = {"id": "same-id", "name": "Card 1"}
        card_data2 = {"id": "same-id", "name": "Card 1"}

        obj1 = Object(card_data1)
        obj2 = Object(card_data2)

        assert hash(obj1) == hash(obj2)

    def test_object_hash_different_ids(self):
        """Test that Objects with different IDs have different hashes."""
        card_data1 = {"id": "id-1", "name": "Card 1"}
        card_data2 = {"id": "id-2", "name": "Card 2"}

        obj1 = Object(card_data1)
        obj2 = Object(card_data2)

        assert hash(obj1) != hash(obj2)

    def test_object_set_usage(self):
        """Test that Objects can be used in sets."""
        card1 = {"id": "id-1", "name": "Card 1"}
        card2 = {"id": "id-1", "name": "Card 1"}  # Duplicate
        card3 = {"id": "id-2", "name": "Card 2"}

        obj1 = Object(card1)
        obj2 = Object(card2)
        obj3 = Object(card3)

        card_set = {obj1, obj2, obj3}
        assert len(card_set) == 2  # obj1 and obj2 are duplicates

    def test_object_dict_usage(self):
        """Test that Objects can be used as dict keys."""
        card_data = {"id": "test-id", "name": "Test Card"}
        obj = Object(card_data)

        card_dict = {obj: "owned"}
        assert card_dict[obj] == "owned"
