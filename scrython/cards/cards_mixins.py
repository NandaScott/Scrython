from functools import cache
from ..utils import to_object_array

class CoreFieldsMixin:
  @property
  def arena_id(self):
    """
    This card's Arena ID, if any. A large percentage of cards are not available on Arena.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['arena_id']

  @property
  def id(self):
    """
    A unique identifier within Scryfall's database.

    Type: UUID (Required)
    """
    return self.scryfall_data['id']

  @property
  def lang(self):
    """
    A language code for this printing.

    Type: String (Required)
    """
    return self.scryfall_data['lang']

  @property
  def mtgo_id(self):
    """
    Magic Online catalog identifier when available.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['mtgo_id']

  @property
  def mtgo_foil_id(self):
    """
    Foil variant identifier for Magic Online.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['mtgo_foil_id']

  @property
  def multiverse_ids(self):
    """
    This card's multiverse IDs on Gatherer, if any, as an array.

    Type: Array of Integers (Nullable)
    """
    return self.scryfall_data['multiverse_ids']

  @property
  def tcgplayer_id(self):
    """
    TCGplayer product identifier.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['tcgplayer_id']

  @property
  def tcgplayer_etched_id(self):
    """
    TCGplayer etched version identifier.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['tcgplayer_etched_id']

  @property
  def cardmarket_id(self):
    """
    Cardmarket API identifier.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['cardmarket_id']

  @property
  def object(self):
    """
    Content type, always "card".

    Type: String (Required)
    """
    return 'card'

  @property
  def layout(self):
    """
    A code for this card's layout.

    Type: String (Required)
    """
    return self.scryfall_data['layout']

  @property
  def oracle_id(self):
    """
    Consistent ID across reprints of same card.

    Type: UUID (Nullable)
    """
    return self.scryfall_data['oracle_id']

  @property
  def prints_search_uri(self):
    """
    Link to all reprints via API.

    Type: URI (Required)
    """
    return self.scryfall_data['prints_search_uri']

  @property
  def rulings_uri(self):
    """
    Link to card's rulings list.

    Type: URI (Required)
    """
    return self.scryfall_data['rulings_uri']

  @property
  def scryfall_uri(self):
    """
    Permanent webpage link.

    Type: URI (Required)
    """
    return self.scryfall_data['scryfall_uri']

  @property
  def uri(self):
    """
    API object link.

    Type: URI (Required)
    """
    return self.scryfall_data['uri']

