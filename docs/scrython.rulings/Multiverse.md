# **class** `scrython.rulings.Multiverse()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`Multiverse().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|
|id|string|The multiverse id of the card you want rulings for.|
|format|string, optional|Returns data in the specified method. Defaults to JSON.|
|face|string, optional|If you\'re using the `image` format, this will specify if you want the front or back face.|
|version|string, optional|If you\'re using the `image` format, this will specify if you want the small, normal, large, etc version of the image.|
|pretty|string, optional|Returns a prettier version of the json object. Note that this may break functionality with Scrython.|

## Returns
N/A

## Raises

|exception type|reason|
|:---:|:---:|

## Examples
```python
>>> rule = scrython.rulings.Id(id="4301") 
>>> rule.data_length() 
```

## Methods

---
### `data()`

```
The data returned from the query

        Acceptable keys:
            object (string): The type of object for a given ruling.
            source (string): The source of the ruling.
            published_at (string): The date when the ruling was published.
            comment (string): The effective ruling.

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
The length of the `data` list.
        
        Returns:
            Integer
        
```
---
### `has_more()`

```
True if there is more than one page of results
        
        Returns:
            boolean: True if there are more results
        
```
---
### `object()`

```
Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        
```