def to_object_array(Object, key, scryfall_data):
    """Remaps an array of dicts to an array of Objects"""
    return list(map(lambda data: Object(data), scryfall_data[key]))
