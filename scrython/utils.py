def to_object_array(Object, key):
  """Remaps an array of dicts to an array of Objects"""
  return list(map(lambda data: Object(data), self.scryfall_data[key]))