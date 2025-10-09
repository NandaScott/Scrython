class BulkDataObjectMixin:
  @property
  def object(self):
    return 'bulk_data'

  @property
  def id(self):
    return self.scryfall_data['id']
  
  @property
  def uri(self):
    return self.scryfall_data['uri']
  
  @property
  def type(self):
    return self.scryfall_data['type']
  
  @property
  def name(self):
    return self.scryfall_data['name']
  
  @property
  def description(self):
    return self.scryfall_data['description']
  
  @property
  def download_uri(self):
    return self.scryfall_data['download_uri']
  
  @property
  def updated_at(self):
    return self.scryfall_data['updated_at']
  
  @property
  def size(self):
    return self.scryfall_data['size']
  
  @property
  def content_type(self):
    return self.scryfall_data['content_type']
  
  @property
  def content_encoding(self):
    return self.scryfall_data['content_encoding']