class GameplayFieldsMixin:
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

    return to_object_array(RelatedCardObject, 'all_parts')

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

    return to_object_array(CardFaceObject, 'card_faces')

  @property
  def cmc(self):
    """
    The card's mana value.

    Type: Decimal (Required)
    """
    return self.scryfall_data['cmc']

  @property
  def color_identity(self):
    """
    This card's color identity.

    Type: Colors (Required)
    """
    return self.scryfall_data['color_identity']

  @property
  def color_indicator(self):
    """
    Colors indicated on the card face.

    Type: Colors (Nullable)
    """
    return self.scryfall_data['color_indicator']

  @property
  def colors(self):
    """
    Card's colors per game rules.

    Type: Colors (Nullable)
    """
    return self.scryfall_data['colors']

  @property
  def defense(self):
    """
    Defense value if applicable.

    Type: String (Nullable)
    """
    return self.scryfall_data['defense']

  @property
  def edhrec_rank(self):
    """
    EDHREC popularity ranking.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['edhrec_rank']

  @property
  def game_changer(self):
    """
    True if this card is on the Commander Game Changer list.

    Type: Boolean (Nullable)
    """
    return self.scryfall_data['game_changer']

  @property
  def hand_modifier(self):
    """
    Vanguard card hand delta value.

    Type: String (Nullable)
    """
    return self.scryfall_data['hand_modifier']

  @property
  def keywords(self):
    """
    Array of keywords that this card uses, such as Flying.

    Type: Array (Required)
    """
    return self.scryfall_data['keywords']

  @property
  def legalities(self):
    """
    Format legality across play modes.

    Type: Object (Required)
    """
    return self.scryfall_data['legalities']

  @property
  def life_modifier(self):
    """
    Vanguard card life delta value.

    Type: String (Nullable)
    """
    return self.scryfall_data['life_modifier']

  @property
  def loyalty(self):
    """
    Planeswalker loyalty value.

    Type: String (Nullable)
    """
    return self.scryfall_data['loyalty']

  @property
  def mana_cost(self):
    """
    The mana cost for this card. This value will be any empty string if the cost is absent.

    Type: String (Nullable)

    Example: "{3}{U}{U}"
    """
    return self.scryfall_data['mana_cost']

  @property
  def name(self):
    """
    Card name; multiface cards show both names separated.

    Type: String (Required)
    """
    return self.scryfall_data['name']

  @property
  def oracle_text(self):
    """
    Official card ability text.

    Type: String (Nullable)
    """
    return self.scryfall_data['oracle_text']

  @property
  def penny_rank(self):
    """
    Penny Dreadful format ranking.

    Type: Integer (Nullable)
    """
    return self.scryfall_data['penny_rank']

  @property
  def power(self):
    """
    Creature power value.

    Type: String (Nullable)
    """
    return self.scryfall_data['power']

  @property
  def produced_mana(self):
    """
    Mana colors the card can generate.

    Type: Colors (Nullable)
    """
    return self.scryfall_data['produced_mana']

  @property
  def reserved(self):
    """
    True if this card is on the Reserved List.

    Type: Boolean (Required)
    """
    return self.scryfall_data['reserved']

  @property
  def toughness(self):
    """
    Creature toughness value.

    Type: String (Nullable)
    """
    return self.scryfall_data['toughness']

  @property
  def type_line(self):
    """
    The type line of this card.

    Type: String (Required)

    Example: "Legendary Creature — Human Wizard"
    """
    return self.scryfall_data['type_line']
  
class PrintFieldsMixin:
  @property
  def artist(self):
    return self.scryfall_data['artist']
  
  @property
  def artist_ids(self):
    return self.scryfall_data['artist_ids']
  
  @property
  def attraction_lights(self):
    return self.scryfall_data['attraction_lights']
  
  @property
  def booster(self):
    return self.scryfall_data['booster']
  
  @property
  def border_color(self):
    return self.scryfall_data['border_color']
  
  @property
  def card_back_id(self):
    return self.scryfall_data['card_back_id']
  
  @property
  def collector_number(self):
    return self.scryfall_data['collector_number']
  
  @property
  def content_warning(self):
    return self.scryfall_data['content_warning']
  
  @property
  def digital(self):
    return self.scryfall_data['digital']
  
  @property
  def finishes(self):
    return self.scryfall_data['finishes']
  
  @property
  def flavor_name(self):
    return self.scryfall_data['flavor_name']
  
  @property
  def flavor_text(self):
    return self.scryfall_data['flavor_text']
  
  @property
  def frame_effects(self):
    return self.scryfall_data['frame_effects']
  
  @property
  def frame(self):
    return self.scryfall_data['frame']
  
  @property
  def full_art(self):
    return self.scryfall_data['full_art']
  
  @property
  def games(self):
    return self.scryfall_data['games']
  
  @property
  def highres_image(self):
    return self.scryfall_data['highres_image']
  
  @property
  def illustration_id(self):
    return self.scryfall_data['illustration_id']
  
  @property
  def image_status(self):
    return self.scryfall_data['image_status']
  
  @property
  def image_uris(self):
    return self.scryfall_data['image_uris']
  
  @property
  def oversized(self):
    return self.scryfall_data['oversized']
  
  @property
  def prices(self):
    return self.scryfall_data['prices']
  
  @property
  def printed_name(self):
    return self.scryfall_data['printed_name']
  
  @property
  def printed_text(self):
    return self.scryfall_data['printed_text']
  
  @property
  def printed_type_line(self):
    return self.scryfall_data['printed_type_line']
  
  @property
  def promo(self):
    return self.scryfall_data['promo']
  
  @property
  def promo_types(self):
    return self.scryfall_data['promo_types']
  
  @property
  def purchase_uris(self):
    return self.scryfall_data['purchase_uris']
  
  @property
  def rarity(self):
    return self.scryfall_data['rarity']
  
  @property
  def related_uris(self):
    return self.scryfall_data['related_uris']
  
  @property
  def released_at(self):
    return self.scryfall_data['released_at']
  
  @property
  def reprint(self):
    return self.scryfall_data['reprint']
  
  @property
  def scryfall_set_uri(self):
    return self.scryfall_data['scryfall_set_uri']
  
  @property
  def set_name(self):
    return self.scryfall_data['set_name']
  
  @property
  def set_search_uri(self):
    return self.scryfall_data['set_search_uri']
  
  @property
  def set_type(self):
    return self.scryfall_data['set_type']
  
  @property
  def set_uri(self):
    return self.scryfall_data['set_uri']
  
  @property
  def set(self):
    return self.scryfall_data['set']
  
  @property
  def set_id(self):
    return self.scryfall_data['set_id']
  
  @property
  def story_spotlight(self):
    return self.scryfall_data['story_spotlight']
  
  @property
  def textless(self):
    return self.scryfall_data['textless']
  
  @property
  def variation(self):
    return self.scryfall_data['variation']
  
  @property
  def variation_of(self):
    return self.scryfall_data['variation_of']
  
  @property
  def security_stamp(self):
    return self.scryfall_data['security_stamp']
  
  @property
  def watermark(self):
    return self.scryfall_data['watermark']
  
  @property
  def previewed_at(self):
    return self.scryfall_data['preview']['previewed_at']
  
  @property
  def preview_source_uri(self):
    return self.scryfall_data['preview']['source_uri']
  
  @property
  def preview_source(self):
    return self.scryfall_data['preview']['source']

class CardFaceMixin:
  @property
  def artist(self):
    return self.scryfall_data['artist']
  
  @property
  def artist_id(self):
    return self.scryfall_data['artist_id']
  
  @property
  def cmc(self):
    return self.scryfall_data['cmc']
  
  @property
  def color_indicator(self):
    return self.scryfall_data['color_indicator']
  
  @property
  def colors(self):
    return self.scryfall_data['colors']
  
  @property
  def defense(self):
    return self.scryfall_data['defense']
  
  @property
  def flavor_text(self):
    return self.scryfall_data['flavor_text']
  
  @property
  def illustration_id(self):
    return self.scryfall_data['illustration_id']
  
  @property
  def image_uris(self):
    return self.scryfall_data['image_uris']
  
  @property
  def layout(self):
    return self.scryfall_data['layout']
  
  @property
  def loyalty(self):
    return self.scryfall_data['loyalty']
  
  @property
  def mana_cost(self):
    return self.scryfall_data['mana_cost']
  
  @property
  def name(self):
    return self.scryfall_data['name']
  
  @property
  def object(self):
    return self.scryfall_data['object']
  
  @property
  def oracle_id(self):
    return self.scryfall_data['oracle_id']
  
  @property
  def oracle_text(self):
    return self.scryfall_data['oracle_text']
  
  @property
  def power(self):
    return self.scryfall_data['power']
  
  @property
  def printed_name(self):
    return self.scryfall_data['printed_name']
  
  @property
  def printed_text(self):
    return self.scryfall_data['printed_text']
  
  @property
  def printed_type_line(self):
    return self.scryfall_data['printed_type_line']
  
  @property
  def toughness(self):
    return self.scryfall_data['toughness']
  
  @property
  def type_line(self):
    return self.scryfall_data['type_line']
  
  @property
  def watermark(self):
    return self.scryfall_data['watermark']

class RelatedCardsObjectMixin:
  @property
  def id(self):
    return self.scryfall_data['id']
  
  @property
  def object(self):
    return self.scryfall_data['object']
  
  @property
  def component(self):
    return self.scryfall_data['component']
  
  @property
  def name(self):
    return self.scryfall_data['name']
  
  @property
  def type_line(self):
    return self.scryfall_data['type_line']
  
  @property
  def uri(self):
    return self.scryfall_data['uri']

class CardsObjectMixin(CoreFieldsMixin, GameplayFieldsMixin, PrintFieldsMixin):
  pass