from .rulings_object import RulingsObject

class Mtgo(RulingsObject):
    """
    cards/mtgo/:id/rulings

    Gets the ruling of a card by the Mtgo Id.

    Args:
        id (string): The mtgo id of the card you want rulings for.
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
        >>> rule = scrython.rulings.Mtgo(id="9611")
        >>> rule.data_length()
    """
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/mtgo/{}/rulings?'.format(str(kwargs.get('id')))
        super(Mtgo, self).__init__(self.url)
