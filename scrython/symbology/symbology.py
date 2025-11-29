from typing import Any

from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallListMixin

from .symbology_mixins import ManaCostMixin, SymbologyObjectMixin


class Object(SymbologyObjectMixin):
    """
    Wrapper class for individual card symbol objects from Scryfall API responses.

    Provides access to all card symbol properties through SymbologyObjectMixin.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self._scryfall_data = data


class All(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get all card symbols in Scryfall's database.

    Endpoint: GET /symbology

    Returns a list of CardSymbol objects representing all mana symbols, energy symbols,
    tap/untap symbols, and other symbols used in Magic card costs and text.

    Example:
        # Get all symbols
        symbols = scrython.symbology.All()

        # Iterate through symbols
        for symbol in symbols.data:
            if symbol.represents_mana:
                print(f"{symbol.symbol}: {symbol.english}")
                print(f"  Mana value: {symbol.mana_value}")
                print(f"  Colors: {symbol.colors}")

        # Filter to mana symbols only
        mana_symbols = [s for s in symbols.data if s.represents_mana]
        print(f"Total mana symbols: {len(mana_symbols)}")

        # Find hybrid symbols
        hybrid_symbols = [s for s in symbols.data if s.hybrid]
        print(f"Hybrid mana symbols: {len(hybrid_symbols)}")

    See: https://scryfall.com/docs/api/card-symbols
    """

    _endpoint = "/symbology"
    list_data_type = Object


class ParseMana(ManaCostMixin, ScrythonRequestHandler):
    """
    Parse a mana cost string into structured data.

    Endpoint: GET /symbology/parse-mana

    Returns a ManaCost object containing parsed information about the mana cost,
    including total mana value, colors, and whether the cost is colorless/mono/multi.

    Args:
        cost: The mana cost string to parse (required). Use curly braces for symbols.

    Example:
        # Parse a simple mana cost
        parsed = scrython.symbology.ParseMana(cost="{2}{U}{U}")
        print(f"Mana value: {parsed.mana_value}")  # 4
        print(f"Colors: {parsed.colors}")  # ['U']
        print(f"Monocolored: {parsed.monocolored}")  # True
        print(f"Multicolored: {parsed.multicolored}")  # False

        # Parse a multicolored cost
        parsed = scrython.symbology.ParseMana(cost="{G}{W}")
        print(f"Colors: {parsed.colors}")  # ['G', 'W']
        print(f"Multicolored: {parsed.multicolored}")  # True

        # Parse a hybrid cost
        parsed = scrython.symbology.ParseMana(cost="{2/W}{2/W}{2/W}")
        print(f"Mana value: {parsed.mana_value}")  # Depends on payment choice
        print(f"Monocolored: {parsed.monocolored}")  # True

        # Parse a colorless cost
        parsed = scrython.symbology.ParseMana(cost="{3}")
        print(f"Colorless: {parsed.colorless}")  # True

    See: https://scryfall.com/docs/api/card-symbols
    """

    _endpoint = "/symbology/parse-mana"


class Symbology:
    """
    Smart factory for Symbology API endpoints.

    Routes to the correct symbology endpoint based on provided kwargs.

    Supported parameters:
        - cost: Mana cost string to parse → ParseMana
        - (no parameters): Get all symbols → All

    Example:
        # Get all symbols
        symbols = scrython.Symbology()
        for symbol in symbols.data:
            print(symbol.symbol)

        # Parse a mana cost
        cost = scrython.Symbology(cost="{2}{U}{U}")
        print(f"Mana value: {cost.mana_value}")
        print(f"Colors: {cost.colors}")
    """

    def __new__(cls, **kwargs):
        if "cost" in kwargs:
            return ParseMana(**kwargs)
        else:
            return All(**kwargs)
