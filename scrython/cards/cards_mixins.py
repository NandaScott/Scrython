from functools import cache
from typing import Any

from ..utils import to_object_array


class CoreFieldsMixin:
    scryfall_data: dict[str, Any]

    @property
    def arena_id(self):
        """
        This card's Arena ID, if any. A large percentage of cards are not available on Arena.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["arena_id"]

    @property
    def card_id(self):
        """
        A unique identifier within Scryfall's database.

        Type: UUID (Required)
        """
        return self.scryfall_data["id"]

    @property
    def lang(self):
        """
        A language code for this printing.

        Type: String (Required)
        """
        return self.scryfall_data["lang"]

    @property
    def mtgo_id(self):
        """
        Magic Online catalog identifier when available.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["mtgo_id"]

    @property
    def mtgo_foil_id(self):
        """
        Foil variant identifier for Magic Online.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["mtgo_foil_id"]

    @property
    def multiverse_ids(self):
        """
        This card's multiverse IDs on Gatherer, if any, as an array.

        Type: Array of Integers (Nullable)
        """
        return self.scryfall_data["multiverse_ids"]

    @property
    def tcgplayer_id(self):
        """
        TCGplayer product identifier.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["tcgplayer_id"]

    @property
    def tcgplayer_etched_id(self):
        """
        TCGplayer etched version identifier.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["tcgplayer_etched_id"]

    @property
    def cardmarket_id(self):
        """
        Cardmarket API identifier.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["cardmarket_id"]

    @property
    def object(self):
        """
        Content type, always "card".

        Type: String (Required)
        """
        return "card"

    @property
    def layout(self):
        """
        A code for this card's layout.

        Type: String (Required)
        """
        return self.scryfall_data["layout"]

    @property
    def oracle_id(self):
        """
        Consistent ID across reprints of same card.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["oracle_id"]

    @property
    def prints_search_uri(self):
        """
        Link to all reprints via API.

        Type: URI (Required)
        """
        return self.scryfall_data["prints_search_uri"]

    @property
    def rulings_uri(self):
        """
        Link to card's rulings list.

        Type: URI (Required)
        """
        return self.scryfall_data["rulings_uri"]

    @property
    def scryfall_uri(self):
        """
        Permanent webpage link.

        Type: URI (Required)
        """
        return self.scryfall_data["scryfall_uri"]

    @property
    def uri(self):
        """
        API object link.

        Type: URI (Required)
        """
        return self.scryfall_data["uri"]


class GameplayFieldsMixin:
    scryfall_data: dict[str, Any]

    @property
    @cache
    def all_parts(self):
        """
        Related Card Objects for closely connected cards.

        Type: Array (Nullable)
        """

        class RelatedCardObject(RelatedCardsObjectMixin):
            def __init__(self, data):
                self.scryfall_data = data

        return to_object_array(RelatedCardObject, "all_parts")

    @property
    @cache
    def card_faces(self):
        """
        Array of Card Face objects for multifaced cards.

        Type: Array (Nullable)
        """

        class CardFaceObject(CardFaceMixin):
            def __init__(self, data):
                self.scryfall_data = data

        return to_object_array(CardFaceObject, "card_faces")

    @property
    def cmc(self):
        """
        The card's mana value.

        Type: Decimal (Required)
        """
        return self.scryfall_data["cmc"]

    @property
    def color_identity(self):
        """
        This card's color identity.

        Type: Colors (Required)
        """
        return self.scryfall_data["color_identity"]

    @property
    def color_indicator(self):
        """
        Colors indicated on the card face.

        Type: Colors (Nullable)
        """
        return self.scryfall_data["color_indicator"]

    @property
    def colors(self):
        """
        Card's colors per game rules.

        Type: Colors (Nullable)
        """
        return self.scryfall_data["colors"]

    @property
    def defense(self):
        """
        Defense value if applicable.

        Type: String (Nullable)
        """
        return self.scryfall_data["defense"]

    @property
    def edhrec_rank(self):
        """
        EDHREC popularity ranking.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["edhrec_rank"]

    @property
    def game_changer(self):
        """
        True if this card is on the Commander Game Changer list.

        Type: Boolean (Nullable)
        """
        return self.scryfall_data["game_changer"]

    @property
    def hand_modifier(self):
        """
        Vanguard card hand delta value.

        Type: String (Nullable)
        """
        return self.scryfall_data["hand_modifier"]

    @property
    def keywords(self):
        """
        Array of keywords that this card uses, such as Flying.

        Type: Array (Required)
        """
        return self.scryfall_data["keywords"]

    @property
    def legalities(self):
        """
        Format legality across play modes.

        Type: Object (Required)
        """
        return self.scryfall_data["legalities"]

    @property
    def life_modifier(self):
        """
        Vanguard card life delta value.

        Type: String (Nullable)
        """
        return self.scryfall_data["life_modifier"]

    @property
    def loyalty(self):
        """
        Planeswalker loyalty value.

        Type: String (Nullable)
        """
        return self.scryfall_data["loyalty"]

    @property
    def mana_cost(self):
        """
        The mana cost for this card. This value will be any empty string if the cost is absent.

        Type: String (Nullable)

        Example: "{3}{U}{U}"
        """
        return self.scryfall_data["mana_cost"]

    @property
    def name(self):
        """
        Card name; multiface cards show both names separated.

        Type: String (Required)
        """
        return self.scryfall_data["name"]

    @property
    def oracle_text(self):
        """
        Official card ability text.

        Type: String (Nullable)
        """
        return self.scryfall_data["oracle_text"]

    @property
    def penny_rank(self):
        """
        Penny Dreadful format ranking.

        Type: Integer (Nullable)
        """
        return self.scryfall_data["penny_rank"]

    @property
    def power(self):
        """
        Creature power value.

        Type: String (Nullable)
        """
        return self.scryfall_data["power"]

    @property
    def produced_mana(self):
        """
        Mana colors the card can generate.

        Type: Colors (Nullable)
        """
        return self.scryfall_data["produced_mana"]

    @property
    def reserved(self):
        """
        True if this card is on the Reserved List.

        Type: Boolean (Required)
        """
        return self.scryfall_data["reserved"]

    @property
    def toughness(self):
        """
        Creature toughness value.

        Type: String (Nullable)
        """
        return self.scryfall_data["toughness"]

    @property
    def type_line(self):
        """
        The type line of this card.

        Type: String (Required)

        Example: "Legendary Creature — Human Wizard"
        """
        return self.scryfall_data["type_line"]


