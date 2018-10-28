from .rulings_object import RulingsObject

class Multiverse(RulingsObject):
    """
    cards/multiverse/:id/rulings

    Gets the ruling of a card by the Multiverse Id.

    Args:
        id (string): The multiverse id of the card you want rulings for.
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
        >>> rule = scrython.rulings.Id(id="4301")
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/multiverse/{}/rulings?'.format(str(kwargs.get('id')))
        super(Multiverse, self).__init__(self.url)
