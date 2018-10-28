# **class** `scrython.cards.Search()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`Search().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|
|q|string|The query to search. This will be updated in the future.|
|order|string, optional|Defaults to \'none\' The order you\'d like the data returned.|
|unique|string, optional|Defaults to \'none\' A way to filter similar cards.|
|include_extras|boolean, optional|Defaults to \'false\' Includes cards that are normally omitted from search results, like Un-|
|include_multilingual|boolean, optional|Defaults to \'false\' Includes cards that are in the language specified.|
|page|integer, optional|Defaults to \'1\' The page number you\'d like to search, if any.|
|format|string, optional|Defaults to \'json\'. Returns data in the specified method.|
|face|string, optional|Defaults to empty string. If you\'re using the `image` format, this will specify if you want the front or back face.|
|version|string, optional|Defaults to empty string. If you\'re using the `image` format, this will specify if you want the small, normal, large, etc version of the image.|
|pretty|string, optional|Defaults to empty string. Returns a prettier version of the json object. Note that this may break functionality with Scrython.|

## Returns
N/A

## Raises

|exception type|reason|
|:---:|:---:|
|Exception|If the \'q\' parameter is not provided.|
|Exception|If the object returned is an error.|

## Examples
```python
>>> search = scrython.cards.Search(q="++e:A25", order="spoiled") 
>>> search.data() 
```

## Methods

---
### `data()`

```
The data returned from the query

        You may reference any keys that could be accessed in a card object.
        There are far too many to list here, but you may find a list if applicable
        keys in the documentation.

        Args:
            index (integer, optional): Defaults to None. Access a specific index.
            key (string, optional): Defaults to None. Returns the value of the given key. Requires the `index` argument.
        
        Returns:
            List: The full list of data.
            Dictionary: If given an index.
            String: If given an index and key.
        
```
---
### `data_length()`

```

        
        Returns:
            integer: The length of data returned
        
```
---
### `has_more()`

```
Determines if there are more pages of results.
        
        Returns:
            boolean: True if there is more than 1 page of results
        
```
---
### `next_page()`

```
The API URI to the next page of the query
        
        Returns:
            string: A URI to the next page of the query
        
```
---
### `object()`

```
Returns the type of object it is.
        (card, error, etc)
        
        Returns:
            string: The type of object
        
```
---
### `total_cards()`

```
How many cards are returned from the query
        
        Returns:
            integer: The number of cards returned
        
```