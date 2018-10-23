from .cards_object import CardsObject

class ArenaId(CardsObject):
    """
    cards/id
    Get a card by the Arena id.

    Args:
        id (string):
            The Scryfall Id of the card.
        format (string, optional):
            Defaults to 'json'.
            Returns data in the specified method.
        face (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify if you want the front or back face.
        version (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify if you want the small, normal,
            large, etc version of the image.
        pretty (string, optional):
            Defaults to empty string.
            Returns a prettier version of the json object.
            Note that this may break functionality with Scrython.

    Attributes:
        All attributes are inherited from CardsObject.

    Example usage:
        >>> card = scrython.cards.ArenaId(id="66975")
        >>> card.name()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/arena/{}?'.format(str(kwargs.get('id')))
        super(ArenaId, self).__init__(self.url)
