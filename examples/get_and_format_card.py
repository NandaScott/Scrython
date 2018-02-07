import scrython

getCard = input("What card would you like me to search? ")

card = scrython.cards.Named(fuzzy=getCard)

if card.object() == 'error':
    print(card.scryfallJson['details'])

if card.type_line() == 'Creature':
    PT = "({}/{})".format(card.power(), card.toughness())
else:
    PT = ""

if card.cmc() == 0:
    mana_cost = ""
else:
    mana_cost = card.mana_cost()

string = """
{cardname} {mana_cost}
{type_line} {set_code} {rarity}
{oracle_text}{power_toughness}
""".format(
        cardname=card.name(),
        mana_cost=mana_cost,
        type_line=card.type_line(),
        set_code=card.set_code().upper(),
        rarity=card.rarity(),
        oracle_text=card.oracle_text(),
        power_toughness=PT
        )

print(string)
