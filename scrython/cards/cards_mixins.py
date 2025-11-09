from functools import cache
from ..utils import to_object_array

class CoreFieldsMixin:
  @property
  def arena_id(self):
    return self.scryfall_data['arena_id']
  
  @property
  def id(self):
    return self.scryfall_data['id']
  
  @property
  def lang(self):
    return self.scryfall_data['lang']
  
  @property
  def mtgo_id(self):
    return self.scryfall_data['mtgo_id']
  
  @property
  def mtgo_foil_id(self):
    return self.scryfall_data['mtgo_foil_id']
  
  @property
  def multiverse_ids(self):
    return self.scryfall_data['multiverse_ids']
  
  @property
  def tcgplayer_id(self):
    return self.scryfall_data['tcgplayer_id']
  
  @property
  def tcgplayer_etched_id(self):
    return self.scryfall_data['tcgplayer_etched_id']
  
  @property
  def cardmarket_id(self):
    return self.scryfall_data['cardmarket_id']
  
  @property
  def object(self):
    return 'card'
  
  @property
  def layout(self):
    return self.scryfall_data['layout']
  
  @property
  def oracle_id(self):
    return self.scryfall_data['oracle_id']
  
  @property
  def prints_search_uri(self):
    return self.scryfall_data['prints_search_uri']
  
  @property
  def rulings_uri(self):
    return self.scryfall_data['rulings_uri']
  
  @property
  def scryfall_uri(self):
    return self.scryfall_data['scryfall_uri']
  
  @property
  def uri(self):
    return self.scryfall_data['uri']

class GameplayFieldsMixin:
  @property
  @cache
  def all_parts(self):
    class RelatedCardObject(RelatedCardsObjectMixin):
      def __init__(self, data):
        self.scryfall_data = data

    return to_object_array(RelatedCardObject, 'all_parts')
  
  @property
  @cache
  def card_faces(self):
    class CardFaceObject(CardFaceMixin):
      def __init__(self, data):
        self.scryfall_data = data

    return to_object_array(CardFaceObject, 'card_faces')
  
  @property
  def cmc(self):
    return self.scryfall_data['cmc']
  
  @property
  def color_identity(self):
    return self.scryfall_data['color_identity']
  
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
  def edhrec_rank(self):
    return self.scryfall_data['edhrec_rank']
  
  @property
  def game_changer(self):
    return self.scryfall_data['game_changer']
  
  @property
  def hand_modifier(self):
    return self.scryfall_data['hand_modifier']
  
  @property
  def keywords(self):
    return self.scryfall_data['keywords']
  
  @property
  def legalities(self):
    return self.scryfall_data['legalities']
  
  @property
  def life_modifier(self):
    return self.scryfall_data['life_modifier']
  
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
  def oracle_text(self):
    return self.scryfall_data['oracle_text']
  
  @property
  def penny_rank(self):
    return self.scryfall_data['penny_rank']
  
  @property
  def power(self):
    return self.scryfall_data['power']
  
  @property
  def produced_mana(self):
    return self.scryfall_data['produced_mana']
  
  @property
  def reserved(self):
    return self.scryfall_data['reserved']
  
  @property
  def toughness(self):
    return self.scryfall_data['toughness']
  
  @property
  def type_line(self):
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