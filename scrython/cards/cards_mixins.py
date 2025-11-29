from functools import cache
from typing import Any

from ..types import (
    ImageUris,
    Legalities,
    Prices,
    PurchaseUris,
    RelatedUris,
)
from ..utils import to_object_array


class CoreFieldsMixin:
    _scryfall_data: dict[str, Any]

    @property
    def arena_id(self) -> int | None:
        """
        This card's Arena ID, if any. A large percentage of cards are not available on Arena.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("arena_id")

    @property
    def card_id(self) -> str:
        """
        A unique identifier within Scryfall's database.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def lang(self) -> str:
        """
        A language code for this printing.

        Type: String (Required)
        """
        return self._scryfall_data["lang"]

    @property
    def mtgo_id(self) -> int | None:
        """
        Magic Online catalog identifier when available.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("mtgo_id")

    @property
    def mtgo_foil_id(self) -> int | None:
        """
        Foil variant identifier for Magic Online.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("mtgo_foil_id")

    @property
    def multiverse_ids(self) -> list[int] | None:
        """
        This card's multiverse IDs on Gatherer, if any, as an array.

        Type: Array of Integers (Nullable)
        """
        return self._scryfall_data.get("multiverse_ids")

    @property
    def tcgplayer_id(self) -> int | None:
        """
        TCGplayer product identifier.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("tcgplayer_id")

    @property
    def tcgplayer_etched_id(self) -> int | None:
        """
        TCGplayer etched version identifier.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("tcgplayer_etched_id")

    @property
    def cardmarket_id(self) -> int | None:
        """
        Cardmarket API identifier.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("cardmarket_id")

    @property
    def object(self) -> str:
        """
        Content type, always "card".

        Type: String (Required)
        """
        return "card"

    @property
    def layout(self) -> str:
        """
        A code for this card's layout.

        Type: String (Required)
        """
        return self._scryfall_data["layout"]

    @property
    def oracle_id(self) -> str | None:
        """
        Consistent ID across reprints of same card.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("oracle_id")

    @property
    def prints_search_uri(self) -> str:
        """
        Link to all reprints via API.

        Type: URI (Required)
        """
        return self._scryfall_data["prints_search_uri"]

    @property
    def rulings_uri(self) -> str:
        """
        Link to card's rulings list.

        Type: URI (Required)
        """
        return self._scryfall_data["rulings_uri"]

    @property
    def scryfall_uri(self) -> str:
        """
        Permanent webpage link.

        Type: URI (Required)
        """
        return self._scryfall_data["scryfall_uri"]

    @property
    def uri(self) -> str:
        """
        API object link.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]


class GameplayFieldsMixin:
    _scryfall_data: dict[str, Any]

    @property
    @cache
    def all_parts(self) -> list[Any] | None:
        """
        Related Card Objects for closely connected cards.

        Type: Array (Nullable)
        """

        class RelatedCardObject(RelatedCardsObjectMixin):
            def __init__(self, data):
                self._scryfall_data = data

        return to_object_array(RelatedCardObject, "all_parts", self._scryfall_data)

    @property
    @cache
    def card_faces(self) -> list[Any] | None:
        """
        Array of Card Face objects for multifaced cards.

        Type: Array (Nullable)
        """

        class CardFaceObject(CardFaceMixin):
            def __init__(self, data):
                self._scryfall_data = data

        return to_object_array(CardFaceObject, "card_faces", self._scryfall_data)

    @property
    def cmc(self) -> float:
        """
        The card's mana value.

        Type: Decimal (Required)
        """
        return self._scryfall_data["cmc"]

    @property
    def color_identity(self) -> list[str]:
        """
        This card's color identity.

        Type: Colors (Required)
        """
        return self._scryfall_data["color_identity"]

    @property
    def color_indicator(self) -> list[str] | None:
        """
        Colors indicated on the card face.

        Type: Colors (Nullable)
        """
        return self._scryfall_data.get("color_indicator")

    @property
    def colors(self) -> list[str] | None:
        """
        Card's colors per game rules.

        Type: Colors (Nullable)
        """
        return self._scryfall_data.get("colors")

    @property
    def defense(self) -> str | None:
        """
        Defense value if applicable.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("defense")

    @property
    def edhrec_rank(self) -> int | None:
        """
        EDHREC popularity ranking.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("edhrec_rank")

    @property
    def game_changer(self) -> bool | None:
        """
        True if this card is on the Commander Game Changer list.

        Type: Boolean (Nullable)
        """
        return self._scryfall_data.get("game_changer")

    @property
    def hand_modifier(self) -> str | None:
        """
        Vanguard card hand delta value.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("hand_modifier")

    @property
    def keywords(self) -> list[str]:
        """
        Array of keywords that this card uses, such as Flying.

        Type: Array (Required)
        """
        return self._scryfall_data["keywords"]

    @property
    def legalities(self) -> Legalities:
        """
        Format legality across play modes.

        Type: Object (Required)
        """
        return self._scryfall_data["legalities"]

    @property
    def life_modifier(self) -> str | None:
        """
        Vanguard card life delta value.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("life_modifier")

    @property
    def loyalty(self) -> str | None:
        """
        Planeswalker loyalty value.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("loyalty")

    @property
    def mana_cost(self) -> str | None:
        """
        The mana cost for this card. This value will be any empty string if the cost is absent.

        Type: String (Nullable)

        Example: "{3}{U}{U}"
        """
        return self._scryfall_data.get("mana_cost")

    @property
    def name(self) -> str:
        """
        Card name; multiface cards show both names separated.

        Type: String (Required)
        """
        return self._scryfall_data["name"]

    @property
    def oracle_text(self) -> str | None:
        """
        Official card ability text.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("oracle_text")

    @property
    def penny_rank(self) -> int | None:
        """
        Penny Dreadful format ranking.

        Type: Integer (Nullable)
        """
        return self._scryfall_data.get("penny_rank")

    @property
    def power(self) -> str | None:
        """
        Creature power value.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("power")

    @property
    def produced_mana(self) -> list[str] | None:
        """
        Mana colors the card can generate.

        Type: Colors (Nullable)
        """
        return self._scryfall_data.get("produced_mana")

    @property
    def reserved(self) -> bool:
        """
        True if this card is on the Reserved List.

        Type: Boolean (Required)
        """
        return self._scryfall_data["reserved"]

    @property
    def toughness(self) -> str | None:
        """
        Creature toughness value.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("toughness")

    @property
    def type_line(self) -> str:
        """
        The type line of this card.

        Type: String (Required)

        Example: "Legendary Creature — Human Wizard"
        """
        return self._scryfall_data["type_line"]


class PrintFieldsMixin:
    _scryfall_data: dict[str, Any]

    @property
    def artist(self) -> str | None:
        """
        The name of the illustrator of this card. Newly spoiled cards may not have this field yet.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("artist")

    @property
    def artist_ids(self) -> list[str] | None:
        """
        The IDs of the artists that illustrated this card. Newly spoiled cards may not have this field yet.

        Type: Array of UUIDs (Nullable)
        """
        return self._scryfall_data.get("artist_ids")

    @property
    def attraction_lights(self) -> list[int] | None:
        """
        The lit Unfinity attractions lights on this card, if any.

        Type: Array (Nullable)
        """
        return self._scryfall_data.get("attraction_lights")

    @property
    def booster(self) -> bool:
        """
        Whether this card is found in boosters.

        Type: Boolean (Required)
        """
        return self._scryfall_data["booster"]

    @property
    def border_color(self) -> str:
        """
        This card's border color: black, white, borderless, yellow, silver, or gold.

        Type: String (Required)
        """
        return self._scryfall_data["border_color"]

    @property
    def card_back_id(self) -> str | None:
        """
        The Scryfall ID for the card back design present on this card.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("card_back_id")

    @property
    def collector_number(self) -> str:
        """
        This card's collector number. Note that collector numbers can contain non-numeric characters, such as letters or ★.

        Type: String (Required)
        """
        return self._scryfall_data["collector_number"]

    @property
    def content_warning(self) -> bool | None:
        """
        True if you should consider avoiding use of this print downstream.

        Type: Boolean (Nullable)
        """
        return self._scryfall_data.get("content_warning")

    @property
    def digital(self) -> bool:
        """
        True if this card was only released in a video game.

        Type: Boolean (Required)
        """
        return self._scryfall_data["digital"]

    @property
    def finishes(self) -> list[str]:
        """
        An array of computer-readable flags that indicate if this card can come in foil, nonfoil, or etched finishes.

        Type: Array of Strings (Required)
        """
        return self._scryfall_data["finishes"]

    @property
    def flavor_name(self) -> str | None:
        """
        The just-for-fun name printed on the card (such as for Godzilla series cards).

        Type: String (Nullable)
        """
        return self._scryfall_data.get("flavor_name")

    @property
    def flavor_text(self) -> str | None:
        """
        The flavor text, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("flavor_text")

    @property
    def frame_effects(self) -> list[str] | None:
        """
        This card's frame effects, if any.

        Type: Array of Strings (Nullable)
        """
        return self._scryfall_data.get("frame_effects")

    @property
    def frame(self) -> str:
        """
        This card's frame layout.

        Type: String (Required)
        """
        return self._scryfall_data["frame"]

    @property
    def full_art(self) -> bool:
        """
        True if this card's artwork is larger than normal.

        Type: Boolean (Required)
        """
        return self._scryfall_data["full_art"]

    @property
    def games(self) -> list[str]:
        """
        A list of games that this card print is available in, paper, arena, and/or mtgo.

        Type: Array of Strings (Required)
        """
        return self._scryfall_data["games"]

    @property
    def highres_image(self) -> bool:
        """
        True if this card's imagery is high resolution.

        Type: Boolean (Required)
        """
        return self._scryfall_data["highres_image"]

    @property
    def illustration_id(self) -> str | None:
        """
        A unique identifier for the card artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("illustration_id")

    @property
    def image_status(self) -> str:
        """
        A computer-readable indicator for the state of this card's image, one of missing, placeholder, lowres, or highres_scan.

        Type: String (Required)
        """
        return self._scryfall_data["image_status"]

    @property
    def image_uris(self) -> ImageUris | None:
        """
        An object listing available imagery for this card.

        Type: Object (Nullable)
        """
        return self._scryfall_data.get("image_uris")

    @property
    def oversized(self) -> bool:
        """
        True if this card is oversized.

        Type: Boolean (Required)
        """
        return self._scryfall_data["oversized"]

    @property
    def prices(self) -> Prices:
        """
        An object containing daily price information for this card, including usd, usd_foil, usd_etched, eur, eur_foil, eur_etched, and tix prices, as strings.

        Type: Object (Required)

        Note: Prices should be considered dangerously stale after 24 hours.
        """
        return self._scryfall_data["prices"]

    @property
    def printed_name(self) -> str | None:
        """
        The localized name printed on this card, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("printed_name")

    @property
    def printed_text(self) -> str | None:
        """
        The localized text printed on this card, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("printed_text")

    @property
    def printed_type_line(self) -> str | None:
        """
        The localized type line printed on this card, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("printed_type_line")

    @property
    def promo(self) -> bool:
        """
        True if this card is a promotional print.

        Type: Boolean (Required)
        """
        return self._scryfall_data["promo"]

    @property
    def promo_types(self) -> list[str] | None:
        """
        An array of strings describing what categories of promo cards this card falls into.

        Type: Array of Strings (Nullable)
        """
        return self._scryfall_data.get("promo_types")

    @property
    def purchase_uris(self) -> PurchaseUris | None:
        """
        An object providing URIs to this card's listing on major marketplaces. Omitted if the card is unpurchaseable.

        Type: Object (Nullable)
        """
        return self._scryfall_data.get("purchase_uris")

    @property
    def rarity(self) -> str:
        """
        This card's rarity. One of common, uncommon, rare, special, mythic, or bonus.

        Type: String (Required)
        """
        return self._scryfall_data["rarity"]

    @property
    def related_uris(self) -> RelatedUris:
        """
        An object providing URIs to this card's listing on other Magic resources.

        Type: Object (Required)
        """
        return self._scryfall_data["related_uris"]

    @property
    def released_at(self) -> str:
        """
        The date this card was first released.

        Type: Date (Required)
        """
        return self._scryfall_data["released_at"]

    @property
    def reprint(self) -> bool:
        """
        True if this card is a reprint.

        Type: Boolean (Required)
        """
        return self._scryfall_data["reprint"]

    @property
    def scryfall_set_uri(self) -> str:
        """
        A link to this card's set on Scryfall's website.

        Type: URI (Required)
        """
        return self._scryfall_data["scryfall_set_uri"]

    @property
    def set_name(self) -> str:
        """
        This card's full set name.

        Type: String (Required)
        """
        return self._scryfall_data["set_name"]

    @property
    def set_search_uri(self) -> str:
        """
        A link to where you can begin paginating this card's set on the Scryfall API.

        Type: URI (Required)
        """
        return self._scryfall_data["set_search_uri"]

    @property
    def set_type(self) -> str:
        """
        The type of set this printing is in.

        Type: String (Required)
        """
        return self._scryfall_data["set_type"]

    @property
    def set_uri(self) -> str:
        """
        A link to this card's set object on Scryfall's API.

        Type: URI (Required)
        """
        return self._scryfall_data["set_uri"]

    @property
    def set(self) -> str:
        """
        This card's set code.

        Type: String (Required)
        """
        return self._scryfall_data["set"]

    @property
    def set_id(self) -> str:
        """
        This card's Set object UUID.

        Type: UUID (Required)
        """
        return self._scryfall_data["set_id"]

    @property
    def story_spotlight(self) -> bool:
        """
        True if this card is a Story Spotlight.

        Type: Boolean (Required)
        """
        return self._scryfall_data["story_spotlight"]

    @property
    def textless(self) -> bool:
        """
        True if the card is printed without text.

        Type: Boolean (Required)
        """
        return self._scryfall_data["textless"]

    @property
    def variation(self) -> bool:
        """
        Whether this card is a variation of another printing.

        Type: Boolean (Required)
        """
        return self._scryfall_data["variation"]

    @property
    def variation_of(self) -> str | None:
        """
        The printing ID of the printing this card is a variation of.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("variation_of")

    @property
    def security_stamp(self) -> str | None:
        """
        The security stamp on this card, if any. One of oval, triangle, acorn, circle, arena, or heart.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("security_stamp")

    @property
    def watermark(self) -> str | None:
        """
        This card's watermark, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("watermark")

    @property
    def previewed_at(self) -> str | None:
        """
        The date this card was previewed.

        Type: Date (Nullable)
        """
        if preview := self._scryfall_data.get("preview"):
            return preview.get("previewed_at")
        return None

    @property
    def preview_source_uri(self) -> str | None:
        """
        A link to the preview for this card.

        Type: URI (Nullable)
        """
        if preview := self._scryfall_data.get("preview"):
            return preview.get("source_uri")
        return None

    @property
    def preview_source(self) -> str | None:
        """
        The name of the source that previewed this card.

        Type: String (Nullable)
        """
        if preview := self._scryfall_data.get("preview"):
            return preview.get("source")
        return None


class CardFaceMixin:
    _scryfall_data: dict[str, Any]

    @property
    def artist(self) -> str | None:
        """
        The name of the illustrator of this card face. Newly spoiled cards may not have this field yet.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("artist")

    @property
    def artist_id(self) -> str | None:
        """
        The ID of the illustrator of this card face. Newly spoiled cards may not have this field yet.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("artist_id")

    @property
    def cmc(self) -> float | None:
        """
        The mana value of this particular face, if the card is reversible.

        Type: Decimal (Nullable)
        """
        return self._scryfall_data.get("cmc")

    @property
    def color_indicator(self) -> list[str] | None:
        """
        The colors in this face's color indicator, if any.

        Type: Colors (Nullable)
        """
        return self._scryfall_data.get("color_indicator")

    @property
    def colors(self) -> list[str] | None:
        """
        This face's colors, if the game defines colors for the individual face of this card.

        Type: Colors (Nullable)
        """
        return self._scryfall_data.get("colors")

    @property
    def defense(self) -> str | None:
        """
        This face's defense, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("defense")

    @property
    def flavor_text(self) -> str | None:
        """
        The flavor text printed on this face, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("flavor_text")

    @property
    def illustration_id(self) -> str | None:
        """
        A unique identifier for the card face artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("illustration_id")

    @property
    def image_uris(self) -> ImageUris | None:
        """
        An object providing URIs to imagery for this face, if this is a double-sided card.

        Type: Object (Nullable)
        """
        return self._scryfall_data.get("image_uris")

    @property
    def layout(self) -> str | None:
        """
        The layout of this card face, if the card is reversible.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("layout")

    @property
    def loyalty(self) -> str | None:
        """
        This face's loyalty, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("loyalty")

    @property
    def mana_cost(self) -> str | None:
        """
        The mana cost for this face. This value will be any empty string "" if the cost is absent.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("mana_cost")

    @property
    def name(self) -> str:
        """
        The name of this particular face.

        Type: String (Required)
        """
        return self._scryfall_data["name"]

    @property
    def object(self) -> str:
        """
        A content type for this object, always card_face.

        Type: String (Required)
        """
        return self._scryfall_data["object"]

    @property
    def oracle_id(self) -> str | None:
        """
        The Oracle ID of this particular face, if the card is reversible.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("oracle_id")

    @property
    def oracle_text(self) -> str | None:
        """
        The Oracle text for this face, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("oracle_text")

    @property
    def power(self) -> str | None:
        """
        This face's power, if any. Note that some cards have powers that are not numeric, such as *.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("power")

    @property
    def printed_name(self) -> str | None:
        """
        The localized name printed on this face, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("printed_name")

    @property
    def printed_text(self) -> str | None:
        """
        The localized text printed on this face, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("printed_text")

    @property
    def printed_type_line(self) -> str | None:
        """
        The localized type line printed on this face, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("printed_type_line")

    @property
    def toughness(self) -> str | None:
        """
        This face's toughness, if any. Note that some cards have toughnesses that are not numeric, such as *.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("toughness")

    @property
    def type_line(self) -> str | None:
        """
        The type line of this particular face, if the card is reversible.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("type_line")

    @property
    def watermark(self) -> str | None:
        """
        The watermark on this particular card face, if any.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("watermark")


