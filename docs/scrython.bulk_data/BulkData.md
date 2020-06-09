# **class** `scrython.bulk_data.BulkData()`

These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`BulkData().scryfallJson`).

## Args

|arg|type|description|
|:---:|:---:|:---:|

## Returns
object: The Scryfall endpoint object.

## Raises

|exception type|reason|
|:---:|:---:|
|Exception|Raised if Scryfall sends an error object.|

## Examples
```python
>>> data = scrython.bulk_data.BulkData() 
>>> data.bulk_compressed_size() 
```

## Methods

---
### `bulk_compressed_size()`

```
The size of the file in bytes
        
        Args:
            num (int): The index of the object in the `data` key
            human_readable (bool, optional): Defaults to False. Converts the bytes into a human readable format
        
        Returns:
            integer: Returns integer by default. 
            string: If human_readable is True, returns a string.
        
```
---
### `bulk_content_encoding()`

```
The encoding of the file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The encoding of the file
        
```
---
### `bulk_content_type()`

```
The MIME type of the file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The MIME type
        
```
---
### `bulk_description()`

```
A description of the object
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The description of the data item
        
```
---
### `bulk_id()`

```
The unique ID of the bulk item
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The Scryfall id of the object
        
```
---
### `bulk_name()`

```
The name of the type of bulk data object
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The name of the data item
        
```
---
### `bulk_object()`

```
Returns the type of object the specified index is
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The type of object
        
```
---
### `bulk_permalink_uri()`

```
None
```
---
### `bulk_type()`

```
The type of bulk data
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The type of the data item
        
```
---
### `bulk_updated_at()`

```
The time the item was last updated
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: Timestamp
        
```
---
### `bulk_uri()`

```
The URL that hosts the bulk file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: A URI to download the compressed data
        
```
---
### `data()`

```
A list of all types of types returned by the endpoints
        
        Returns:
            list: List of all types
        
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
Returns the type of object it is.
        (card, error, etc)
        
        Returns:
            string: The type of object
        
```