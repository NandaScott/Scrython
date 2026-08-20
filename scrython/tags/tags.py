from ..types import ScryfallTagData, ScryfallTaggingData
from .tags_mixins import TaggingObjectMixin, TagObjectMixin


class Tagging(TaggingObjectMixin):
    """
    Wrapper class for individual tagging objects nested within a Tag.

    A tagging links a tag to a single card, by illustration for art tags or by
    oracle identity for oracle tags. Provides access to all tagging properties
    through TaggingObjectMixin.
    """

    def __init__(self, data: ScryfallTaggingData) -> None:
        self._scryfall_data = data


class Object(TagObjectMixin):
    """
    Wrapper class for individual tag objects from the Scryfall bulk files.

    Tags are not served from a dedicated API endpoint. Download the art_tags or
    oracle_tags bulk file through the generic bulk_data path, then wrap each entry:

        bulk = scrython.bulk_data.ByType(type="oracle_tags")
        tags = [scrython.tags.Object(t) for t in bulk.download()]

    Provides access to all tag properties through TagObjectMixin.
    """

    def __init__(self, data: ScryfallTagData) -> None:
        self._scryfall_data = data
