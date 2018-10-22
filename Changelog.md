# Changelog

## 1.6.0

New stuff
- Artist names have been added to `catalog`
- Multiple new functions have been added to `Cards`, `Symbology`

Changes
- Scrython has been changed to use spaces rather than tabs.
- Multiple functions have had their names updated to properly reflect the new key names.
- Some functions have been deleted entirely

Bugfixes

## 1.5.0

New stuff

- Arena IDs are now accessible from all `cards` objects with `arena_id()`.
- The `lang` attribute is now accessible from all `cards` objects with `lang()`
- `printed_name()`, `printed_type_line()`, `printed_text()` have been added to all `card`
    objects.
- `lang` optional argument has now been added to `Collector()` object. Defaults to `en`

Changes

- Key errors are now handled more cleanly, and doesn't return two traceback errors.
- Updated sets to be more like the other classes in structure.
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
