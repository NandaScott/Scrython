# Scrython

Scrython is a wrapper for the Scryfall API, designed for an easier use. Make sure to familiarize yourself with the docs.

[Here is a link to the Scryfall API documentation.](https://scryfall.com/docs/api)

# Dependencies
- `python` >= 3.5.3
- `asyncio` >= 3.4.3
- `aiohttp` >= 3.4.4

## Basic usage

You can install scrython by running `pip install scrython`. Note that it requires `asyncio` and `aiohttp` too.

Scrython can be imported using `import scrython` at the top of your code.
I've written to library to attempt to be familiar for those who already use it. As such, modules like `cards` are named to reflect the endpoints found in `api.scryfall.com/cards/`and so on.
For the most part I've kept all the class attributes the same as their key names, except for a few cases where I've found better functionality.

```
    >>>import scrython
    >>>card = scrython.cards.Named(fuzzy="Black Lotus")
    >>>card.name()
    'Black Lotus'
    >>>card.id()
    'bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd'
    >>>card.oracle_text()
    '{T}, Sacrifice Black Lotus: Add three mana of any one color to your mana pool.'
```

## Breaking changes
Since Scryfall's API is constantly changing, this library will also be changing.

Versions will be broken down as such:

x.0.0: Overall library version

0.x.0: Major version changes. Includes anything that will break functionality from previous version, or adds upon them.

0.0.x: Minor patch changes.

>It's important to keep up to date with library changes, since it relies on how Scryfall has updated it's own API. If they change something, my library will potentially break or be outdated until a fix is patched.

## Key notes
There will be no attempts to keep backwards compatibility for the duration of this project.

There is no default rate limiting for this library. Not all projects are created equal, so not all of them will need a universal limit. It's up to the responsibility of the user to make sure they don't overload Scryfall's servers.

The simplest way to prevent sending too many requests too quickly is the following:

    >>> time.sleep(0.1)
    >>> card = scrython.cards.Random()

