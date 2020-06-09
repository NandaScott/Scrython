# **class** `scrython.cards.Id()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`Id().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|
|id|string|The Scryfall Id of the card.|
|format|string, optional|Defaults to \'json\'. Returns data in the specified method.|
|face|string, optional|Defaults to empty string. If you\'re using the `image` format, this will specify if you want the front or back face.|
|version|string, optional|Defaults to empty string. If you\'re using the `image` format, this will specify if you want the small, normal, large, etc version of the image.|
|pretty|string, optional|Defaults to empty string. Returns a prettier version of the json object. Note that this may break functionality with Scrython.|

## Returns
N/A

## Raises

|exception type|reason|
|:---:|:---:|
|Exception|If the \'id\' parameter is not provided.|
|Exception|If the object returned is an error.|

## Examples
```python
>>> card = scrython.cards.Id(id="5386a61c-4928-4bd1-babe-5b089ab8b2d9") 
>>> card.name() 
```

## Methods

---
### `all_parts()`

```
This this card is closely related to other cards, this property will be an list with it
        
        Returns:
            list
        
```
---
### `arena_id()`

```
The Arena ID of the card, if any
        
        Returns:
            int: The Arena ID of the card, if any
        
```
---
### `artist()`

```
The artist of the card
        
        Returns:
            string
        
```
---
### `border_color()`

```
The color of the card border
        
        Returns:
            string
        
```
---
### `card_faces()`

```
If it exists, all parts found on a card's face will be found as an object from this list
        
        Returns:
            list
        
```
---
### `cmc()`

```
A float of the converted mana cost of the card
        
        Returns:
            float: The cmc of the card
        
```
---
### `collector_number()`

```
The collector number of the card
        
        Returns:
            string
        
```
---
### `color_identity()`

```
A list of strings with all colors found on the card itself
        
        Returns:
            list
        
```
---
### `color_indicator()`

```
An list of all colors found in this card's color indicator
        
        Returns:
            list
        
```
---
### `colors()`

```
A list of strings with all colors found in the mana cost
        
        Returns:
            list
        
```
---
### `digital()`

```
Returns True if the card is the digital version
        
        Returns:
            boolean
        
```
---
### `edhrec_rank()`

```
The rank of the card on edhrec.com
        
        Returns:
            int: The rank of the card on edhrec.co
        
```
---
### `flavor_text()`

```
The flavor text of the card, if any
        
        Returns:
            string
        
```
---
### `foil()`

```
True if this printing exists in a foil version
        
        Returns:
            boolean
        
```
---
### `frame()`

```
The year of the card frame
        
        Returns:
            string
        
```
---
### `frame_effects()`

```
The card's frame effect, if any. (miracle, nyxtouched, etc.)
        
        Returns:
            list: The card's frame effects.
        
```
---
### `full_art()`

```
Returns True if the card is considered full art
        
        Returns:
            boolean
        
```
---
### `games()`

```
A list of games that this card print is available in.

        Returns:
            array: A list of games
        
```
---
### `hand_modifier()`

```
This cards hand modifier value, assuming it's a Vanguard card
        
        Returns:
            string
        
```
---
### `highres_image()`

```
Determine if a card has a highres scan available
        
        Returns:
            boolean
        
```
---
### `id()`

```
A unique ID for the returned card object
        
        Returns:
            string
        
```
---
### `illustration_id()`

```
The related id of the card art
        
        Returns:
            string
        
```
---
### `image_uris()`

```
All image uris of the card in various qualities

        An index and an image type must be supplied a single uri.

        If the card has additional faces, the returned dict will
        default to the front of the card.

        Returns:
            dict: If given no arguments
            string: If given an index and image_type

        Raises:
            Exception: If given no index
            KeyError: If the given image type is not a known type
        
```
---
### `lang()`

```
The language of the card
        
        Returns:
            string
        
```
---
### `layout()`

```
The image layout of the card. (normal, transform, etc)
        
        Returns:
            string
        
```
---
### `legalities()`

```
A dictionary of all formats and their legality
        
        Returns:
            dict
        
```
---
### `life_modifier()`

```
This is the cards life modifier value, assuming it's a Vanguard card
        
        Returns:
            string
        
```
---
### `loyalty()`

```
This card's loyalty. Some loyalties may be X rather than a number
        
        Returns:
            string
        
```
---
### `mana_cost()`

