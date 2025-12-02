# Scrython

Scrython is a wrapper for the Scryfall API, designed for an easier use.

[Here is a link to the Scryfall API documentation.](https://scryfall.com/docs/api)

## Installation

Scrython is available in PyPI, and requires no other dependencies.

```python
pip install scrython
```

## ⚠️ Important: Rate Limiting

**Good news!** Scrython 2.0 now includes **built-in rate limiting** enabled by default, enforcing Scryfall's 10 requests/second guideline automatically. You no longer need to manually add delays between requests.

**Scryfall requires 50-100 milliseconds delay between requests** (~10 requests/second maximum).

### Automatic Rate Limiting (Default):

```python
import scrython

# Rate limiting is automatic! No delays needed
cards_to_fetch = ['Lightning Bolt', 'Counterspell', 'Black Lotus']

for card_name in cards_to_fetch:
    card = scrython.cards.Named(fuzzy=card_name)  # Automatically rate limited
    print(f"{card.name} - {card.set}")
```

### Custom Rate Limits:

```python
# Use a slower rate (5 requests/second)
card = scrython.cards.Named(fuzzy='Lightning Bolt', rate_limit_per_second=5)

# Disable rate limiting (use with caution!)
card = scrython.cards.Named(fuzzy='Lightning Bolt', rate_limit=False)
```

### Legacy Code (Manual Rate Limiting):

If you prefer manual rate limiting or need finer control:

```python
import scrython
import time

# Disable automatic rate limiting and use manual delays
for card_name in cards_to_fetch:
    card = scrython.cards.Named(fuzzy=card_name, rate_limit=False)
    print(f"{card.name} - {card.set}")
    time.sleep(0.1)  # 100ms delay
```

### Better: Use Bulk Data for Large Datasets

For large-scale data processing, use Scryfall's bulk data downloads instead:

```python
import scrython

# Download all unique cards at once
bulk = scrython.bulk_data.ByType(type='oracle_cards')
cards = bulk.download()

# Process all cards locally without rate limits!
for card in cards:
    print(f"{card['name']} - {card['set']}")

# Bulk data files are updated every 12 hours
```

### Built-in Caching

Scrython 2.0 includes built-in caching with TTL (time-to-live) support:

```python
import scrython

# Enable caching with 1-hour TTL (default)
card = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True)

# First call makes API request
card1 = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True)

# Second call returns cached result (no API request!)
card2 = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True)

# Custom TTL (in seconds)
card = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True, cache_ttl=7200)  # 2 hours
```

**Note:** Card prices become unreliable after 24 hours. Consider shorter TTLs for price-sensitive applications.

### Legacy Caching (functools.lru_cache):

You can still use Python's built-in caching if preferred:

```python
from functools import lru_cache
import scrython

@lru_cache(maxsize=1000)
def get_card_by_name(name: str):
    """Cache card lookups to avoid duplicate requests."""
    return scrython.cards.Named(fuzzy=name, rate_limit=False)

card1 = get_card_by_name('Lightning Bolt')
card2 = get_card_by_name('Lightning Bolt')  # Cached
```

### Custom User-Agent (Recommended)

Scryfall requests that applications identify themselves with a custom User-Agent:

```python
from scrython.base import ScrythonRequestHandler
import scrython

# Set custom User-Agent for your application
ScrythonRequestHandler.set_user_agent('MyMTGApp/1.0 (contact@example.com)')

# All subsequent requests will use your custom User-Agent
card = scrython.cards.Named(fuzzy='Black Lotus')
```

## Complete Usage Examples

### Basic Card Lookup

```python
import scrython

# Fuzzy name search (handles typos)
card = scrython.cards.Named(fuzzy='Light Bolt')
print(card.name)  # "Lightning Bolt"
print(card.mana_cost)  # "{R}"
print(card.type_line)  # "Instant"
print(card.oracle_text)

# Exact name match
card = scrython.cards.Named(exact='Black Lotus')
print(card.prices)
# {'usd': '25000.00', 'usd_foil': None, ...}
```

### Advanced Search

```python
# Search with Scryfall syntax
results = scrython.cards.Search(q='type:creature cmc:1 color:red')

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
card = scrython.cards.ByCodeNumber(code='znr', number='123')

# By various IDs
card = scrython.cards.ByMultiverseId(id=456789)
card = scrython.cards.ByMTGOId(id=67890)
card = scrython.cards.ById(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')

# Get random card
card = scrython.cards.Random()
card = scrython.cards.Random(q='rarity:mythic')  # Random mythic
```

### Working with Sets

```python
# Get all sets
all_sets = scrython.sets.All()

for set_obj in all_sets.data:
    print(f"{set_obj.name} ({set_obj.code}) - {set_obj.card_count} cards")

# Get specific set
set_obj = scrython.sets.ByCode(code='znr')
print(f"{set_obj.name} released on {set_obj.released_at}")
print(f"Set type: {set_obj.set_type}")
```

### Bulk Data Download

Bulk data files contain all Magic cards and are updated every 12 hours. This is the recommended approach for processing large datasets, as it avoids rate limits entirely.

```python
import scrython

# Get all bulk data options
all_bulk = scrython.bulk_data.All()

for bulk in all_bulk.data:
    print(f"{bulk.name}: {bulk.description}")
    print(f"Size: {bulk.size / 1_000_000:.1f} MB")

# Download oracle cards (all unique cards with Oracle text)
oracle_cards = scrython.bulk_data.ByType(type='oracle_cards')

# Option 1: Download and return data in memory
cards = oracle_cards.download()
print(f"Downloaded {len(cards)} cards")

# Process without rate limits!
for card in cards:
    if 'Lightning' in card['name']:
        print(card['name'])

# Option 2: Save to file
oracle_cards.download(filepath='oracle_cards.json')
print("Bulk data saved to oracle_cards.json")

# Option 3: Save without returning data (memory efficient)
oracle_cards.download(filepath='oracle_cards.json', return_data=False)

# Option 4: Show progress bar (requires: pip install scrython[progress])
cards = oracle_cards.download(progress=True)

# Available bulk data types:
# - 'oracle_cards': All unique cards with Oracle text
# - 'unique_artwork': All cards with unique artwork
# - 'default_cards': One version of each card
# - 'all_cards': All card printings
# - 'rulings': All card rulings
```

**Note:** The `download()` method automatically detects whether responses are gzip-compressed by checking HTTP `Content-Encoding` headers. This means it works seamlessly regardless of Scryfall's CDN configuration - you don't need to worry about compression formats.

### Error Handling

```python
from scrython.base import ScryfallError

try:
    card = scrython.cards.Named(exact='Nonexistent Card Name')
except ScryfallError as e:
    print(f"Error {e.status}: {e.details}")
    if e.warnings:
        print(f"Suggestions: {e.warnings}")
```

### Autocomplete

```python
# Get card name suggestions
suggestions = scrython.cards.Autocomplete(q='light')

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
cards = scrython.cards.Collection(data={'identifiers': identifiers})

for card in cards.data:
    print(f"{card.name} - {card.set}")
```

### Accessing Card Properties

```python
card = scrython.cards.Named(fuzzy='Lightning Bolt')

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

## Advanced Features (New in 2.0)

### Magic Methods

Cards and other objects now support Python magic methods for better developer experience:

```python
import scrython

card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Readable representation
print(repr(card))  # Object(id='abc123...', name='Lightning Bolt')
print(str(card))   # Lightning Bolt (LEA)

# Equality comparison (by ID)
card1 = scrython.cards.Named(fuzzy='Lightning Bolt')
card2 = scrython.cards.Named(exact='Lightning Bolt')
print(card1 == card2)  # True (same card ID)

# Use in sets and dicts (hashable)
unique_cards = {card1, card2, card3}  # Deduplicates by ID
card_lookup = {card1: 'owned', card2: 'wanted'}
```

### Serialization

Export and import card data easily:

```python
import scrython

card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Export to dict
card_dict = card.to_dict()

# Export to JSON
json_str = card.to_json(indent=2)

# Save to file
with open('card.json', 'w') as f:
    f.write(card.to_json())

# Import from dict (no API call!)
from scrython.cards.cards import Object
restored_card = Object.from_dict(card_dict)

# Export search results
results = scrython.cards.Search(q='bolt')
all_cards = results.to_list()  # List of dicts
```

### Iteration Support

Iterate directly over search results with Pythonic syntax:

```python
import scrython

results = scrython.cards.Search(q='c:red type:instant')

# Direct iteration (current page)
for card in results:
    print(card.name)

# Get length
print(len(results))  # Number of cards in current page

# Auto-pagination through ALL results
for card in results.iter_all():
    print(card.name)  # Automatically fetches all pages

# Works with list comprehensions
names = [card.name for card in results]

# Works with filter
red_cards = [c for c in results if c.has_color('R')]
```

### Convenience Methods

Quick access to common card operations:

```python
import scrython

card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Legality checks
if card.is_legal_in('commander'):
    print('Commander legal!')

# Color checks
if card.has_color('R'):
    print('Red card!')

# Type checks
if card.is_instant:
    print('Instant speed!')

# Also available: is_creature, is_sorcery, is_enchantment,
#                 is_artifact, is_planeswalker

# Price helpers
cheapest = card.lowest_price()
most_expensive = card.highest_price()
print(f'Price range: ${cheapest:.2f} - ${most_expensive:.2f}')

# Image helpers (handles double-faced cards)
url = card.get_image_url(size='large')
if url:
    print(f'Image: {url}')
```

### List Convenience Methods

Transform and filter search results easily:

```python
import scrython

results = scrython.cards.Search(q='bolt')

# Convert to dict keyed by name
by_name = results.as_dict(key='name')
print(by_name['Lightning Bolt'].set)

# Filter results
cheap_cards = results.filter(lambda c: c.lowest_price() and c.lowest_price() < 1.0)

# Map/transform results
card_names = results.map(lambda c: c.name)

# Chaining
lea_names = [c.name for c in results.filter(lambda c: c.set == 'lea')]
```

### Combining Features

Put it all together for powerful workflows:

```python
import scrython

# Search with caching and rate limiting
results = scrython.cards.Search(
    q='c:red cmc<=3',
    cache=True,
    cache_ttl=3600,
    rate_limit_per_second=5
)

# Iterate and filter
affordable_red = []
for card in results.iter_all():
    if card.is_legal_in('commander') and card.has_color('R'):
        price = card.lowest_price()
        if price and price < 5.0:
            affordable_red.append({
                'name': card.name,
                'price': price,
                'type': card.type_line
            })

# Export results
import json
with open('affordable_red.json', 'w') as f:
    json.dump(affordable_red, f, indent=2)

print(f'Found {len(affordable_red)} affordable red cards!')
```