class RelatedCardsObjectMixin:
    _scryfall_data: dict[str, Any]

    @property
    def id(self) -> str:
        """
        An unique ID for this card in Scryfall's database.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def object(self) -> str:
        """
        A content type for this object, always related_card.

        Type: String (Required)
        """
        return self._scryfall_data["object"]

    @property
    def component(self) -> str:
        """
        A field explaining what role this card plays in this relationship, one of token, meld_part, meld_result, or combo_piece.

        Type: String (Required)
        """
        return self._scryfall_data["component"]

    @property
    def name(self) -> str:
        """
        The name of this particular related card.

        Type: String (Required)
        """
        return self._scryfall_data["name"]

    @property
    def type_line(self) -> str:
        """
        The type line of this card.

        Type: String (Required)
        """
        return self._scryfall_data["type_line"]

    @property
    def uri(self) -> str:
        """
        A URI where you can retrieve a full object describing this card on Scryfall's API.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]


class CardsObjectMixin(CoreFieldsMixin, GameplayFieldsMixin, PrintFieldsMixin):
    """Convenience methods for card objects."""

    def is_legal_in(self, format_name: str) -> bool:
        """
        Check if card is legal in a specific format.

        Args:
            format_name: Format name (e.g., 'commander', 'modern', 'standard')

        Returns:
            True if card is legal in the format, False otherwise

        Example:
            card = scrython.cards.Named(fuzzy='Lightning Bolt')
            if card.is_legal_in('commander'):
                print('Legal in Commander!')
        """
        legalities = self._scryfall_data.get("legalities", {})
        return legalities.get(format_name.lower()) == "legal"

    def has_color(self, color: str) -> bool:
        """
        Check if card contains a specific color.

        Args:
            color: Single letter color code ('W', 'U', 'B', 'R', 'G')

        Returns:
            True if card has the color, False otherwise

        Example:
            card = scrython.cards.Named(fuzzy='Lightning Bolt')
            if card.has_color('R'):
                print('Red card!')
        """
        colors = self._scryfall_data.get("colors", [])
        return color.upper() in colors

    @property
    def is_creature(self) -> bool:
        """Check if card is a creature."""
        type_line = self._scryfall_data.get("type_line", "")
        return "Creature" in type_line

    @property
    def is_instant(self) -> bool:
        """Check if card is an instant."""
        type_line = self._scryfall_data.get("type_line", "")
        return "Instant" in type_line

    @property
    def is_sorcery(self) -> bool:
        """Check if card is a sorcery."""
        type_line = self._scryfall_data.get("type_line", "")
        return "Sorcery" in type_line

    @property
    def is_enchantment(self) -> bool:
        """Check if card is an enchantment."""
        type_line = self._scryfall_data.get("type_line", "")
        return "Enchantment" in type_line

    @property
    def is_artifact(self) -> bool:
        """Check if card is an artifact."""
        type_line = self._scryfall_data.get("type_line", "")
        return "Artifact" in type_line

    @property
    def is_planeswalker(self) -> bool:
        """Check if card is a planeswalker."""
        type_line = self._scryfall_data.get("type_line", "")
        return "Planeswalker" in type_line

    def lowest_price(self) -> float | None:
        """
        Return the lowest non-None price across all price types.

        Returns:
            Lowest price in USD, or None if no prices available

        Example:
            card = scrython.cards.Named(fuzzy='Lightning Bolt')
            cheapest = card.lowest_price()
            if cheapest:
                print(f'Cheapest: ${cheapest:.2f}')
        """
        prices = self._scryfall_data.get("prices", {})
        valid_prices = []

        for price_str in prices.values():
            if price_str is not None:
                try:
                    valid_prices.append(float(price_str))
                except (ValueError, TypeError):
                    continue

        return min(valid_prices) if valid_prices else None

    def highest_price(self) -> float | None:
        """
        Return the highest non-None price across all price types.

        Returns:
            Highest price in USD, or None if no prices available

        Example:
            card = scrython.cards.Named(fuzzy='Black Lotus')
            most_expensive = card.highest_price()
            if most_expensive:
                print(f'Most expensive: ${most_expensive:.2f}')
        """
        prices = self._scryfall_data.get("prices", {})
        valid_prices = []

        for price_str in prices.values():
            if price_str is not None:
                try:
                    valid_prices.append(float(price_str))
                except (ValueError, TypeError):
                    continue

        return max(valid_prices) if valid_prices else None

    def get_image_url(self, size: str = "normal") -> str | None:
        """
        Get image URL for the card, handling double-faced cards.

        Args:
            size: Image size ('small', 'normal', 'large', 'png', 'art_crop', 'border_crop')

        Returns:
            Image URL or None if not available

        Example:
            card = scrython.cards.Named(fuzzy='Lightning Bolt')
            url = card.get_image_url(size='large')
            if url:
                print(f'Image: {url}')
        """
        # Check for image_uris at top level first
        image_uris = self._scryfall_data.get("image_uris")
        if image_uris and size in image_uris:
            return image_uris[size]

        # For double-faced cards, check card_faces
        card_faces = self._scryfall_data.get("card_faces")
        if card_faces and len(card_faces) > 0:
            front_face = card_faces[0]
            face_images = front_face.get("image_uris")
            if face_images and size in face_images:
                return face_images[size]

        return None
