# Catalog

Documentation for a catalog object. These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`card.scryfallJson`).

## Classes
All classes accept the following parameters.

| Param |Required [y/n]| Input type | Description |
| :---: | :---: | :---:  |:---: |
|format|No|String|The format to return. Defaults to JSON.|
|pretty|No|Boolean|Makes the returned JSON prettier. The library may not work properly with this setting.|

**Classes**
|Name|Description|
|`.ArtifactTypes()`|Returns all unique types of artifacts printed.|
|`.CardNames()`|Returns all unique card names printed.|
|`.CreatureTypes()`|Returns all unique creature types printed.|
|`.LandTypes()`|Returns all unique land types printed.|
|`.Loyalties()`|Returns all unique starting loyalties printed.|
|`.PlaneswalkerTypes()`|Returns all unique planeswalker types printed.|
|`.Powers()`|Returns all unique power values printed.|
|`.SpellTypes()`|Returns all unique spell types printed.|
|`.Toughnesses()`|Returns all unique toughness values printed.|
|`.Watermarks()`|Returns the name of all unique watermarks printed.|
|`.WordBanks()`|Returns all unique words ever printed on a card.|

## Attributes
All attributes are listed assuming the following
`catalog = scrython.catalog.<Class>()` is the current usage.

|Name|Data type returned|Description|
|:---:|:---:|:---:|
|`catalog.object()`|String|Returns the type of object it is. (card, error, etc)|
|`catalog.uri()`|String|The API URI for the endpoint you've called.|
|`catalog.total_values()`|Integer|The number of items in `data()`.|
|`catalog.data()`|List|A list of all types returned by the endpoint.|
