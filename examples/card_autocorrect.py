import scrython
import time

query = input("Name a card: ")

auto = ""

try:
    time.sleep(0.05)
    card = scrython.cards.Named(exact=query)
except Exception:
    time.sleep(0.05)
    auto = scrython.cards.Autocomplete(q=query, query=query)

if auto:
    print("Did you mean?")
    for item in auto.data():
        print(item)
else:
    print(card.name())
