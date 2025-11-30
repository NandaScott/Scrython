from typing import Any


class SymbologyObjectMixin:
    """Provides property accessors for card symbol objects from the Scryfall API."""

    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        """
        A content type for this object, always card_symbol.

        Type: String (Required)
        """
        return "card_symbol"

    @property
    def symbol(self) -> str:
        """
        The plaintext symbol, usually in curly braces {}.

        Type: String (Required)

        Example: "{W}", "{U/B}", "{2}"
        """
        return self._scryfall_data["symbol"]

    @property
    def loose_variant(self) -> str | None:
        """
        An alternate plaintext symbol for this symbol, if it has one.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("loose_variant")

    @property
    def english(self) -> str:
        """
        An English description of this symbol.

        Type: String (Required)
        """
        return self._scryfall_data["english"]

    @property
    def transposable(self) -> bool:
        """
        True if this symbol can be replaced by other symbols.

        Type: Boolean (Required)
        """
        return self._scryfall_data["transposable"]

    @property
    def represents_mana(self) -> bool:
        """
        True if this symbol represents mana.

        Type: Boolean (Required)
        """
        return self._scryfall_data["represents_mana"]

    @property
    def mana_value(self) -> float | None:
        """
        A decimal number representing this symbol's mana value (formerly converted mana cost or CMC).

        Type: Decimal (Nullable)

        Note: Can be fractional for hybrid mana symbols.
        """
        return self._scryfall_data.get("mana_value")

    @property
    def appears_in_mana_costs(self) -> bool:
        """
        True if this symbol appears in mana costs.

        Type: Boolean (Required)
        """
        return self._scryfall_data["appears_in_mana_costs"]

    @property
    def funny(self) -> bool:
        """
        True if this symbol only appears on funny cards.

        Type: Boolean (Required)
        """
        return self._scryfall_data["funny"]

    @property
    def colors(self) -> list[str]:
        """
        An array of color abbreviations that this symbol represents.

        Type: Array of Strings (Required)

        Example: ["W"], ["U", "B"], []
        """
        return self._scryfall_data["colors"]

    @property
    def hybrid(self) -> bool:
        """
        True if this is a hybrid mana symbol.

        Type: Boolean (Required)
        """
        return self._scryfall_data.get("hybrid", False)

    @property
    def phyrexian(self) -> bool:
        """
        True if this is a Phyrexian mana symbol.

        Type: Boolean (Required)
        """
        return self._scryfall_data.get("phyrexian", False)

    @property
    def cmc(self) -> float | None:
        """
        A decimal number representing this symbol's converted mana cost.

        Type: Decimal (Nullable)

        Note: Deprecated. Use mana_value instead.
        """
        return self._scryfall_data.get("cmc")

    @property
    def svg_uri(self) -> str | None:
        """
        A URI to an SVG image of this symbol on Scryfall's CDN.

        Type: URI (Nullable)
        """
        return self._scryfall_data.get("svg_uri")

    @property
    def gatherer_alternates(self) -> list[str] | None:
        """
        An array of alternative Gatherer representations for this symbol.

        Type: Array of Strings (Nullable)
        """
        return self._scryfall_data.get("gatherer_alternates")


class ManaCostMixin:
    """Provides property accessors for mana cost parse results from the Scryfall API."""

    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        """
        A content type for this object, always mana_cost.

        Type: String (Required)
        """
        return "mana_cost"

    @property
    def cost(self) -> str:
        """
        The original mana cost string that was parsed.

        Type: String (Required)

        Example: "{2}{U}{U}"
        """
        return self._scryfall_data["cost"]

    @property
    def cmc(self) -> float:
        """
        The converted mana cost of this cost.

        Type: Decimal (Required)

        Note: Deprecated. Use mana_value instead.
        """
        return self._scryfall_data["cmc"]

    @property
    def mana_value(self) -> float:
        """
        The total mana value of this cost.

        Type: Decimal (Required)
        """
        return self._scryfall_data.get("mana_value", self._scryfall_data["cmc"])

    @property
    def colors(self) -> list[str]:
        """
        An array of color abbreviations in this cost.

        Type: Array of Strings (Required)

        Example: ["U"], ["W", "U"], []
        """
        return self._scryfall_data["colors"]

    @property
    def colorless(self) -> bool:
        """
        True if this cost contains no colored mana symbols.

        Type: Boolean (Required)
        """
        return self._scryfall_data["colorless"]

    @property
    def monocolored(self) -> bool:
        """
        True if this cost contains only one color of mana.

        Type: Boolean (Required)
        """
        return self._scryfall_data["monocolored"]

    @property
    def multicolored(self) -> bool:
        """
        True if this cost contains two or more colors of mana.

        Type: Boolean (Required)
        """
        return self._scryfall_data["multicolored"]
