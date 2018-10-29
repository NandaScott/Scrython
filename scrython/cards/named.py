from .cards_object import CardsObject
import urllib.parse

class Named(CardsObject):
    """
    cards/named
    Gets a card by the name.

    Args:
        fuzzy (string): Uses the fuzzy parameter for the card name.
        exact (string): Uses the exact parameter for the card name.
        set (string, optional):
            Defaults to empty string.
            Returns the set of the card if specified.
            Requires the 3 letter set code.
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

    Returns:
        N/A

    Raises:
        Exception: If the 'fuzzy' or 'exact' parameter is not provided.
        Exception: If the object returned is an error.

    Examples:
        >>> card = scrython.cards.Named(exact="Black Lotus")
        >>> card.colors()
    """
    def __init__(self, **kwargs):

        self.dict = {
            'set':kwargs.get('set', '')
        }

        if 'exact' in kwargs:
            self.dict['exact'] = kwargs.get('exact')
        elif 'fuzzy' in kwargs:
            self.dict['fuzzy'] = kwargs.get('fuzzy')
        else:
            raise Exception('You must provide a `fuzzy` or `exact` parameter.')

        self.args = urllib.parse.urlencode(self.dict)
        self.url = 'cards/named?' + self.args
        super(Named, self).__init__(self.url)
