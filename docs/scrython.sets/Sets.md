# **class** `scrython.sets.Sets()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`Sets().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|
|format|string, optional|Returns data in the specified method. Defaults to JSON.|
|pretty|string, optional|Returns a prettier version of the json object. Note that this may break functionality with Scrython.|

## Returns
N/A

## Raises
N/A

## Examples
```python
>>> set = scrython.sets.Sets() 
>>> set.data(3, "name") 
```

## Methods

---
### `data()`

```
The data returned from the query

        Acceptable keys:
            object (string): The set object.
            code (string): The three letter set code of the set.
            mtgo_code (string): The mtgo equivalent of `code()`.
            name (string): The full name of the set.
            set_type (string): The type of the set (expansion, commander, etc)
            released_at (string): The date the set was launched.
            block_code (string): The the letter code for the block the set was in.
            block (string): The full name of the block a set was in.
            parent_set_code (string): The set code for the parent set.
            card_count (integer): The number of cards in the set.
            digital (boolean): True if this set is only featured on MTGO.
            foil_only (boolean): True if this set only has foils.
            icon_svg_uri (string): A URI to the SVG of the set symbol.
            search_uri (string): The scryfall API url for the search.

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
True if there are more pages available
        
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