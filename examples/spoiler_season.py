import scrython, time

def keyCheck(key, _dict):
    try:
        _dict[key]
        return True
    except KeyError:
        return False

def nameBar(name, manaCost):
    return "{} {}".format(name, manaCost)

def typeBar(typeLine, rarity):
    return "{} | {}".format(typeLine, rarity[:1].upper())

def powerAndToughness(power, toughness):
    return "{}/{}".format(power, toughness)

query = input("Enter a set: ")

currentSetSize = 0
lastList = []
currentList = []

while query is not None:

    #Grab the data
    spoilers = scrython.cards.Search(q="++e:{}".format(query), order='spoiled')

     #If the total cards has increased
    if spoilers.total_cards() > currentSetSize:

        #Dump if currentList already exists
        if currentList:
            del currentList[:]

        #If there aren't enough spoilers we iterate through the whole list.
        #Otherwise we only want the first 15
        if spoilers.total_cards() > 15:
            maxIteration = 15
        else:
            maxIteration = spoilers.total_cards()

        for i in range(maxIteration):
            currentList.append(spoilers.data()[i]['id'])

        #Iterate through data
        for card in reversed(spoilers.data()):
            if card['id'] in lastList:
                continue
            print("~~~~~~~~~~\nNew card:")

            #Grab the relevant keys
            if keyCheck('card_faces', card):
                print(nameBar(card['name'], card['card_faces'][0]['mana_cost']))
                print(typeBar(card['card_faces'][0]['mana_cost'], card['card_faces'][0]['rarity']))
            else:
                print(nameBar(card['name'], card['mana_cost']))
                print(typeBar(card['type_line'], card['rarity']))

            if keyCheck('oracle_text', card):
                print(card['oracle_text'])

            if keyCheck('power', card) and keyCheck('toughness', card):
                print(powerAndToughness(card['power'], card['toughness']))

    #Update card count
    currentSetSize = spoilers.total_cards()
    #Dump all in last list
    if lastList:
        del lastList[:]
    #Add the first 15 ids in current list to last list
    for i in range(maxIteration):
        lastList.append(currentList[i])

    time.sleep(300)
