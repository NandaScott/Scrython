from .cards_object import CardsObject

class Multiverse(CardsObject):
    """
    cards/multiverse
    Get a card by Multiverse id

    Args:
        id (string):
            The Multiverse Id of the card.
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
        >>> card = scrython.cards.Multiverse(id='96865')
        >>> card.name()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/multiverse/{}?'.format(str(kwargs.get('id')))
        super(Multiverse, self).__init__(self.url)
