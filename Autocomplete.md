# **class** `Autocomplete()`
These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`{Class_name}().scryfallJson`).
|cards/autocomplete|
|Get a list of potential autocompletion phrases.|

## Args

| arg | description |
|:---:|:---:|
|q (string):
|The query of the autocompletion.|
|format (string, optional):
|Defaults to 'json'.|
|Returns data in the specified method.|
|face (string, optional):
|Defaults to empty string.|
|If you're using the `image` format,|
|this will specify if you want the front or back face.|
|version (string, optional):
|Defaults to empty string.|
|If you're using the `image` format, this will specify|
|if you want the small, normal, large, etc version of the image.|
|pretty (string, optional):
|Defaults to empty string.|
|Returns a prettier version of the json object.|
|Note that this may break functionality with Scrython.|

## Raises

| arg | description |
|:---:|:---:|
|Exception: If the 'q' parameter is not provided.|
|Exception: If the object returned is an error.|

## Example usage

| arg | description |
|:---:|:---:|
|>>> auto = scrython.cards.Autocomplete(q="Thal")|
|>>> auto.total_items()|