from .rulings_object import RulingsObject

class Id(RulingsObject):
    """
    cards/:id/rulings

    Gets the ruling of a card by the Scryfall Id.

    Positional arguments:
        id : str ...................... The id of the card you want rulings for.

    Optional arguments:
        All arguments inherited from RulingsObject

    Attributes:
        All attributes inherited from RulingsObject

    Example usage:
        >>> rule = scrython.rulings.Id(id='5976c352-ac49-4e0d-a4c0-ec9b6b78db9c')
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/{}/rulings?'.format(str(kwargs.get('id')))
        super(Id, self).__init__(self.url)