class PrintFieldsMixin:
    scryfall_data: dict[str, Any]

    @property
    def artist(self):
        """
        The name of the illustrator of this card. Newly spoiled cards may not have this field yet.

        Type: String (Nullable)
        """
        return self.scryfall_data["artist"]

    @property
    def artist_ids(self):
        """
        The IDs of the artists that illustrated this card. Newly spoiled cards may not have this field yet.

        Type: Array of UUIDs (Nullable)
        """
        return self.scryfall_data["artist_ids"]

    @property
    def attraction_lights(self):
        """
        The lit Unfinity attractions lights on this card, if any.

        Type: Array (Nullable)
        """
        return self.scryfall_data["attraction_lights"]

    @property
    def booster(self):
        """
        Whether this card is found in boosters.

        Type: Boolean (Required)
        """
        return self.scryfall_data["booster"]

    @property
    def border_color(self):
        """
        This card's border color: black, white, borderless, yellow, silver, or gold.

        Type: String (Required)
        """
        return self.scryfall_data["border_color"]

    @property
    def card_back_id(self):
        """
        The Scryfall ID for the card back design present on this card.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["card_back_id"]

    @property
    def collector_number(self):
        """
        This card's collector number. Note that collector numbers can contain non-numeric characters, such as letters or ★.

        Type: String (Required)
        """
        return self.scryfall_data["collector_number"]

    @property
    def content_warning(self):
        """
        True if you should consider avoiding use of this print downstream.

        Type: Boolean (Nullable)
        """
        return self.scryfall_data["content_warning"]

    @property
    def digital(self):
        """
        True if this card was only released in a video game.

        Type: Boolean (Required)
        """
        return self.scryfall_data["digital"]

    @property
    def finishes(self):
        """
        An array of computer-readable flags that indicate if this card can come in foil, nonfoil, or etched finishes.

        Type: Array of Strings (Required)
        """
        return self.scryfall_data["finishes"]

    @property
    def flavor_name(self):
        """
        The just-for-fun name printed on the card (such as for Godzilla series cards).

        Type: String (Nullable)
        """
        return self.scryfall_data["flavor_name"]

    @property
    def flavor_text(self):
        """
        The flavor text, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["flavor_text"]

    @property
    def frame_effects(self):
        """
        This card's frame effects, if any.

        Type: Array of Strings (Nullable)
        """
        return self.scryfall_data["frame_effects"]

    @property
    def frame(self):
        """
        This card's frame layout.

        Type: String (Required)
        """
        return self.scryfall_data["frame"]

    @property
    def full_art(self):
        """
        True if this card's artwork is larger than normal.

        Type: Boolean (Required)
        """
        return self.scryfall_data["full_art"]

    @property
    def games(self):
        """
        A list of games that this card print is available in, paper, arena, and/or mtgo.

        Type: Array of Strings (Required)
        """
        return self.scryfall_data["games"]

    @property
    def highres_image(self):
        """
        True if this card's imagery is high resolution.

        Type: Boolean (Required)
        """
        return self.scryfall_data["highres_image"]

    @property
    def illustration_id(self):
        """
        A unique identifier for the card artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["illustration_id"]

    @property
    def image_status(self):
        """
        A computer-readable indicator for the state of this card's image, one of missing, placeholder, lowres, or highres_scan.

        Type: String (Required)
        """
        return self.scryfall_data["image_status"]

    @property
    def image_uris(self):
        """
        An object listing available imagery for this card.

        Type: Object (Nullable)
        """
        return self.scryfall_data["image_uris"]

    @property
    def oversized(self):
        """
        True if this card is oversized.

        Type: Boolean (Required)
        """
        return self.scryfall_data["oversized"]

    @property
    def prices(self):
        """
        An object containing daily price information for this card, including usd, usd_foil, usd_etched, eur, eur_foil, eur_etched, and tix prices, as strings.

        Type: Object (Required)

        Note: Prices should be considered dangerously stale after 24 hours.
        """
        return self.scryfall_data["prices"]

    @property
    def printed_name(self):
        """
        The localized name printed on this card, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["printed_name"]

    @property
    def printed_text(self):
        """
        The localized text printed on this card, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["printed_text"]

    @property
    def printed_type_line(self):
        """
        The localized type line printed on this card, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["printed_type_line"]

    @property
    def promo(self):
        """
        True if this card is a promotional print.

        Type: Boolean (Required)
        """
        return self.scryfall_data["promo"]

    @property
    def promo_types(self):
        """
        An array of strings describing what categories of promo cards this card falls into.

        Type: Array of Strings (Nullable)
        """
        return self.scryfall_data["promo_types"]

    @property
    def purchase_uris(self):
        """
        An object providing URIs to this card's listing on major marketplaces. Omitted if the card is unpurchaseable.

        Type: Object (Nullable)
        """
        return self.scryfall_data["purchase_uris"]

    @property
    def rarity(self):
        """
        This card's rarity. One of common, uncommon, rare, special, mythic, or bonus.

        Type: String (Required)
        """
        return self.scryfall_data["rarity"]

    @property
    def related_uris(self):
        """
        An object providing URIs to this card's listing on other Magic resources.

        Type: Object (Required)
        """
        return self.scryfall_data["related_uris"]

    @property
    def released_at(self):
        """
        The date this card was first released.

        Type: Date (Required)
        """
        return self.scryfall_data["released_at"]

    @property
    def reprint(self):
        """
        True if this card is a reprint.

        Type: Boolean (Required)
        """
        return self.scryfall_data["reprint"]

    @property
    def scryfall_set_uri(self):
        """
        A link to this card's set on Scryfall's website.

        Type: URI (Required)
        """
        return self.scryfall_data["scryfall_set_uri"]

    @property
    def set_name(self):
        """
        This card's full set name.

        Type: String (Required)
        """
        return self.scryfall_data["set_name"]

    @property
    def set_search_uri(self):
        """
        A link to where you can begin paginating this card's set on the Scryfall API.

        Type: URI (Required)
        """
        return self.scryfall_data["set_search_uri"]

    @property
    def set_type(self):
        """
        The type of set this printing is in.

        Type: String (Required)
        """
        return self.scryfall_data["set_type"]

    @property
    def set_uri(self):
        """
        A link to this card's set object on Scryfall's API.

        Type: URI (Required)
        """
        return self.scryfall_data["set_uri"]

    @property
    def set(self):
        """
        This card's set code.

        Type: String (Required)
        """
        return self.scryfall_data["set"]

    @property
    def set_id(self):
        """
        This card's Set object UUID.

        Type: UUID (Required)
        """
        return self.scryfall_data["set_id"]

    @property
    def story_spotlight(self):
        """
        True if this card is a Story Spotlight.

        Type: Boolean (Required)
        """
        return self.scryfall_data["story_spotlight"]

    @property
    def textless(self):
        """
        True if the card is printed without text.

        Type: Boolean (Required)
        """
        return self.scryfall_data["textless"]

    @property
    def variation(self):
        """
        Whether this card is a variation of another printing.

        Type: Boolean (Required)
        """
        return self.scryfall_data["variation"]

    @property
    def variation_of(self):
        """
        The printing ID of the printing this card is a variation of.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["variation_of"]

    @property
    def security_stamp(self):
        """
        The security stamp on this card, if any. One of oval, triangle, acorn, circle, arena, or heart.

        Type: String (Nullable)
        """
        return self.scryfall_data["security_stamp"]

    @property
    def watermark(self):
        """
        This card's watermark, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["watermark"]

    @property
    def previewed_at(self):
        """
        The date this card was previewed.

        Type: Date (Nullable)
        """
        return self.scryfall_data["preview"]["previewed_at"]

    @property
    def preview_source_uri(self):
        """
        A link to the preview for this card.

        Type: URI (Nullable)
        """
        return self.scryfall_data["preview"]["source_uri"]

    @property
    def preview_source(self):
        """
        The name of the source that previewed this card.

        Type: String (Nullable)
        """
        return self.scryfall_data["preview"]["source"]


