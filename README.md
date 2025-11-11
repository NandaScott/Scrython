# Scrython

Scrython is a wrapper for the Scryfall API, designed for an easier use. Make sure to familiarize yourself with the docs.

[Here is a link to the Scryfall API documentation.](https://scryfall.com/docs/api)

# Dependencies
- `python` >= 3.5.3
- `asyncio` >= 3.4.3
- `aiohttp` >= 3.4.4

## Basic usage

You can install scrython by running `pip install scrython`. Note that it requires `asyncio` and `aiohttp` too.

Scrython can be imported using `import scrython` at the top of your code.
I've written to library to attempt to be familiar for those who already use it. As such, modules like `cards` are named to reflect the endpoints found in `api.scryfall.com/cards/`and so on.
For the most part I've kept all the class attributes the same as their key names, except for a few cases where I've found better functionality.

```
    >>>import scrython
    >>>card = scrython.cards.Named(fuzzy="Black Lotus")
    >>>card.name()
    'Black Lotus'
    >>>card.id()
    'bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd'
    >>>card.oracle_text()
    '{T}, Sacrifice Black Lotus: Add three mana of any one color to your mana pool.'
```

## ⚠️ Important: Rate Limiting

**Scryfall requires 50-100 milliseconds delay between requests** (~10 requests/second maximum).

Excessive requests can result in temporary or permanent IP bans. You are responsible for implementing rate limiting in your application.

### Example with Rate Limiting:

```python
import scrython
import time

# Search for cards with proper delays
cards_to_fetch = ['Lightning Bolt', 'Counterspell', 'Black Lotus']

for card_name in cards_to_fetch:
    card = scrython.Cards(fuzzy=card_name)
    print(f"{card.name} - {card.set}")

    # IMPORTANT: Add delay between requests
    time.sleep(0.1)  # 100ms delay
```

### Better: Use Bulk Data for Large Datasets

For large-scale data processing, use Scryfall's bulk data downloads instead:

```python
bulk = scrython.BulkData(type='default_cards')
download_url = bulk.download_uri

# Download and process locally
# (Bulk data files are updated every 12 hours)
```

### Caching Recommendations

- Cache responses for at least 24 hours
- Card prices become unreliable after 24 hours
- Consider downloading bulk data for offline processing

### Custom User-Agent (Recommended)

Scryfall requests that applications identify themselves with a custom User-Agent:

```python
import scrython

# Set custom User-Agent for your application
scrython.Cards.set_user_agent('MyMTGApp/1.0 (contact@example.com)')

# All subsequent requests will use your custom User-Agent
card = scrython.Cards(fuzzy='Black Lotus')
```

## Complete Usage Examples

### Basic Card Lookup

```python
import scrython

# Fuzzy name search (handles typos)
card = scrython.Cards(fuzzy='Light Bolt')
print(card.name)  # "Lightning Bolt"
print(card.mana_cost)  # "{R}"
print(card.type_line)  # "Instant"
print(card.oracle_text)

# Exact name match
card = scrython.Cards(exact='Black Lotus')
print(card.prices)
# {'usd': '25000.00', 'usd_foil': None, ...}
```

### Advanced Search

```python
# Search with Scryfall syntax
results = scrython.Cards(search='type:creature cmc:1 color:red')

print(f"Found {results.total_cards} cards")

for card in results.data:
    print(f"{card.name} - {card.set_name}")

# Handle pagination
if results.has_more:
    print("More results available - implement pagination as needed")
```

### Getting Specific Cards

```python
# By set code and collector number
card = scrython.Cards(code='znr', number='123')

# By various IDs
card = scrython.Cards(multiverse='456789')
card = scrython.Cards(mtgo='67890')
card = scrython.Cards(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')

# Get random card
card = scrython.Cards(random=True)
card = scrython.Cards(random=True, q='rarity:mythic')  # Random mythic
```

### Working with Sets

```python
# Get all sets
all_sets = scrython.Sets()

for set_obj in all_sets.data:
    print(f"{set_obj.name} ({set_obj.code}) - {set_obj.card_count} cards")

# Get specific set
set_obj = scrython.Sets(code='znr')
print(f"{set_obj.name} released on {set_obj.released_at}")
print(f"Set type: {set_obj.set_type}")
```

### Bulk Data Download

```python
import scrython
import requests

# Get all bulk data options
all_bulk = scrython.BulkData()

for bulk in all_bulk.data:
    print(f"{bulk.name}: {bulk.description}")
    print(f"Size: {bulk.size / 1_000_000:.1f} MB")

# Download specific bulk data
oracle_cards = scrython.BulkData(type='oracle_cards')
print(f"Download from: {oracle_cards.download_uri}")

# Actually download (example)
response = requests.get(oracle_cards.download_uri)
cards = response.json()
print(f"Downloaded {len(cards)} cards")

# Now process locally without rate limits!
for card in cards:
    if 'Lightning' in card['name']:
        print(card['name'])
```

### Error Handling

```python
from scrython.base import ScryfallError

try:
    card = scrython.Cards(exact='Nonexistent Card Name')
except ScryfallError as e:
    print(f"Error {e.status}: {e.details}")
    if e.warnings:
        print(f"Suggestions: {e.warnings}")
```

### Autocomplete

```python
# Get card name suggestions
suggestions = scrython.Cards(autocomplete='light')

for name in suggestions.data:
    print(name)
# Output: "Light", "Lightning Bolt", "Lightning Strike", ...
```

### Collection Queries

```python
# Fetch multiple cards by their identifiers
identifiers = [
    {'id': '5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d'},
    {'name': 'Lightning Bolt', 'set': 'lea'},
    {'multiverse_id': 409574}
]
cards = scrython.Cards(collection=identifiers)

for card in cards.data:
    print(f"{card.name} - {card.set}")
```

### Accessing Card Properties

```python
card = scrython.Cards(fuzzy='Lightning Bolt')

# Core identifiers
print(card.id)              # Scryfall UUID
print(card.oracle_id)       # Oracle ID (consistent across reprints)
print(card.multiverse_ids)  # Gatherer IDs

# Gameplay properties
print(card.mana_cost)       # "{R}"
print(card.cmc)             # 1.0
print(card.type_line)       # "Instant"
print(card.oracle_text)     # Card rules text
print(card.colors)          # ["R"]
print(card.legalities)      # Format legality

# Print properties
print(card.artist)          # Artist name
print(card.set_name)        # Full set name
print(card.rarity)          # "common", "uncommon", etc.
print(card.image_uris)      # Image URLs
print(card.prices)          # Price information

# Multi-face cards
if card.card_faces:
    for face in card.card_faces:
        print(f"{face.name}: {face.mana_cost}")
```

### Caching & Performance

```python
from functools import lru_cache
import scrython

@lru_cache(maxsize=1000)
def get_card_by_name(name: str):
    """Cache card lookups to avoid duplicate requests."""
    return scrython.Cards(fuzzy=name)

# First call makes API request
card1 = get_card_by_name('Lightning Bolt')

# Second call returns cached result (no API request)
card2 = get_card_by_name('Lightning Bolt')
```

## Breaking changes
Since Scryfall's API is constantly changing, this library will also be changing.

Versions will be broken down as such:

x.0.0: Overall library version

0.x.0: Major version changes. Includes anything that will break functionality from previous version, or adds upon them.

0.0.x: Minor patch changes.

>It's important to keep up to date with library changes, since it relies on how Scryfall has updated it's own API. If they change something, my library will potentially break or be outdated until a fix is patched.

## Key notes
There will be no attempts to keep backwards compatibility for the duration of this project.

There is no default rate limiting for this library. Not all projects are created equal, so not all of them will need a universal limit. It's up to the responsibility of the user to make sure they don't overload Scryfall's servers.

The simplest way to prevent sending too many requests too quickly is the following:

    >>> time.sleep(0.1)
    >>> card = scrython.cards.Random()

