"""
Type definitions for Scryfall API responses.

This module contains TypedDict definitions for all Scryfall API objects,
providing strong typing for card, set, and bulk data structures.
"""

from typing import Any, TypedDict

from typing_extensions import NotRequired

# Type aliases for common Scryfall types
UUID = str
URI = str
Colors = list[str]
Date = str  # ISO 8601 date string


class ImageUris(TypedDict, total=False):
    """Image URIs for different card image sizes."""

    png: str
    border_crop: str
    art_crop: str
    large: str
    normal: str
    small: str


class Prices(TypedDict, total=False):
    """Price information in various currencies."""

    usd: str | None
    usd_foil: str | None
    usd_etched: str | None
    eur: str | None
    eur_foil: str | None
    tix: str | None


class PurchaseUris(TypedDict, total=False):
    """URIs to purchase the card from various vendors."""

    tcgplayer: str
    cardmarket: str
    cardhoarder: str


class RelatedUris(TypedDict, total=False):
    """URIs to related resources."""

    gatherer: str
    tcgplayer_infinite_articles: str
    tcgplayer_infinite_decks: str
    edhrec: str


class Legalities(TypedDict, total=False):
    """Format legality information."""

    standard: str
    future: str
    historic: str
    timeless: str
    gladiator: str
    pioneer: str
    explorer: str
    modern: str
    legacy: str
    pauper: str
    vintage: str
    penny: str
    commander: str
    oathbreaker: str
    standardbrawl: str
    brawl: str
    alchemy: str
    paupercommander: str
    duel: str
    oldschool: str
    premodern: str
    predh: str


class CardFaceData(TypedDict):
    """Data for a single face of a multi-faced card."""

    object: str
    name: str
    type_line: str
    oracle_text: NotRequired[str]
    mana_cost: NotRequired[str]
    colors: NotRequired[Colors]
    color_indicator: NotRequired[Colors]
    power: NotRequired[str]
    toughness: NotRequired[str]
    loyalty: NotRequired[str]
    defense: NotRequired[str]
    flavor_text: NotRequired[str]
    flavor_name: NotRequired[str]
    artist: NotRequired[str]
    artist_id: NotRequired[UUID]
    illustration_id: NotRequired[UUID]
    image_uris: NotRequired[ImageUris]
    watermark: NotRequired[str]


class RelatedCard(TypedDict):
    """Information about a related card (combo pieces, tokens, etc.)."""

    object: str
    id: UUID
    component: str
    name: str
    type_line: str
    uri: URI


class Preview(TypedDict):
    """Preview information for upcoming cards."""

    source: str
    source_uri: URI
    previewed_at: Date


class ScryfallCardData(TypedDict):
    """
    Complete TypedDict for a Scryfall Card object.

    See: https://scryfall.com/docs/api/cards
    """

    # Core required fields
    id: UUID
    object: str
    lang: str
    layout: str
    prints_search_uri: URI
    rulings_uri: URI
    scryfall_uri: URI
    uri: URI

    # Core optional fields
    arena_id: NotRequired[int]
    mtgo_id: NotRequired[int]
    mtgo_foil_id: NotRequired[int]
    multiverse_ids: NotRequired[list[int]]
    tcgplayer_id: NotRequired[int]
    tcgplayer_etched_id: NotRequired[int]
    cardmarket_id: NotRequired[int]
    oracle_id: NotRequired[UUID]

    # Gameplay required fields
    name: str
    type_line: str
    cmc: float
    color_identity: Colors
    keywords: list[str]
    legalities: Legalities
    reserved: bool

    # Gameplay optional fields
    all_parts: NotRequired[list[RelatedCard]]
    card_faces: NotRequired[list[CardFaceData]]
    color_indicator: NotRequired[Colors]
    colors: NotRequired[Colors]
    defense: NotRequired[str]
    edhrec_rank: NotRequired[int]
    hand_modifier: NotRequired[str]
    life_modifier: NotRequired[str]
    loyalty: NotRequired[str]
    mana_cost: NotRequired[str]
    oracle_text: NotRequired[str]
    penny_rank: NotRequired[int]
    power: NotRequired[str]
    produced_mana: NotRequired[Colors]
    toughness: NotRequired[str]

    # Print required fields
    booster: bool
    border_color: str
    card_back_id: UUID
    collector_number: str
    digital: bool
    finishes: list[str]
    frame: str
    full_art: bool
    games: list[str]
    highres_image: bool
    image_status: str
    prices: Prices
    promo: bool
    rarity: str
    related_uris: RelatedUris
    released_at: Date
    reprint: bool
    scryfall_set_uri: URI
    set_name: str
    set_search_uri: URI
    set_type: str
    set_uri: URI
    set: str
    set_id: UUID
    story_spotlight: bool
    textless: bool
    variation: bool

    # Print optional fields
    artist: NotRequired[str]
    artist_ids: NotRequired[list[UUID]]
    attraction_lights: NotRequired[list[int]]
    content_warning: NotRequired[bool]
    flavor_name: NotRequired[str]
    flavor_text: NotRequired[str]
    frame_effects: NotRequired[list[str]]
    illustration_id: NotRequired[UUID]
    image_uris: NotRequired[ImageUris]
    oversized: NotRequired[bool]
    preview: NotRequired[Preview]
    printed_name: NotRequired[str]
    printed_text: NotRequired[str]
    printed_type_line: NotRequired[str]
    promo_types: NotRequired[list[str]]
    purchase_uris: NotRequired[PurchaseUris]
    security_stamp: NotRequired[str]
    variation_of: NotRequired[UUID]
    watermark: NotRequired[str]


class ScryfallSetData(TypedDict):
    """
    Complete TypedDict for a Scryfall Set object.

    See: https://scryfall.com/docs/api/sets
    """

    # Required fields
    id: UUID
    code: str
    name: str
    uri: URI
    scryfall_uri: URI
    search_uri: URI
    released_at: Date | None
    set_type: str
    card_count: int
    digital: bool
    nonfoil_only: bool
    foil_only: bool
    icon_svg_uri: URI

    # Optional fields
    mtgo_code: NotRequired[str]
    tcgplayer_id: NotRequired[int]
    parent_set_code: NotRequired[str]
    block_code: NotRequired[str]
    block: NotRequired[str]


class ScryfallBulkDataData(TypedDict):
    """
    Complete TypedDict for a Scryfall Bulk Data object.

    See: https://scryfall.com/docs/api/bulk-data
    """

    id: UUID
    object: str
    type: str
    updated_at: str
    uri: URI
    name: str
    description: str
    download_uri: URI
    size: int
    content_type: str
    content_encoding: str


class ScryfallListData(TypedDict):
    """
    TypedDict for a Scryfall List object (paginated results).

    See: https://scryfall.com/docs/api/lists
    """

    object: str
    data: list[Any]
    has_more: bool
    next_page: NotRequired[URI]
    total_cards: NotRequired[int]
    warnings: NotRequired[list[str]]


class ScryfallCatalogData(TypedDict):
    """
    TypedDict for a Scryfall Catalog object.

    See: https://scryfall.com/docs/api/catalogs
    """

    object: str
    uri: URI
    total_values: int
    data: list[str]
