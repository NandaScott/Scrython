# Changelog

## 1.3.4

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
