"""
Scryfall Tagger integration for Scrython.

Provides access to the community-driven Magic: The Gathering card
tagging database at tagger.scryfall.com via its GraphQL API.

Main classes:
    CardTags  — Get all tags for a card by set code and collector number
    TagSearch — Search or browse the tag database
    TagBySlug — Look up a specific tag by its slug identifier
    TagObject — Wrapper for individual tag/edge data with dot-notation access
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
