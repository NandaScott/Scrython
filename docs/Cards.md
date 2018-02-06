# Cards
Documentation for a card object. These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`card.scryfallJson`).

## Attributes
All attributes are listed assuming the following
`card = scrython.cards.<Class>()` is the current usage.

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`card.object()`|String | Returns the type of object it is. (card, error, etc)
|`card.id()`|String | The scryfall id of the card.
|`card.multiverse_ids()`|List | The associated multiverse ids of the card.
|`card.mtgo_id()`|Integer | The Magic Online id of the card.
|`card.mtgo_foil_id()`|Integer | The Magic Online foil id of the card.
|`card.name()`|String | The full name of the card. Cards with multiple faces are named with '//' as a seperator.
|`card.uri()`|String | The Scryfall API uri for the card.
|`card.scryfall_uri()`|String | The full Scryfall page of the card.
|`card.layout()`|String | The image layout of the card. (normal, transform, etc)
|`card.highres_image()`|Bool | Returns True if the card has a high res image.
|`card.image_uris()`|Dict | All image uris of the card in various qualities.
|`card.cmc()`|float | A float of the converted mana cost of the card.
|`card.type_line()`|String | The full type line of the card.
|`card.oracle_text()`|String | The official oracle text of a card.
|`card.mana_cost()`|String | The full mana cost using shorthanded mana symbols.
|`card.colors()`|List | An array of strings with all colors found in the mana cost.
|`card.color_identity()`|List | An array of strings with all colors found on the card itself.
|`card.legalities()`|Dict | A dictionary of all formats and their legality.
|`card.reserved()`|Bool | Returns True if the card is on the reserved list.
|`card.reprint()`|Bool | Returns True if the card has been reprinted before.
|`card.set()`|String | The 3 letter code for the set of the card.
|`card.set_name()`|String | The full name for the set of the card.
|`card.set_uri()`|String | The API uri for the full set list of the card.
|`card.set_search_uri()`|String | Same output as set_uri.
|`card.scryfall_set_uri()`|String | The full link to the set on Scryfall.
|`card.rulings_uri()`|String | The API uri for the rulings of the card.
|`card.prints_search_uri()`|String | A link to where you can begin paginating all re/prints for this card on Scryfall’s API.
|`card.collector_number()`|String | The collector number of the card.
|`card.digital()`|Bool | Returns True if the card is the digital version.
|`card.rarity()`|String | The rarity of the card.
|`card.illuStringation_id()`|String | The related id of the card art.
|`card.artist()`|String | The artist of the card.
|`card.frame()`|String | The year of the card frame.
|`card.full_art()`|Bool | Returns True if the card is considered full art.
|`card.border_color()`|String | The color of the card border.
|`card.timeshifted()`|Bool | Returns True if the card is timeshifted.
|`card.colorshifted()`|Bool | Returns True if the card is colorshifted.
|`card.futureshifted()`|Bool | Returns True if the card is futureshifted.
|`card.edhrec_rank()`|Integer | The rank of the card on edhrec.com
|`card.currency("<mode>")`|String |  Takes an argument for a currency, then returns a string of that value. (`currency("usd")>>"1.35"`). Current modes are `usd`, `eur`, and `tix`.
|`card.related_uris()`|Dict | A dictionary of related websites for this card.
|`card.purchase_uris()`|Dict | A dictionary of links to purchase the card.
|`card.life_modifier()`|String | This is the cards life modifier value, assuming it's a Vanguard card.
|`card.hand_modifier()`|String | This cards hand modifier value, assuming it's a Vanguard card.
|`card.color_indicator()`|List | An array of all colors found in this card's color indicator.
|`card.all_parts()`|List | This this card is closely related to other cards, this property will be an array with it.
|`card.card_faces()`|List | If it exists, all parts found on a card's face will be found as an object from this array.
|`card.watermark()`|String | The associated watermark of the card, if any.
|`card.story_spotlight_number()`|Integer | This card's story spotlight number, if any.
|`card.story_spotlight_uri()`|String | The URI for the card's story article, if any.