class CardFaceMixin:
    scryfall_data: dict[str, Any]

    @property
    def artist(self):
        """
        The name of the illustrator of this card face. Newly spoiled cards may not have this field yet.

        Type: String (Nullable)
        """
        return self.scryfall_data["artist"]

    @property
    def artist_id(self):
        """
        The ID of the illustrator of this card face. Newly spoiled cards may not have this field yet.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["artist_id"]

    @property
    def cmc(self):
        """
        The mana value of this particular face, if the card is reversible.

        Type: Decimal (Nullable)
        """
        return self.scryfall_data["cmc"]

    @property
    def color_indicator(self):
        """
        The colors in this face's color indicator, if any.

        Type: Colors (Nullable)
        """
        return self.scryfall_data["color_indicator"]

    @property
    def colors(self):
        """
        This face's colors, if the game defines colors for the individual face of this card.

        Type: Colors (Nullable)
        """
        return self.scryfall_data["colors"]

    @property
    def defense(self):
        """
        This face's defense, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["defense"]

    @property
    def flavor_text(self):
        """
        The flavor text printed on this face, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["flavor_text"]

    @property
    def illustration_id(self):
        """
        A unique identifier for the card face artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["illustration_id"]

    @property
    def image_uris(self):
        """
        An object providing URIs to imagery for this face, if this is a double-sided card.

        Type: Object (Nullable)
        """
        return self.scryfall_data["image_uris"]

    @property
    def layout(self):
        """
        The layout of this card face, if the card is reversible.

        Type: String (Nullable)
        """
        return self.scryfall_data["layout"]

    @property
    def loyalty(self):
        """
        This face's loyalty, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["loyalty"]

    @property
    def mana_cost(self):
        """
        The mana cost for this face. This value will be any empty string "" if the cost is absent.

        Type: String (Nullable)
        """
        return self.scryfall_data["mana_cost"]

    @property
    def name(self):
        """
        The name of this particular face.

        Type: String (Required)
        """
        return self.scryfall_data["name"]

    @property
    def object(self):
        """
        A content type for this object, always card_face.

        Type: String (Required)
        """
        return self.scryfall_data["object"]

    @property
    def oracle_id(self):
        """
        The Oracle ID of this particular face, if the card is reversible.

        Type: UUID (Nullable)
        """
        return self.scryfall_data["oracle_id"]

    @property
    def oracle_text(self):
        """
        The Oracle text for this face, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["oracle_text"]

    @property
    def power(self):
        """
        This face's power, if any. Note that some cards have powers that are not numeric, such as *.

        Type: String (Nullable)
        """
        return self.scryfall_data["power"]

    @property
    def printed_name(self):
        """
        The localized name printed on this face, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["printed_name"]

    @property
    def printed_text(self):
        """
        The localized text printed on this face, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["printed_text"]

    @property
    def printed_type_line(self):
        """
        The localized type line printed on this face, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["printed_type_line"]

    @property
    def toughness(self):
        """
        This face's toughness, if any. Note that some cards have toughnesses that are not numeric, such as *.

        Type: String (Nullable)
        """
        return self.scryfall_data["toughness"]

    @property
    def type_line(self):
        """
        The type line of this particular face, if the card is reversible.

        Type: String (Nullable)
        """
        return self.scryfall_data["type_line"]

    @property
    def watermark(self):
        """
        The watermark on this particular card face, if any.

        Type: String (Nullable)
        """
        return self.scryfall_data["watermark"]


class RelatedCardsObjectMixin:
    scryfall_data: dict[str, Any]

    @property
    def id(self):
        """
        An unique ID for this card in Scryfall's database.

        Type: UUID (Required)
        """
        return self.scryfall_data["id"]

    @property
    def object(self):
        """
        A content type for this object, always related_card.

        Type: String (Required)
        """
        return self.scryfall_data["object"]

    @property
    def component(self):
        """
        A field explaining what role this card plays in this relationship, one of token, meld_part, meld_result, or combo_piece.

        Type: String (Required)
        """
        return self.scryfall_data["component"]

    @property
    def name(self):
        """
        The name of this particular related card.

        Type: String (Required)
        """
        return self.scryfall_data["name"]

    @property
    def type_line(self):
        """
        The type line of this card.

        Type: String (Required)
        """
        return self.scryfall_data["type_line"]

    @property
    def uri(self):
        """
        A URI where you can retrieve a full object describing this card on Scryfall's API.

        Type: URI (Required)
        """
        return self.scryfall_data["uri"]


class CardsObjectMixin(CoreFieldsMixin, GameplayFieldsMixin, PrintFieldsMixin):
    pass
