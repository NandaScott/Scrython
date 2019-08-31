import scrython

# oops, we asked for an exact match to a card, but failed to put the name in quotes
# that's going to throw a Scryfall error
try:
    search = scrython.cards.Search(q="!Black Lotus")
except scrython.ScryfallError as e:
    print(str(e.status) + ' ' + e.code + ': ' + e.details)
