# **class** `scrython.symbology.ParseMana()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`ParseMana().scryfallJson`).
    
## Args

|arg|type|description|
|:---:|:---:|:---:|
|cost|string|The given mana cost you want.|
|format|string, optional|Returns data in the specified method. Defaults to JSON.|
|pretty|string, optional|Returns a prettier version of the json object. Note that this may break functionality with Scrython.|

## Returns
N/A

## Raises

|exception type|reason|
|:---:|:---:|

## Examples
```python
>>> mana = scrython.symbology.ParseMana(cost="xcug") 
>>> mana.colors() 
```

## Methods

---
### `cmc()`

```
The converted mana cost of the card 
        
        Returns:
            float
        
```
---
### `colorless()`

```
True if the mana cost is colorless
        
        Returns:
            boolean
        
```
---
### `colors()`

```
A list of all colors in the mana cost
        
        Returns:
            list
        
```
---
### `mana_cost()`

```
The formatted mana cost
        
        Returns:
            string
        
```
---
### `monocolored()`

```
True if the mana cost is mono colored
        
        Returns:
            boolean
        
```
---
### `multicolored()`

```
True if the mana cost is a multicolored cost
        
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