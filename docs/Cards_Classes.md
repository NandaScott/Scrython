# Cards Classes

## `cards.Named()`
Gets a card by the name.

**Parameters:**

| Param |Required [y/n]| Input type | Function |
| :---: | :---: | :---:  |:---: |
|fuzzy|Yes|string|Uses the fuzzy parameter for the card name.|
|exact|Yes|string|Uses the exact parameter for the card name.|
|set|No|string|Returns the set of the card if specified. If not the card edition will be the most recent printing. Requires the 3 letter set code.

**Attributes:**
The same listed in the `cards` documentation.

Since the `/cards/named` endpoint specifically requires the fuzzy or exact markers, they are required to be explicitly denoted.
Example usage:

    card = scrython.cards.Named(fuzzy="Blacker Lotus")
    card = scrython.cards.Named(exact="Saheeli Rai")
    card = scrython.cards.Named(fuzzy="Austere Command",
							    set="IMA")

## `cards.Random()`
Get a random card.

**Parameters:**
No parameters are required.

**Attributes:**
The same listed in the `cards` documentation.

Example usage:

    card = scrython.cards.Random()

## `cards.Multiverse()`
Get a card by Multiverse id

**Parameters:**

| Param |Required [y/n]| Input type | Function |
|:---:|:---:|:---:|:---:|
|id|Yes|Integer or String| This is the associated multiverse id of the given card.

**Attributes:**
The same listed in the `cards` documentation.

Example usage:

    card = scrython.cards.Multiverse(id="389511")

## `cards.Mtgo()`
Get a card by MTGO id.

**Parameters:**

| Param |Required [y/n]| Input type | Function |
|:---:|:---:|:---:|:---:|
|id|Yes|String|The required mtgo id of the card.

**Attributes:**
The same listed in the `cards` documentation.

Example usage:

    card = scrython.cards.Mtgo(id="14943")

## `cards.Collector()`
Get a card by collector number.

**Parameters:**

| Param |Required [y/n]| Input type | Function |
|:---:|:---:|:---:|:---:|
|code|Yes|String|This is the 3 letter code for the set|
|collector_number|Yes|String|This is the collector number of the card.|

**Attributes:**
The same listed in the `cards` documentation.

Example usage:

    card = scrython.cards.Collector(code="vma", collector_number="100")

## `cards.Id()`
Get a card by the Scryfall id.

**Attributes:**
The same listed in the `cards` documentation.

**Parameters:**

| Param |Required [y/n]| Input type | Function |
|:---:|:---:|:---:|:---:|
|id|Yes|String|The Scryfall Id of the card.|

Example usage:

    card = scrython.cards.Id(id="696ca38e-3035-492f-8f1b-258f60b8788c")

## `cards.Autocomplete()`
Get a list of potential autocompletion phrases.

**Parameters:**

| Param |Required [y/n]| Input type | Function |
|:---:|:---:|:---:|:---:|
|query|Yes|String| The query of the autocompletion.|

**Attributes:**

|Name|Output Type|Description|
|:--:|:--:|:--:|
|`object()`|String|Returns what kind of object it is.|
|`total_items()`|Integer|How many items are in the list.|
|`data()`|List|The list of potential autocompletes.|

Example usage:

    card = scrython.cards.Autocomplete(query="Ezuri")
