import scrython
import time
import json
import os.path
import re

# This file will parse a scryfall exported deck list and create a list of tokens
# needed for that deck. To run this, make sure that your deck file is in the same folder
# as this. You can then copy/paste the output file back into Scryfall to list all the
# tokens.

def get_cards():
  with open('scryfall-deck.txt', 'r') as f:
    cards_from_file = f.read().splitlines()

    list_of_cards = []
  for name in cards_from_file:
    true_name = re.findall(r'[^\d\s//].*', name)
    if true_name == ['Commander'] or len(true_name) == 0:
      continue
    else:
      true_name = true_name[0]

    list_of_cards.append(true_name)

  data = { 'data': [] }

  for i, card in enumerate(list_of_cards, start=1):
    print('Fetching card: {} | {} of {}'.format(card, i, len(list_of_cards)))
    card = scrython.cards.Named(fuzzy=card)
    data['data'].append(card.scryfallJson)
    time.sleep(0.5)

  with open('scryfall_data.json', 'w+') as f:
    f.write(json.dumps(data, sort_keys=True, indent=4))

def create_list():
  with open('scryfall_data.json', 'r') as f:
    data = json.load(f)

  # Parses through each card in the full json we collected from get_cards
  # If the card has the all_parts key, check if it's a token.
  # If it is, fetch that token and record it's name and set code
  with open('tokens_needed.txt', 'w') as f:
    for card in data['data']:
      if 'all_parts' in card:
        for part in card['all_parts']:
          if part['component'] == 'token':
            token = scrython.cards.Id(id=part['id'])
            time.sleep(0.1)
            f.write('{} | {}\n'.format(token.name(), token.set_code()))

if not os.path.isfile('./scryfall_data.json'):
  get_cards()

create_list()