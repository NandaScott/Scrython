from .cards_object import CardsObject

class ArenaId(CardsObject):
    """
    cards/id
    Get a card by the Arena id.

    Positional arguments:
        id : str ....................... The Scryfall Id of the card.

    Optional arguments:
        Inherits all arguments from CardsObject.

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
