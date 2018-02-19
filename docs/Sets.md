# Sets

Documentation for a sets object. These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`sets.scryfallJson`).

## *class* `Code()`

**Attributes**

All attributes are listed assuming the following
`card = scrython.sets.<Class>()` is the current usage.

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`object()`|String|Returns the type of object it is. (card, error, etc)|
|`code()`|String|The three letter set code of the set|
|`mtgo_code()`|String|The mtgo equivalent of `code()`|
|`name()`|String|The full name of the set.|
|`set_type()`|String|The type of the set (expansion, commander, etc)|
|`released_at()`|String|The date the set was launched.|
|`block_code()`|String|The the letter code for the block the set was in.|
|`block()`|String|The full name of the block a set was in.|
|`parent_set_code()`|String| The set code for the parent set.|
|`card_count()`|Integer| The number of cards in the set.|
|`digital()`|Boolean| True if this set is only featured on MTGO.|
|`foil()`|Boolean|True if this set only has foils.|
|`icon_svg_uri()`|String| A URI to the SVG of the set symbol.|
|`search_uri()`|String|The scryfall API url for the search.|

## *class* `Sets()`

`Sets()` gets it's own special attributes that don't match with the normal set attributes.

**Parameters**

No parameters are required.

**Attributes**

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`object()`|String|Returns the type of object it is. (card, error, etc)|
|`has_more()`|Boolean| True if there are more pages available.|
|`data()`|List| List of all data returned.|
|`data_length()`|Integer|The length of the data returned.|
|`set_object(num)`|String| The set object. Requires an integer as a parameter.|
|`set_code(num)`|String|The three letter set code of the set Requires an integer as a parameter.|
|`set_mtgo_code(num)`|String|The mtgo equivalent of `code()` Requires an integer as a parameter.|
|`set_name(num)`|String|The full name of the set. Requires an integer as a parameter.|
|`set_set_type(num)`|String|The type of the set (expansion, commander, etc) Requires an integer as a parameter.|
|`set_released_at(num)`|String|The date the set was launched. Requires an integer as a parameter.|
|`set_block_code(num)`|String|The the letter code for the block the set was in. Requires an integer as a parameter.|
|`set_block(num)`|String|The full name of the block a set was in. Requires an integer as a parameter.|
|`set_parent_set_code(num)`|String| The set code for the parent set. Requires an integer as a parameter.|
|`set_card_count(num)`|Integer| The number of cards in the set. Requires an integer as a parameter.|
|`set_digital(num)`|Boolean| True if this set is only featured on MTGO. Requires an integer as a parameter.|
|`set_foil(num)`|Boolean|True if this set only has foils. Requires an integer as a parameter.|
|`set_icon_svg_uri(num)`|String| A URI to the SVG of the set symbol. Requires an integer as a parameter.|
|`set_search_uri(num)`|String|The scryfall API url for the search. Requires an integer as a parameter.|
