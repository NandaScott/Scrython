from .rulings_object import RulingsObject

class Code(RulingsObject):
    """
    cards/:code/:collector_number/rulings

    Gets the ruling of a card by the set and collector number.

    Args:
        set (string): The 3 letter set code of the card you want rulings for.
        collector_number (string): The collector number of the card.
        format (string, optional): Returns data in the specified method. Defaults to JSON.
        face (string, optional): 
            If you're using the `image` format, this will specify if you want the front or back face.
        version (string, optional):
            If you're using the `image` format, this will specify if you want the small, normal, large, etc version of the image.
        pretty (string, optional):
            Returns a prettier version of the json object. Note that this may break functionality with Scrython.

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> rule = scrython.rulings.Code(code="ddg", collector_number="42")
        >>> rule.data_length()
    """
    def __init__(self, code, collector_number):
        self.url = 'cards/{}/{}/rulings?'.format(code.lower(), str(collector_number))
        super(Code, self).__init__(self.url)
