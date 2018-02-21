from .rulings_object import RulingsObject

class Code(RulingsObject):
    """
    cards/:code/:collector_number/rulings

    Gets the ruling of a card by the set and collector number.

    Positional arguments:
        set : str ...... The 3 letter set code of the card you want rulings for.
        collector_number : ................... The collector number of the card.

    Optional arguments:
        All arguments inherited from RulingsObject

    Attributes:
        All attributes inherited from RulingsObject

    Example usage:
        >>> rule = scrython.rulings.Code(code='ddg', collector_number='42')
        >>> rule.data_length()
    """
    def __init__(self, code, collector_number):
        self.url = 'cards/{}/{}/rulings?'.format(code.lower(), str(collector_number))
        super(Code, self).__init__(self.url)
