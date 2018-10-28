from .cards_object import CardsObject
import urllib.parse

class Mtgo(CardsObject):
    """
    cards/mtgo
    Get a card by MTGO id.

    Args:
        id (string):
            The MTGO Id of the card.
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
        Exception: If the 'id' parameter is not provided.
        Exception: If the object returned is an error.

    Examples:
        >>> card = scrython.cards.Mtgo(id="48296")
        >>> card.set_name()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/mtgo/{}?'.format(str(kwargs.get('id')))
        super(Mtgo, self).__init__(self.url)
