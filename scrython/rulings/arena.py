from .rulings_object import RulingsObject

class Arena(RulingsObject):
    """
    cards/mtgo/:id/rulings

    Gets the ruling of a card by the Arena Id.

    Args:
        id (string): The arena id of the card you want rulings for.
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
        >>> rule = scrython.rulings.Arena(id="66975")
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/arena/{}/rulings?'.format(str(kwargs.get('id')))
        super(Arena, self).__init__(self.url)
