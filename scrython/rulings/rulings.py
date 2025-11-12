from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallListMixin

from .rulings_mixins import RulingsObjectMixin


class Object(RulingsObjectMixin):
    """
    Wrapper class for individual ruling objects from Scryfall API responses.

    Provides access to all ruling properties through RulingsObjectMixin.
    """

    def __init__(self, data):
        self._scryfall_data = data


class ById(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get rulings for a card by its Scryfall UUID.

    Endpoint: GET /cards/:id/rulings

    Returns a list of Ruling objects. Rulings represent official rules clarifications
    from Wizards of the Coast or explanatory notes from Scryfall.

    Args:
        id: The Scryfall UUID for the card (required).

    Example:
        # Get rulings for a specific card
        rulings = scrython.rulings.ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        # Iterate through rulings
        for ruling in rulings.data:
            print(f"{ruling.published_at}: {ruling.comment}")
            print(f"Source: {ruling.source}")

        # Check total number of rulings
        print(f"Total rulings: {len(rulings.data)}")

    See: https://scryfall.com/docs/api/rulings
    """

    _endpoint = "/cards/:id/rulings"
    list_data_type = Object


class ByMultiverseId(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get rulings for a card by its Multiverse ID.

    Endpoint: GET /cards/multiverse/:id/rulings

    Returns a list of Ruling objects. Multiverse IDs are identifiers used by
    Wizards of the Coast's Gatherer database.

    Args:
        id: The Multiverse ID for the card (required).

    Example:
        rulings = scrython.rulings.ByMultiverseId(id=3749)
        for ruling in rulings.data:
            print(f"{ruling.published_at}: {ruling.comment}")

    See: https://scryfall.com/docs/api/rulings
    """

    _endpoint = "/cards/multiverse/:id/rulings"
    list_data_type = Object


class ByMTGOId(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get rulings for a card by its MTGO ID.

    Endpoint: GET /cards/mtgo/:id/rulings

    Returns a list of Ruling objects. MTGO IDs are unique identifiers used in
    Magic: The Gathering Online.

    Args:
        id: The MTGO ID for the card (required).

    Example:
        rulings = scrython.rulings.ByMTGOId(id=54321)
        for ruling in rulings.data:
            if ruling.source == "wotc":
                print(f"Official ruling: {ruling.comment}")

    See: https://scryfall.com/docs/api/rulings
    """

    _endpoint = "/cards/mtgo/:id/rulings"
    list_data_type = Object


class ByArenaId(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get rulings for a card by its Arena ID.

    Endpoint: GET /cards/arena/:id/rulings

    Returns a list of Ruling objects. Arena IDs are unique identifiers used in
    Magic: The Gathering Arena.

    Args:
        id: The Arena ID for the card (required).

    Example:
        rulings = scrython.rulings.ByArenaId(id=67890)
        print(f"Found {len(rulings.data)} rulings")
        for ruling in rulings.data:
            print(ruling.comment)

    See: https://scryfall.com/docs/api/rulings
    """

    _endpoint = "/cards/arena/:id/rulings"
    list_data_type = Object


class ByCodeNumber(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get rulings for a card by its set code and collector number.

    Endpoint: GET /cards/:code/:number/rulings

    Returns a list of Ruling objects. This method identifies cards using their
    set code (e.g., "znr") and collector number (e.g., "241").

    Args:
        code: The three-to-six-letter set code (required).
        number: The collector number (required).

    Example:
        # Get rulings for Omnath from Zendikar Rising
        rulings = scrython.rulings.ByCodeNumber(code="znr", number="232")

        for ruling in rulings.data:
            print(f"[{ruling.published_at}] {ruling.comment}")

        # Filter by source
        wotc_rulings = [r for r in rulings.data if r.source == "wotc"]
        print(f"Official WotC rulings: {len(wotc_rulings)}")

    See: https://scryfall.com/docs/api/rulings
    """

    _endpoint = "/cards/:code/:number/rulings"
    list_data_type = Object


class Rulings:
    """
    Smart factory for Rulings API endpoints.

    Routes to the correct rulings endpoint based on provided kwargs.

    Supported parameters:
        - id: Scryfall UUID → ById
        - multiverse_id: Multiverse ID → ByMultiverseId
        - mtgo_id: MTGO ID → ByMTGOId
        - arena_id: Arena ID → ByArenaId
        - code + number: Set code and collector number → ByCodeNumber

    Example:
        # All these return ruling lists using different identifiers
        rulings1 = scrython.Rulings(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")
        rulings2 = scrython.Rulings(multiverse_id=3749)
        rulings3 = scrython.Rulings(mtgo_id=54321)
        rulings4 = scrython.Rulings(arena_id=67890)
        rulings5 = scrython.Rulings(code="m21", number="241")
    """

    def __new__(cls, **kwargs):
        if "id" in kwargs:
            return ById(**kwargs)
        elif "multiverse_id" in kwargs:
            # Map multiverse_id to id for the endpoint
            return ByMultiverseId(id=kwargs["multiverse_id"])
        elif "mtgo_id" in kwargs:
            # Map mtgo_id to id for the endpoint
            return ByMTGOId(id=kwargs["mtgo_id"])
        elif "arena_id" in kwargs:
            # Map arena_id to id for the endpoint
            return ByArenaId(id=kwargs["arena_id"])
        elif "code" in kwargs and "number" in kwargs:
            return ByCodeNumber(**kwargs)
        else:
            raise ValueError(
                "Invalid parameters for Rulings. Must provide one of: "
                "id, multiverse_id, mtgo_id, arena_id, or (code + number)"
            )
