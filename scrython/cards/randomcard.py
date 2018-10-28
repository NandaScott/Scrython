from .cards_object import CardsObject


class Random(CardsObject):
    """
    cards/random
    Get a random card.

    Args:
        format (string, optional):
            Defaults to 'json'.
            Returns data in the specified method.
        face (string, optional):
            Defaults to empty string.
            If you're using the `image` format,
            this will specify if you want the front or back face.
        version (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify
            if you want the small, normal, large, etc version of the image.
        pretty (string, optional): 
            Defaults to empty string.
            Returns a prettier version of the json object. 
            Note that this may break functionality with Scrython.

    Returns:
        N/A

    Raises:
        Exception: If the object returned is an error.

    Examples:
        >>> card = scrython.cards.Random()
        >>> card.purchase_uris()
    """
    def __init__(self):
        self.url = 'cards/random?'
        super(Random, self).__init__(self.url)
