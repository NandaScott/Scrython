from functools import cache
from typing import Any


class ScryfallListMixin:
    list_data_type: type | None = None
    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        return "list"

    @property
    @cache
    def data(self) -> list[Any]:
        if self.list_data_type:
            return list(map(lambda data: self.list_data_type(data), self._scryfall_data["data"]))  # type: ignore[misc]

        return self._scryfall_data["data"]

    @property
    def has_more(self) -> bool:
        return self._scryfall_data["has_more"]

    @property
    def next_page(self) -> str | None:
        return self._scryfall_data.get("next_page")

    @property
    def total_cards(self) -> int | None:
        return self._scryfall_data.get("total_cards")

    @property
    def warnings(self) -> list[str] | None:
        return self._scryfall_data.get("warnings")

    def to_list(self) -> list[dict[str, Any]]:
        """
        Export all list items as a list of dictionaries.

        For list results that contain wrapped objects (like card searches),
        this method serializes each item to a dictionary.

        Returns:
            List of dictionaries containing data for each item

        Example:
            results = scrython.cards.Search(q='bolt')
            all_cards = results.to_list()  # List of card dicts
            for card_dict in all_cards:
                print(card_dict['name'])
        """
        items = []
        for item in self.data:
            # If the item has a to_dict method, use it
            if hasattr(item, "to_dict"):
                items.append(item.to_dict())
            # If the item has _scryfall_data, use that
            elif hasattr(item, "_scryfall_data"):
                items.append(item._scryfall_data.copy())
            # Otherwise, assume it's already a dict or primitive
            else:
                items.append(item)
        return items

    def __iter__(self):
        """
        Allow direct iteration over list results.

        Enables Pythonic iteration over the data in the current page.

        Returns:
            Iterator over data items

        Example:
            results = scrython.cards.Search(q='bolt')
            for card in results:
                print(card.name)
        """
        return iter(self.data)

    def __len__(self) -> int:
        """
        Return the number of items in the current page.

        Returns:
            Number of items in current page data

        Example:
            results = scrython.cards.Search(q='bolt')
            print(len(results))  # Number of cards in first page
        """
        return len(self.data)

    def iter_all(self, **kwargs):
        """
        Generator that auto-paginates through all results.

        Yields items from all pages, automatically fetching subsequent
        pages as needed. This is useful for processing large result sets
        without manually handling pagination.

        Args:
            **kwargs: Optional parameters:
                - cache (bool): Enable caching for pagination (default: False)
                - cache_ttl (int): Cache TTL in seconds (default: 3600)
                - rate_limit (bool): Enable rate limiting (default: True)
                - rate_limit_per_second (float): Rate limit (default: 10.0)

        Yields:
            Individual items from all pages

        Example:
            results = scrython.cards.Search(q='c:red')
            for card in results.iter_all():
                print(card.name)  # Processes all red cards across all pages

            # With caching enabled
            for card in results.iter_all(cache=True, cache_ttl=7200):
                print(card.name)
        """
        import hashlib

        # Yield items from current page
        yield from self.data

        # Fetch and yield subsequent pages
        current = self
        while current.has_more and current.next_page:
            # For pagination URLs, use SHA256 hash as cache key (absolute URLs)
            cache_key = hashlib.sha256(current.next_page.encode()).hexdigest()

            # Use _fetch_raw from ScrythonRequestHandler (available via mixin inheritance)
            next_data = self._fetch_raw(current.next_page, cache_key=cache_key, **kwargs)  # type: ignore[attr-defined]

            # Process items with list_data_type if present
            if self.list_data_type:
                items = [self.list_data_type(item) for item in next_data.get("data", [])]
            else:
                items = next_data.get("data", [])

            yield from items

            # Update pagination state for next iteration
            class _TempPage:
                def __init__(self, data):
                    self.has_more = data.get("has_more", False)
                    self.next_page = data.get("next_page")

            current = _TempPage(next_data)  # type: ignore[assignment]

    def as_dict(self, key: str) -> dict[str, Any]:
        """
        Convert list to dictionary keyed by a specified attribute.

        Args:
            key: Attribute name to use as dictionary key

        Returns:
            Dictionary mapping key values to objects

        Example:
            results = scrython.cards.Search(q='bolt')
            by_name = results.as_dict(key='name')
            print(by_name['Lightning Bolt'].set)
        """
        result = {}
        for item in self.data:
            # Get the key value from the item
            if hasattr(item, key):
                key_value = getattr(item, key)
            elif hasattr(item, "_scryfall_data") and key in item._scryfall_data:
                key_value = item._scryfall_data[key]
            else:
                continue

            result[key_value] = item
        return result

    def filter(self, predicate):
        """
        Filter results by a predicate function.

        Args:
            predicate: Function that takes an item and returns bool

        Returns:
            List of items that satisfy the predicate

        Example:
            results = scrython.cards.Search(q='bolt')
            cheap_cards = results.filter(lambda c: c.lowest_price() and c.lowest_price() < 1.0)
        """
        return [item for item in self.data if predicate(item)]

    def map(self, func):
        """
        Transform results with a function.

        Args:
            func: Function to apply to each item

        Returns:
            List of transformed results

        Example:
            results = scrython.cards.Search(q='bolt')
            card_names = results.map(lambda c: c.name)
        """
        return [func(item) for item in self.data]


class ScryfallCatalogMixin:
    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        return "catalog"

    @property
    def uri(self) -> str:
        return self._scryfall_data["uri"]

    @property
    def total_values(self) -> int:
        return self._scryfall_data["total_values"]

    @property
    def data(self) -> list[str]:
        return self._scryfall_data["data"]
