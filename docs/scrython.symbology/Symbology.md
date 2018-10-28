# **class** `scrython.symbology.Symbology()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`Symbology().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|

## Returns
N/A

## Raises
N/A

## Examples
```python
>>> symbol = scrython.symbology.Symbology() 
```

## Methods

---
### `data()`

```
The data returned from the query

        Acceptable keys:
            symbol (string): The plaintext symbol, usually written with curly braces
            loose_variant (string): The alternate version of the symbol, without curly braces
            transposable (boolean): True if it's possibly to write the symbol backwards
            represents_mana (boolean): True if this is a mana symbol
            cmc (float): The total converted mana cost of the symbol
            appears_in_mana_costs (boolean): True if the symbol appears on the mana cost of any card
            funny (boolean): True if the symbol is featured on any funny cards
            colors (array): An array of all colors in the given symbol
            english (string): An english sentence describing the mana cost
            gatherer_alternate (array): An array of Gatherer like costs

        Args:
            index (integer, optional): Defaults to None. Access a specific index.
            key (string, optional): Defaults to None. Returns the value of the given key. Requires the `index` argument.

        Returns:
            List: The full list of data.
            Dictionary: If given an index
            String: If given an index and key.
        
```
---
### `data_length()`

```
The length of the data returned
        
        Returns:
            integer
        
```
---
### `has_more()`

```
True if there are more pages to the object
        
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