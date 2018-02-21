from .rulings_object import RulingsObject

class Mtgo(RulingsObject):
    """
    cards/mtgo/:id/rulings

    Gets the ruling of a card by the Mtgo Id.

    Positional arguments:
        id : str ................. The mtgo id of the card you want rulings for.

    Optional arguments:
        All arguments inherited from RulingsObject

    Attributes:
        All attributes inherited from RulingsObject

    Example usage:
        >>> rule = scrython.rulings.Mtgo(id='9611')
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/mtgo/{}/rulings?'.format(str(kwargs.get('id')))
        super(Mtgo, self).__init__(self.url)
