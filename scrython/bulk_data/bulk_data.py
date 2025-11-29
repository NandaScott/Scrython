from ..base import ScrythonRequestHandler
from ..base_mixins import ScryfallListMixin
from ..types import ScryfallBulkDataData
from .bulk_data_mixins import BulkDataObjectMixin


class Object(BulkDataObjectMixin):
    """
    Wrapper class for individual bulk data objects from Scryfall API responses.

    Provides access to all bulk data properties through BulkDataObjectMixin.
    """

    _scryfall_data: ScryfallBulkDataData  # type: ignore[assignment]

    def __init__(self, data: ScryfallBulkDataData) -> None:
        self._scryfall_data = data


class All(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get information about all available bulk data files.

    Endpoint: GET /bulk-data

    Returns a list of all Bulk Data objects. Scryfall provides bulk data files
    containing complete datasets of cards, rulings, and other information. These
    files are updated approximately every 12 hours.

    Example:
        # Get all bulk data options
        all_bulk = scrython.bulk_data.All()

        # List available files
        for bulk in all_bulk.data:
            print(f"{bulk.name}: {bulk.description}")
            print(f"Size: {bulk.size / 1_000_000:.1f} MB")
            print(f"Download: {bulk.download_uri}")
            print()

    See: https://scryfall.com/docs/api/bulk-data
    """

    _endpoint = "/bulk-data"
    list_data_type = Object


class ById(BulkDataObjectMixin, ScrythonRequestHandler):
    """
    Get information about a specific bulk data file by its Scryfall ID.

    Endpoint: GET /bulk-data/:id

    Returns a single Bulk Data object. Use this to get download URIs and metadata
    for specific bulk data files.

    Args:
        id: The Scryfall UUID for the bulk data file (required).

    Example:
        bulk = scrython.bulk_data.ById(id='uuid-here')
        print(f"File: {bulk.name}")
        print(f"Last updated: {bulk.updated_at}")
        print(f"Download from: {bulk.download_uri}")

    See: https://scryfall.com/docs/api/bulk-data/id
    """

    _endpoint = "/bulk-data/:id"


class ByType(BulkDataObjectMixin, ScrythonRequestHandler):
    """
    Get information about a specific bulk data file by its type.

    Endpoint: GET /bulk-data/:type

    Returns a single Bulk Data object for the specified type. This is the most
    convenient way to access standard bulk data files like oracle cards or
    default cards.

    Args:
        type: The bulk data type (required).
            Common types: 'oracle_cards', 'unique_artwork', 'default_cards',
                         'all_cards', 'rulings'

    Example:
        # Get Oracle Cards bulk data
        oracle = scrython.bulk_data.ByType(type='oracle_cards')
        print(f"Oracle Cards file: {oracle.name}")
        print(f"Size: {oracle.size / 1_000_000:.1f} MB")
        print(f"Updated: {oracle.updated_at}")

        # Download the file
        import requests
        response = requests.get(oracle.download_uri)
        cards = response.json()
        print(f"Downloaded {len(cards)} cards")

    See: https://scryfall.com/docs/api/bulk-data/type
    """

    _endpoint = "/bulk-data/:type"
