from .rulings_object import RulingsObject

class Multiverse(RulingsObject):
    """
    cards/multiverse/:id/rulings

    Gets the ruling of a card by the Multiverse Id.

    Positional arguments:
        id : str ........... The multiverse id of the card you want rulings for.

    Optional arguments:
        All arguments inherited from RulingsObject

    Attributes:
        All attributes inherited from RulingsObject

    Example usage:
        >>> rule = scrython.rulings.Id(id='4301')
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/multiverse/{}/rulings?'.format(str(kwargs.get('id')))
        super(Multiverse, self).__init__(self.url)
