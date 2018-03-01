import scrython

query = input("What editions of a card are you looking for? ")

data = scrython.cards.Search(q="++{}".format(query))

for card in data.data():
    print(card['set'].upper(), ":", card['set_name'])
