from .cards_object import CardsObject

class Collector(CardsObject):
    """
    cards/collector
    Get a card by collector number.

    Args:
        code (string): This is the 3 letter code for the set
        collector_number (string): This is the collector number of the card
        lang (string, optional): Defaults to 'en'. A 2-3 character language code.

    Returns:
        N/A

    Raises:
        Exception: If the 'code' parameter is not provided.
        Exception: If the 'collector_number' parameter is not provided.
        Exception: If the object returned is an error.

    Examples:
        >>> card = scrython.cards.Collector(code="exo", collector_number="96")
        >>> card.id()
    """
    def __init__(self, **kwargs):
        if kwargs.get('code') is None:
            raise Exception('No code provided to search by')
        elif kwargs.get('collector_number') is None:
            raise Exception('No collector number provided to search by')

        self.url = 'cards/{}/{}/{}?'.format(
            kwargs.get('code'),
            str(kwargs.get('collector_number')),
            kwargs.get('lang', 'en')
            )
        super(Collector, self).__init__(self.url)
