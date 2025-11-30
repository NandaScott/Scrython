def to_object_array(Object, key, scryfall_data):
    """Remaps an array of dicts to an array of Objects.

    Args:
        Object: The class to instantiate for each item in the array
        key: The dictionary key to extract from scryfall_data
        scryfall_data: The source dictionary containing the array data

    Returns:
        List of Object instances, or None if key is not present (for nullable fields)
    """
    if key not in scryfall_data:
        return None
    return list(map(lambda data: Object(data), scryfall_data[key]))
