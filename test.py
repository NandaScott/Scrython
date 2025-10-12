import scrython

search = scrython.Cards(search='Lightning Bolt')
print(repr(search), search.object)

fuzzy = scrython.Cards(fuzzy='Lightning Bolt')
print(repr(fuzzy), fuzzy.object)

exact = scrython.Cards(exact='Lightning Bolt')
print(repr(exact), exact.object)

autocomplete = scrython.Cards(autocomplete='Thal')
print(repr(autocomplete), autocomplete.object)

random = scrython.Cards(random=True)
print(repr(random), random.object)

collection = scrython.Cards(collection=[
    {
      "id": "683a5707-cddb-494d-9b41-51b4584ded69"
    },
    {
      "name": "Ancient Tomb"
    },
    {
      "set": "mrd",
      "collector_number": "150"
    }
  ])
print(repr(collection), collection.object)

code = scrython.Cards(code='znr', number=100)
print(repr(code), code.object)

multiverse = scrython.Cards(multiverse=491743)
print(repr(multiverse), multiverse.object)

mtgo = scrython.Cards(mtgo=83179)
print(repr(mtgo), mtgo.object)

arena = scrython.Cards(arena=73304)
print(repr(arena), arena.object)

tcgplayer = scrython.Cards(tcgplayer=221954)
print(repr(tcgplayer), tcgplayer.object)

cardmarket = scrython.Cards(cardmarket=495484)
print(repr(cardmarket), cardmarket.object)

by_id = scrython.Cards(id='24c40082-516e-4381-a4cc-e61c5a9a6cac')
print(repr(by_id), by_id.object)