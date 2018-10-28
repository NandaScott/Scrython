# **class** `scrython.sets.Code()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`Code().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|
|code|string|The 3 letter code of the set.|
|format|string, optional|Returns data in the specified method. Defaults to JSON.|
|pretty|string, optional|Returns a prettier version of the json object. Note that this may break functionality with Scrython.|

## Returns
N/A

## Raises
N/A

## Examples
```python
>>> set = scrython.sets.Code(code="por") 
>>> set.name() 
```

## Methods

---
### `block()`

```
The full name of the block a set was in
        
        Returns:
            string
        
```
---
### `block_code()`

```
The the letter code for the block the set was in
        
        Returns:
            string
        
```
---
### `card_count()`

```
The number of cards in the set
        
        Returns:
            integer
        
```
---
### `code()`

```
The three letter set code of the set
        
        Returns:
            string
        
```
---
### `digital()`

```
True if this set is only featured on MTGO
        
        Returns:
            boolean
        
```
---
### `foil_only()`

```
True if this set only has foils
        
        Returns:
            boolean
        
```
---
### `icon_svg_uri()`

```
A URI to the SVG of the set symbol
        
        Returns:
            string
        
```
---
### `mtgo_code()`

```
The mtgo equivalent of `code()`
        
        Returns:
            string
        
```
---
### `name()`

```
The full name of the set
        
        Returns:
            string
        
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
### `parent_set_code()`

```
The set code for the parent set
        
        Returns:
            string
        
```
---
### `released_at()`

```
The date the set was launched
        
        Returns:
            string
        
```
---
### `search_uri()`

```
The scryfall API url for the search
        
        Returns:
            string
        
```
---
### `set_type()`

```
The type of the set (expansion, commander, etc)
        
        Returns:
            string
        
```