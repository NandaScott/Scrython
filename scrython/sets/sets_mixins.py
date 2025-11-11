from typing import Any


class SetsObjectMixin:
    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        """
        A content type for this object, always set.

        Type: String (Required)
        """
        return "set"

    @property
    def id(self) -> str:
        """
        A unique ID for this set on Scryfall that will not change.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def code(self) -> str:
        """
        The unique three to six-letter code for this set.

        Type: String (Required)
        """
        return self._scryfall_data["code"]

    @property
    def mtgo_code(self) -> str | None:
        """
        The unique code for this set on MTGO, which may differ from the regular code.

        Type: String (Nullable)
        """
        return self._scryfall_data["mtgo_code"]

    @property
    def arena_code(self) -> str | None:
        """
        The unique code for this set on Arena, which may differ from the regular code.

        Type: String (Nullable)
        """
        return self._scryfall_data["arena_code"]

    @property
    def tcgplayer_id(self) -> int | None:
        """
        This set's ID on TCGplayer's API, also known as the groupId.

        Type: Integer (Nullable)
        """
        return self._scryfall_data["tcgplayer_id"]

    @property
    def name(self) -> str:
        """
        The English name of the set.

        Type: String (Required)
        """
        return self._scryfall_data["name"]

    @property
    def set_type(self) -> str:
        """
        A computer-readable classification for this set.

        Type: String (Required)
        """
        return self._scryfall_data["set_type"]

    @property
    def released_at(self) -> str | None:
        """
        The date the set was released or the first card was printed in the set (in GMT-8 Pacific time).

        Type: Date (Nullable)
        """
        return self._scryfall_data["released_at"]

    @property
    def block_code(self) -> str | None:
        """
        The block code for this set, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data["block_code"]

    @property
    def block(self) -> str | None:
        """
        The block or group name code for this set, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data["block"]

    @property
    def parent_set_code(self) -> str | None:
        """
        The set code for the parent set, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data["parent_set_code"]

    @property
    def card_count(self) -> int:
        """
        The number of cards in this set.

        Type: Integer (Required)
        """
        return self._scryfall_data["card_count"]

    @property
    def printed_size(self) -> int | None:
        """
        The denominator for the set's printed collector numbers.

        Type: Integer (Nullable)
        """
        return self._scryfall_data["printed_size"]

    @property
    def digital(self) -> bool:
        """
        True if this set was only released in a video game.

        Type: Boolean (Required)
        """
        return self._scryfall_data["digital"]

    @property
    def foil_only(self) -> bool:
        """
        True if this set contains only foil cards.

        Type: Boolean (Required)
        """
        return self._scryfall_data["foil_only"]

    @property
    def nonfoil_only(self) -> bool:
        """
        True if this set contains only nonfoil cards.

        Type: Boolean (Required)
        """
        return self._scryfall_data["nonfoil_only"]

    @property
    def scryfall_uri(self) -> str:
        """
        A link to this set's permapage on Scryfall's website.

        Type: URI (Required)
        """
        return self._scryfall_data["scryfall_uri"]

    @property
    def uri(self) -> str:
        """
        A link to this set object on Scryfall's API.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]

    @property
    def icon_svg_uri(self) -> str:
        """
        A URI to an SVG file for this set's icon on Scryfall's CDN.

        Type: URI (Required)
        """
        return self._scryfall_data["icon_svg_uri"]

    @property
    def search_uri(self) -> str:
        """
        A Scryfall API URI that you can request to begin paginating over the cards in this set.

        Type: URI (Required)
        """
        return self._scryfall_data["search_uri"]
