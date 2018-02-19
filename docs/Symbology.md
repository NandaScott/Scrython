# Symbology

Documentation for a sets object. These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`symbology.scryfallJson`).

## *class* `Symbology()`

**Parameters**

There are no parameters needed to call this class.

**Attributes**

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`object()`|String|Returns the type of object it is. (card, error, etc)|
|`has_more()`|Boolean|True if there are more pages to the object.|
|`data()`|List|A list of all data returned.|
|`data_length()`|Integer|The length of the data returned.|
|`symbol_symbol(num)`|String|The plaintext symbol, usually written with curly braces. Requires an integer as a parameter, which acts as a tuple.|
|`symbol_loose_variant(num)`|String|The alternate version of the symbol, without curly braces. Requires an integer as a parameter, which acts as a tuple.|
|`symbol_transposable(num)`|Boolean|True if it's possibly to write the symbol backwards. Requires an integer as a parameter, which acts as a tuple.|
|`symbol_represents_mana(num)`|Boolean|True if this is a mana symbol. Requires an integer as a parameter, which acts as a tuple.|
|`symbol_cmc(num)`|Float|The total converted mana cost of the symbol. Requires an integer as a parameter, which acts as a tuple.|
|`symbol_appears_in_mana_costs(num)`|Boolean|True if the symbol appears on the mana cost of any card.Requires an integer as a parameter, which acts as a tuple.|
|`symbol_funny(num)`|Boolean|True if the symbol is featured on any funny cards. Requires an integer as a parameter, which acts as a tuple.|
|`symbol_colors(num)`|List|An array of all colors in the given symbol. Requires an integer as a parameter, which acts as a tuple.|

## *class* `ParseMana()`

**Parameters**

| Param |Required [y/n]| Input type | Function |
|:---:|:---:|:---:|:---:|
|`cost`|Yes|String|The given mana cost you want. (`RUG`)|

**Attributes**

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`object()`|String|Returns the type of object it is. (card, error, etc)|
|`mana_cost()`|String|The formatted mana cost.|
|`cmc()`|Float|The converted mana cost of the card.|
|`colors()`|List|A list of all colors in the mana cost.|
|`colorless()`|Boolean|True if the mana cost is colorless.|
|`monocolored()`|Boolean|True if the mana cost is mono colored.|
|`multicolored()`|Boolean|True if the mana cost is a multicolored cost.|
