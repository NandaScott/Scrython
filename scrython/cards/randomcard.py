from .cards_object import CardsObject


class Random(CardsObject):
    """
    cards/random
    Get a random card.

    Positional arguments:
        No arguments are required.

    Optional arguments:
        All arguments are inherited from CardsObject

    Attributes:
        All attributes are inherited from CardsObject

    Example usage:
        >>> card = scrython.cards.Random()
        >>> card.purchase_uris()
    """
    def __init__(self):
        self.url = 'cards/random?'
        super(Random, self).__init__(self.url)
