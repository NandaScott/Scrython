# Rulings

Documentation for a rulings object. These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`rulings.scryfallJson`).

## Attributes
All attributes are listed assuming the following
`rule = scrython.rulings.<Class>()` is the current usage.

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`object()`|String|Returns the type of object it is. (card, error, etc)|
|`had_more()`|Bool| If true, this ruling object has more rules than it currently displays.|
|`data()`|List|A list of ruling objects.
|`data_length()`|Integer|The length of the `data` list.|
|`ruling_object()`|String|The type of object for a given ruling. Requires an integer as a parameter, which acts as a tuple.|
|`ruling_source()`|String|The source of the ruling. Requires an integer as a parameter, which acts as a tuple.|
|`ruling_published_at()`|String|The date when the ruling was published. Requires an integer as a parameter, which acts as a tuple.|
|`ruling_comment()`|String|The effective ruling. Requires an integer as a parameter, which acts as a tuple.|

Example usage:

    rule = scrython.rulings.Id(id="0f91d225-788e-42fc-9d01-8668f672b717")
    rule.ruling_comment(5)
    >>>"If you control multiple As Foretolds, you may cast one spell for each of them paying {0}."

## *class* `rulings.Id()`
Gets the ruling of a card by the Scryfall Id.

**Parameters:**

| Param |Required [y/n]| Input type | Description |
| :---: | :---: | :---:  |:---: |
|id|Yes|String|The id of the card you want rulings for.|

Example usage:

    rule = scrython.rulings.Id(id='31412335-110c-449a-9c2f-bff8763a6504')

## *class* `rulings.Mtgo()`
Gets the ruling of a card by the Mtgo Id.

**Parameters:**

|Param|Required [y/n]|Input type|Description|
|:---:|:---:|:---:|:---:|
|id|Yes|String|The Mtgo id of the card you want rulings for.|

Example usage:

    rule = scrython.rulings.Mtgo(id="24811")

## *class* `rulings.Multiverse()`
Gets the ruling of a card by the Multiverse Id.

**Parameters:**

|Param|Required [y/n]|Input type|Description|
|:---:|:---:|:---:|:---:|
|id|Yes|String|The Multiverse Id of the card you want rulings for.|

Example usage:

    rule = scrython.rulings.Multiverse(id="124451")

## *class* `rulings.Code()`
Gets the ruling of a card by the set code and collector number.

**Parameters:**

|Param|Required [y/n]|Input type|Description|
|:---:|:---:|:---:|:---:|
|code|Yes|String|The 3 letter set code of the card.|
|collector_number|Yes|String|The collector number of the card.|

Example usage:

    rule = scrython.rulings.Code(code='CSP', collector_number='142')
