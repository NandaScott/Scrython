"""
Type definitions for tagger.scryfall.com GraphQL API responses.

This module contains TypedDict definitions for card data, edge data
(tags and relationships), and tag catalog data from the Scryfall Tagger.
"""

import sys
from typing import Any, TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


class TaggerCardData(TypedDict):
    """Card data returned by tagger GraphQL queries."""

    id: str
    name: str
    oracleId: str
    printingId: str
    illustrationId: str
    displayName: NotRequired[str]
    artist: NotRequired[str]
    collectorNumber: NotRequired[str]
    layout: NotRequired[str]
    scryfallUrl: NotRequired[str]
    edges: NotRequired[list["TaggerEdgeData"]]


class TaggerEdgeData(TypedDict):
    """
    Edge data from tagger GraphQL (tags and relationships).

    Edges can be of type TAGGING or RELATIONSHIP, distinguished by
    the classifier field. Tag edges have classifiers like
    ORACLE_CARD_TAG, PRINTING_TAG, or ILLUSTRATION_TAG.
    Relationship edges have classifiers like SIMILAR_TO, REFERENCES_TO, etc.
    """

    classifier: str  # One of EdgeClassifier enum values
    type: str  # "TAGGING" or "RELATIONSHIP"
    name: str  # Tag name or relationship label
    namespace: NotRequired[str]
    annotation: NotRequired[str]
    metadata: NotRequired[str]
    id: NotRequired[str]
    subjectId: NotRequired[str]
    subjectName: NotRequired[str]
    relatedId: NotRequired[str]
    relatedName: NotRequired[str]


class TaggerTagData(TypedDict):
    """Tag type data from tagger GraphQL queries."""

    id: str
    name: str
    namespace: str
    description: NotRequired[str]
    category: bool  # True if this is a tag category/container
    alias: NotRequired[bool]
    ancestorTags: NotRequired[list[Any]]
    parentTags: NotRequired[list[Any]]
    childTags: NotRequired[list[Any]]
    descendants: NotRequired[list[Any]]
    aliases: NotRequired[list[Any]]
    hierarchy: NotRequired[list[Any]]
    hasExemplaryTagging: NotRequired[bool]


class TaggerCardTagsResponse(TypedDict):
    """
    Top-level response wrapper for a card's tags.

    Contains both the card metadata and the filtered lists of tags
    by classification type.
    """

    card: TaggerCardData
    oracle_card_tags: NotRequired[list[TaggerEdgeData]]
    printing_tags: NotRequired[list[TaggerEdgeData]]
    illustration_tags: NotRequired[list[TaggerEdgeData]]
    relationships: NotRequired[list[TaggerEdgeData]]


class TaggerTagSearchResult(TypedDict):
    """A single result from a tag search query."""

    id: str
    name: str
    namespace: str
    description: str | None
    category: bool
