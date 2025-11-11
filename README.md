# Scrython

Scrython is a wrapper for the Scryfall API, designed for an easier use.

[Here is a link to the Scryfall API documentation.](https://scryfall.com/docs/api)

## Installation

Scrython is available in PyPI, and requires no other dependencies.

```python
pip install scrython
```

## ⚠️ Important: Rate Limiting

There is no default rate limiting for this library. Not all projects are created equal, so not all of them will need a universal limit. It's up to the responsibility of the user to make sure they don't overload Scryfall's servers.

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

### Custom User-Agent (Recommended)

Scryfall requests that applications identify themselves with a custom User-Agent:

```python
import scrython

# Set custom User-Agent for your application
scrython.set_user_agent('MyMTGApp/1.0 (contact@example.com)')

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
print(card.card_id)              # Scryfall UUID
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
