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
