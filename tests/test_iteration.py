"""Tests for iteration support (__iter__, __len__, iter_all)."""

from scrython.cards.cards import Search


class TestIterationBasics:
    """Test basic iteration functionality."""

    def test_iter_allows_direct_iteration(self, mock_urlopen):
        """Test that __iter__ allows for-loop iteration."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "tst"},
                {"id": "2", "name": "Card 2", "set": "tst"},
                {"id": "3", "name": "Card 3", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        # Should be able to iterate directly
        cards = []
        for card in results:
            cards.append(card.name)

        assert len(cards) == 3
        assert cards == ["Card 1", "Card 2", "Card 3"]

    def test_len_returns_current_page_size(self, mock_urlopen):
        """Test that __len__ returns number of items in current page."""
        list_data = {
            "object": "list",
            "has_more": True,
            "total_cards": 500,
            "data": [{"id": str(i), "name": f"Card {i}", "set": "tst"} for i in range(175)],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        # Length should be current page size, not total_cards
        assert len(results) == 175

    def test_iter_with_empty_results(self, mock_urlopen):
        """Test iteration with empty results."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="nonexistent")

        cards = list(results)
        assert len(cards) == 0
        assert len(results) == 0

    def test_iter_multiple_times(self, mock_urlopen):
        """Test that we can iterate multiple times."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "tst"},
                {"id": "2", "name": "Card 2", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        # First iteration
        first_names = [card.name for card in results]
        # Second iteration
        second_names = [card.name for card in results]

        assert first_names == second_names
        assert first_names == ["Card 1", "Card 2"]

    def test_iter_works_with_list_comprehension(self, mock_urlopen):
        """Test that iteration works with list comprehensions."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Lightning Bolt", "set": "tst"},
                {"id": "2", "name": "Black Lotus", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        # List comprehension
        names = [card.name for card in results]
        assert names == ["Lightning Bolt", "Black Lotus"]

    def test_iter_works_with_filter(self, mock_urlopen):
        """Test that iteration works with filter()."""
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

        # Filter to LEA cards
        lea_cards = [card for card in results if card.set == "lea"]
        assert len(lea_cards) == 2


class TestIterAllPagination:
    """Test iter_all() auto-pagination functionality."""

    def test_iter_all_single_page(self, mock_urlopen):
        """Test iter_all with single page results."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "tst"},
                {"id": "2", "name": "Card 2", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        all_cards = list(results.iter_all())
        assert len(all_cards) == 2
        assert all_cards[0].name == "Card 1"
        assert all_cards[1].name == "Card 2"

    def test_iter_all_multiple_pages(self, mock_urlopen):
        """Test iter_all with multiple pages."""
        import json
        from unittest.mock import Mock, patch

        # First page
        page1_data = {
            "object": "list",
            "has_more": True,
            "next_page": "https://api.scryfall.com/cards/search?page=2",
            "data": [
                {"id": "1", "name": "Card 1", "set": "tst"},
                {"id": "2", "name": "Card 2", "set": "tst"},
            ],
        }

        # Second page
        page2_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "3", "name": "Card 3", "set": "tst"},
                {"id": "4", "name": "Card 4", "set": "tst"},
            ],
        }

        mock_urlopen.set_response(data=page1_data)
        results = Search(q="test")

        # Mock the urlopen call that iter_all makes directly
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(page2_data).encode("utf-8")
        mock_response.info.return_value.get_param.return_value = "utf-8"
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            # iter_all should fetch all pages
            all_cards = list(results.iter_all())

        assert len(all_cards) == 4
        assert all_cards[0].name == "Card 1"
        assert all_cards[1].name == "Card 2"
        assert all_cards[2].name == "Card 3"
        assert all_cards[3].name == "Card 4"

    def test_iter_all_empty_results(self, mock_urlopen):
        """Test iter_all with empty results."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="nonexistent")

        all_cards = list(results.iter_all())
        assert len(all_cards) == 0

    def test_iter_all_is_generator(self, mock_urlopen):
        """Test that iter_all returns a generator."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [{"id": "1", "name": "Card 1", "set": "tst"}],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        generator = results.iter_all()
        # Check it's a generator
        assert hasattr(generator, "__iter__")
        assert hasattr(generator, "__next__")

    def test_iter_all_can_be_consumed_once(self, mock_urlopen):
        """Test that iter_all generator can only be consumed once."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "tst"},
                {"id": "2", "name": "Card 2", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        # First consumption
        generator = results.iter_all()
        first = list(generator)
        assert len(first) == 2

        # Generator is exhausted
        second = list(generator)
        assert len(second) == 0

        # But we can create a new generator
        new_generator = results.iter_all()
        third = list(new_generator)
        assert len(third) == 2

    def test_iter_vs_iter_all_single_page(self, mock_urlopen):
        """Test that iter and iter_all give same results for single page."""
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [
                {"id": "1", "name": "Card 1", "set": "tst"},
                {"id": "2", "name": "Card 2", "set": "tst"},
            ],
        }
        mock_urlopen.set_response(data=list_data)

        results = Search(q="test")

        iter_cards = [card.name for card in results]
        iter_all_cards = [card.name for card in results.iter_all()]

        assert iter_cards == iter_all_cards
