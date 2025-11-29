from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallListMixin
from scrython.types import ScryfallSetData

from .sets_mixins import SetsObjectMixin


class Object(SetsObjectMixin):
    """
    Wrapper class for individual set objects from Scryfall API responses.

    Provides access to all set properties through SetsObjectMixin.
    """

    def __init__(self, data: ScryfallSetData) -> None:
        self._scryfall_data = data  # type: ignore[assignment]


class All(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get all Magic: The Gathering sets in Scryfall's database.

    Endpoint: GET /sets

    Returns a list of all Set objects. Sets are returned in chronological order
    by default. This includes all official sets, promotional sets, and token sets.

    Example:
        # Get all sets
        all_sets = scrython.sets.All()

        # Iterate through sets
        for set_obj in all_sets.data:
            print(f"{set_obj.name} ({set_obj.code}) - {set_obj.card_count} cards")

        # Check if there are more results
        if all_sets.has_more:
            print("More sets available via pagination")

    See: https://scryfall.com/docs/api/sets/all
    """

    _endpoint = "/sets"
    list_data_type = Object


class ByCode(SetsObjectMixin, ScrythonRequestHandler):
    """
    Get a set by its three-to-six-letter set code.

    Endpoint: GET /sets/:code

    Returns a single Set object. Set codes are short, unique identifiers for each
    Magic set (e.g., "znr" for Zendikar Rising, "m21" for Core Set 2021).

    Args:
        code: The three-to-six-letter set code (required).

    Example:
        # Get a specific set by code
        set_obj = scrython.sets.ByCode(code='m21')
        print(f"{set_obj.name} released on {set_obj.released_at}")
        print(f"Set type: {set_obj.set_type}")
        print(f"Card count: {set_obj.card_count}")

    See: https://scryfall.com/docs/api/sets/code
    """

    _endpoint = "/sets/:code"


class ByTCGPlayerId(SetsObjectMixin, ScrythonRequestHandler):
    """
    Get a set by its TCGPlayer group ID.

    Endpoint: GET /sets/tcgplayer/:id

    Returns a single Set object. TCGPlayer group IDs identify product groups on
    TCGPlayer's marketplace. Useful for marketplace integration and price tracking.

    Args:
        id: The TCGPlayer group ID (required).

    Example:
        set_obj = scrython.sets.ByTCGPlayerId(id=12345)
        print(f"Set: {set_obj.name}")
        print(f"TCGPlayer ID: {set_obj.tcgplayer_id}")

    See: https://scryfall.com/docs/api/sets/tcgplayer
    """

    _endpoint = "/sets/tcgplayer/:id"


class ById(SetsObjectMixin, ScrythonRequestHandler):
    """
    Get a set by its Scryfall UUID.

    Endpoint: GET /sets/:id

    Returns a single Set object. Scryfall IDs are unique UUIDs that permanently
    identify each set in Scryfall's database. This is the canonical way to
    retrieve sets.

    Args:
        id: The Scryfall UUID for the set (required).

    Example:
        set_obj = scrython.sets.ById(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')
        print(f"{set_obj.name} ({set_obj.code})")

    See: https://scryfall.com/docs/api/sets/id
    """

    _endpoint = "/sets/:id"
