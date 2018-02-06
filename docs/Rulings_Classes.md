# Rulings Classes

## `rulings.Id()`
Gets the ruling of a card by the Scryfall Id.

**Parameters:**

| Param |Required [y/n]| Input type | Description |
| :---: | :---: | :---:  |:---: |
|id|Yes|String|The id of the card you want rulings for.|

**Attributes:**
The same listed in the `rulings` documentation.

Example usage:
    rule = scrython.rulings.Id(id='31412335-110c-449a-9c2f-bff8763a6504')

## `rulings.Mtgo()`
Gets the ruling of a card by the Mtgo Id.

**Parameters:**

|Param|Required [y/n]|Input type|Description|
|:---:|:---:|:---:|:---:|
|id|Yes|String|The Mtgo id of the card you want rulings for.|

**Attributes:**
The same listed in the `rulings` documentation.

Example usage:
    rule = scrython.rulings.Mtgo(id="24811")

## `rulings.Multiverse()`
Gets the ruling of a card by the Multiverse Id.

**Parameters:**
|Param|Required [y/n]|Input type|Description|
|:---:|:---:|:---:|:---:|
|id|Yes|String|The Multiverse Id of the card you want rulings for.|

**Attributes:**
The same listed in the `rulings` documentation.

Example usage:
    rule = scrython.rulings.Multiverse(id="124451")

## `rulings.Code()`
Gets the ruling of a card by the set code and collector number.

**Parameters:**
|Param|Required [y/n]|Input type|Description|
|:---:|:---:|:---:|:---:|
|code|Yes|String|The 3 letter set code of the card.|
|collector_number|Yes|String|The collector number of the card.|

**Attributes:**
The same listed in the `rulings` documentation.

Example usage:
    rule = scrython.rulings.Code(code='CSP', collector_number='142')
