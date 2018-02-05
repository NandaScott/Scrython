# Cards
Documentation for a card object. These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`card.scryfallJson`).

## Attributes
All attributes are listed assuming the following
`card = scrython.cards.<Class>()` is the current usage.

## `card.object()`
str | Returns the type of object it is. (card, error, etc)
## `card.id()`
str | The scryfall id of the card.
## `card.multiverse_ids()`
arr | The associated multiverse ids of the card.
## `card.mtgo_id()`
int | The Magic Online id of the card.
## `card.mtgo_foil_id()`
int | The Magic Online foil id of the card.
## `card.name()`
str | The full name of the card. Cards with multiple faces are named with '//' as a seperator.
## `card.uri()`
str | The Scryfall API uri for the card.
## `card.scryfall_uri()`
str | The full Scryfall page of the card.
## `card.layout()`
str | The image layout of the card. (normal, transform, etc)
## `card.highres_image()`
bool | Returns True if the card has a high res image.
## `card.image_uris()`
dict | All image uris of the card in various qualities.
## `card.cmc()`
float | A float of the converted mana cost of the card.
## `card.type_line()`
str | The full type line of the card.
## `card.oracle_text()`
str | The official oracle text of a card.
## `card.mana_cost()`
str | The full mana cost using shorthanded mana symbols.
## `card.colors()`
arr | An array of strings with all colors found in the mana cost.
## `card.color_identity()`
arr | An array of strings with all colors found on the card itself.
## `card.legalities()`
dict | A dictionary of all formats and their legality.
## `card.reserved()`
bool | Returns True if the card is on the reserved list.
## `card.reprint()`
bool | Returns True if the card has been reprinted before.
## `card.set()`
str | The 3 letter code for the set of the card.
## `card.set_name()`
str | The full name for the set of the card.
## `card.set_uri()`
str | The API uri for the full set list of the card.
## `card.set_search_uri()`
str | Same output as set_uri.
## `card.scryfall_set_uri()`
str | The full link to the set on Scryfall.
## `card.rulings_uri()`
str | The API uri for the rulings of the card.
## `card.prints_search_uri()`
str | A link to where you can begin paginating all re/prints for this card on Scryfall’s API.
## `card.collector_number()`
str | The collector number of the card.
## `card.digital()`
bool | Returns True if the card is the digital version.
## `card.rarity()`
str | The rarity of the card.
## `card.illustration_id()`
str | The related id of the card art.
## `card.artist()`
str | The artist of the card.
## `card.frame()`
str | The year of the card frame.
## `card.full_art()`
bool | Returns True if the card is considered full art.
## `card.border_color()`
str | The color of the card border.
## `card.timeshifted()`
bool | Returns True if the card is timeshifted.
## `card.colorshifted()`
bool | Returns True if the card is colorshifted.
## `card.futureshifted()`
bool | Returns True if the card is futureshifted.
## `card.edhrec_rank()`
int | The rank of the card on edhrec.com
## `card.currency("<mode>")`
str |  Takes an argument for a currency, then returns a string of that value. (`currency("usd")>>"1.35"`). Current modes are `usd`, `eur`, and `tix`.
## `card.related_uris()`
dict | A dictionary of related websites for this card.
## `card.purchase_uris()`
dict | A dictionary of links to purchase the card.
## `card.life_modifier()`
str | This is the cards life modifier value, assuming it's a Vanguard card.
## `card.hand_modifier()`
str | This cards hand modifier value, assuming it's a Vanguard card.
## `card.color_indicator()`
arr | An array of all colors found in this card's color indicator.
## `card.all_parts()`
arr | This this card is closely related to other cards, this property will be an array with it.
## `card.card_faces()`
arr | If it exists, all parts found on a card's face will be found as an object from this array.
## `card.watermark()`
str | The associated watermark of the card, if any.
## `card.story_spotlight_number()`
int | This card's story spotlight number, if any.
## `card.story_spotlight_uri()`
str | The URI for the card's story article, if any.


