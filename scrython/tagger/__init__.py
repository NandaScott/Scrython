"""
Scryfall Tagger integration for Scrython.

Provides access to the community-driven Magic: The Gathering card
tagging database at tagger.scryfall.com via its GraphQL API.

All endpoint classes (CardTags, TagSearch, TagBySlug) inherit from
ScrythonRequestHandler, providing serialization (to_dict / to_json /
from_dict), magic methods (__eq__ / __hash__ / __repr__ / __str__),
rate limiting, and caching via the shared infrastructure.

TagObject wraps individual tag/edge data with dot-notation access
and supports serialization (to_dict / to_json / from_dict).

Card objects (scrython.cards) also provide tag integration via
get_tags(), get_tag_names(), and has_tag() convenience methods.

Main classes:
    CardTags   — Get all tags for a card by set code and collector number
    TagSearch  — Search or browse the tag database
    TagBySlug  — Look up a specific tag by its slug identifier
    TagObject  — Wrapper for individual tag/edge data with dot-notation access
    TaggerSession — Low-level GraphQL session manager (internal use)
"""

from .tagger import CardTags, TagBySlug, TagSearch
from .tagger_graphql import TaggerSession
from .tagger_mixins import TagObject

__all__ = [
    "CardTags",
    "TagSearch",
    "TagBySlug",
    "TagObject",
    "TaggerSession",
]
