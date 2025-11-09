class SetsObjectMixin:
    @property
    def object(self):
      return 'set'

    @property
    def id(self):
      return self.scryfall_data['id']

    @property
    def code(self):
      return self.scryfall_data['code']

    @property
    def mtgo_code(self):
      return self.scryfall_data['mtgo_code']

    @property
    def arena_code(self):
      return self.scryfall_data['arena_code']

    @property
    def tcgplayer_id(self):
      return self.scryfall_data['tcgplayer_id']

    @property
    def name(self):
      return self.scryfall_data['name']

    @property
    def set_type(self):
      return self.scryfall_data['set_type']

    @property
    def released_at(self):
      return self.scryfall_data['released_at']

    @property
    def block_code(self):
      return self.scryfall_data['block_code']

    @property
    def block(self):
      return self.scryfall_data['block']

    @property
    def parent_set_code(self):
      return self.scryfall_data['parent_set_code']

    @property
    def card_count(self):
      return self.scryfall_data['card_count']

    @property
    def printed_size(self):
      return self.scryfall_data['printed_size']

    @property
    def digital(self):
      return self.scryfall_data['digital']

    @property
    def foil_only(self):
      return self.scryfall_data['foil_only']

    @property
    def nonfoil_only(self):
      return self.scryfall_data['nonfoil_only']

    @property
    def scryfall_uri(self):
      return self.scryfall_data['scryfall_uri']

    @property
    def uri(self):
      return self.scryfall_data['uri']

    @property
    def icon_svg_uri(self):
      return self.scryfall_data['icon_svg_uri']

    @property
    def search_uri(self):
      return self.scryfall_data['search_uri']
