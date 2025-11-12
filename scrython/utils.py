def to_object_array(Object, key, scryfall_data):
    """Remaps an array of dicts to an array of Objects.

    Returns None if the key is not present in scryfall_data (for nullable fields).
    """
    if key not in scryfall_data:
        return None
    return list(map(lambda data: Object(data), scryfall_data[key]))
