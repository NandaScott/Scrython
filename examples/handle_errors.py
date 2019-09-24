import scrython

# oops, we asked for an exact match to a card, but failed to put the name in quotes
# that's going to throw a Scryfall error
try:
    search = scrython.cards.Search(q="!Black Lotus")
except scrython.ScryfallError as e:
    print(str(e.error_details['status']) + ' ' + e.error_details['code'] + ': ' + e.error_details['details'])
