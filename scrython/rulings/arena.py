from .rulings_object import RulingsObject

class Arena(RulingsObject):
    """
    cards/mtgo/:id/rulings

    Gets the ruling of a card by the Arena Id.

    Positional arguments:
        id : str ................. The arena id of the card you want rulings for.

    Optional arguments:
        All arguments inherited from RulingsObject

    Attributes:
        All attributes inherited from RulingsObject

    Example usage:
        >>> rule = scrython.rulings.Arena(id='66975')
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/arena/{}/rulings?'.format(str(kwargs.get('id')))
        super(Arena, self).__init__(self.url)
