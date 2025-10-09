class SetsObjectMixin:
    @property
    def object():
      return 'set'
    
    @property
    def id():
      return self.scryfall_data['id']
    
    @property
    def code():
      return self.scryfall_data['code']
    
    @property
    def mtgo_code():
      return self.scryfall_data['mtgo_code']
    
    @property
    def arena_code():
      return self.scryfall_data['arena_code']
    
    @property
    def tcgplayer_id():
      return self.scryfall_data['tcgplayer_id']
    
    @property
    def name():
      return self.scryfall_data['name']
    
    @property
    def set_type():
      return self.scryfall_data['set_type']
    
    @property
    def released_at():
      return self.scryfall_data['released_at']
    
    @property
    def block_code():
      return self.scryfall_data['block_code']
    
    @property
    def block():
      return self.scryfall_data['block']
    
    @property
    def parent_set_code():
      return self.scryfall_data['parent_set_code']
    
    @property
    def card_count():
      return self.scryfall_data['card_count']
    
    @property
    def printed_size():
      return self.scryfall_data['printed_size']
    
    @property
    def digital():
      return self.scryfall_data['digital']
    
    @property
    def foil_only():
      return self.scryfall_data['foil_only']
    
    @property
    def nonfoil_only():
      return self.scryfall_data['nonfoil_only']
    
    @property
    def scryfall_uri():
      return self.scryfall_data['scryfall_uri']
    
    @property
    def uri():
      return self.scryfall_data['uri']
    
    @property
    def icon_svg_uri():
      return self.scryfall_data['icon_svg_uri']
    
    @property
    def search_uri():
      return self.scryfall_data['search_uri']
