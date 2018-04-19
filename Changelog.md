# Changelog

## 1.5.0

Changes

- Key errors are now handled more cleanly, and doesn't return two traceback errors.
- Updated Sets to be more like the other classes in structure.
- Updated symbology to be more like the other classes in structure.

## 1.4.2

Bugfixes

- `Search().has_more()` has been properly implemented. Whoops.

## 1.3.4

New stuff

- Added attributes `data_length()` and `data_tuple()` to `cards.Search()`.

Changes

- Updates all the classes for readability and DRYness.

## 1.3.0

New Stuff

- Scrython now uses the threading module to allow for discord.py implementations.

Changes

- Added `power()`, `toughness()`, and `flavor_text()` attributes to cards_object. Thanks to Mendess2526!

Bugfixes

- Fixed a bug that would prevent you from creating a cards.Autocomplete() object.

## 1.2.0

New Stuff

- Created this doc for everyone to keep track of changes to this library.
- All classes now have a docstring.
- Created an example script for checking cards in a .csv

Changes

- cards.Autocomplete() has had the `q` parameter updated to `query`.
- symbology.Parsemana() now has a required parameter of `code`.
- Updated the README with more information, and better organization.