```
The full mana cost using shorthanded mana symbols
        
        Returns:
            string
        
```
---
### `mtgo_foil_id()`

```
The corresponding MTGO foil ID of the card
        
        Returns:
            integer: The Magic Online foil id of the card
        
```
---
### `mtgo_id()`

```
The official MTGO id of the of the card
        
        Returns:
            integer: The Magic Online id of the card
        
```
---
### `multiverse_ids()`

```
The official Gatherer multiverse ids of the card
        
        Returns:
            list
        
```
---
### `name()`

```
The oracle name of the card
        
        Returns:
            string
        
```
---
### `nonfoil()`

```
True if this printing does not exist in foil
        
        Returns:
            boolean
        
```
---
### `object()`

```
Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        
```
---
### `oracle_id()`

```
A unique ID for this card's oracle text
        
        Returns:
            string
        
```
---
### `oracle_text()`

```
The official oracle text of a card
        
        Returns:
            string
        
```
---
### `oversized()`

```
True if this printing is an oversized card
        
        Returns:
            boolean
        
```
---
### `power()`

```
The power of the creature, if applicable
        
        Returns:
            string
        
```
---
### `preview()`

```
Preview information for this card, if any.
        You may pass the name of a valid key to return the value of that key.
        Such as a source_uri.
        
        Args:
            key (string): A key for specific information about the preview.

        Returns:
            dict: If provided no key, the entire dict is returned.
            string: If provided a key, the value of that key is returned.
        
```
---
### `prices()`

```
Returns prices from modes `usd`, `usd_foil`, `eur`, and `tix`
        
        Args:
            mode (string): The prices to get
        
        Raises:
            KeyError: If the mode parameter does not match a known key
        
        Returns:
            float: The prices as a float
        
```
---
### `printed_name()`

```
If the card is in a non-English language, this will be the name as it appears on the card
        
        Returns:
            string
        
```
---
### `printed_text()`

```
If the card is in a non-English language, this will be the rules text as it appears on the card
        
        Returns:
            string
        
```
---
### `printed_type_line()`

```
If the card is in a non-English language, this will be the type line as it appears on the card
        
        Returns:
            string
        
```
---
### `prints_search_uri()`

```
A link to where you can begin paginating all re/prints for this card on Scryfall’s API
        
        Returns:
            string
        
```
---
### `promo()`

```
True if this card is a promotional print.

        Returns:
            boolean
        
```
---
### `purchase_uris()`

```
A dictionary of links to purchase the card
        
        Returns:
            dict
        
```
---
### `rarity()`

```
The rarity of the card
        
        Returns:
            string
        
```
---
### `related_uris()`

```
A dictionary of related websites for this card
        
        Returns:
            dict
        
```
---
### `released_at()`

```
The date this card was first released.
        
        Returns:
            string: The date in ISO format
        
```
---
### `reprint()`

```
Returns True if the card has been reprinted before
        
        Returns:
            boolean
        
```
---
### `reserved()`

```
Returns True if the card is on the reserved list
        
        Returns:
            boolean
        
```
---
### `rulings_uri()`

```
The API uri for the rulings of the card
        
        Returns:
            string
        
```
---
### `scryfall_set_uri()`

```
The full link to the set on Scryfall
        
        Returns:
            string
        
```
---
### `scryfall_uri()`

```
The full Scryfall page of the card
        As if it was a URL from the site.
        
        Returns:
            string
        
```
---
### `set_code()`

```
The 3 letter code for the set of the card
        
        Returns:
            string
        
```
---
### `set_name()`

```
The full name for the set of the card
        
        Returns:
            string
        
```
---
### `set_search_uri()`

```
Same output as set_uri
        
        Returns:
            string
        
```
---
### `set_uri()`

```
The API uri for the full set list of the card
        
        Returns:
            string
        
```
---
### `story_spotlight()`

```
True if this card is featured in the story
        
        Returns:
            boolean
        
```
---
### `tcgplayer_id()`

```
The `productId` of the card on TCGplayer.

        Returns:
            integer: The TCGplayer id of the card
        
```
---
### `toughness()`

```
The toughness of the creature, if applicable
        
        Returns:
            string
        
```
---
### `type_line()`

```
The full type line of the card
        
        Returns:
            string
        
```
---
### `uri()`

```
The Scryfall API uri for the card
        
        Returns:
            string
        
```
---
### `watermark()`

```
The associated watermark of the card, if any
        
        Returns:
            string
        
```