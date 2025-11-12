from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallCatalogMixin


class CardNames(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all card names in Scryfall's database.

    Endpoint: GET /catalog/card-names

    Returns a Catalog object containing an array of all canonical card names in English.
    Useful for autocomplete features and card name validation.

    Example:
        # Get all card names
        names = scrython.catalogs.CardNames()
        print(f"Total card names: {names.total_values}")

        # Check if a card exists
        if "Black Lotus" in names.data:
            print("Black Lotus exists in the database")

        # Search for cards starting with "Lightning"
        lightning_cards = [name for name in names.data if name.startswith("Lightning")]
        print(f"Found {len(lightning_cards)} cards starting with 'Lightning'")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/card-names"


class CreatureTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all creature types in Magic.

    Endpoint: GET /catalog/creature-types

    Returns a Catalog object containing an array of all creature types (tribes) that
    appear on creature cards. Useful for tribal deckbuilding and card validation.

    Example:
        # Get all creature types
        types = scrython.catalogs.CreatureTypes()

        # Check for specific tribes
        if "Elf" in types.data:
            print("Elf is a creature type")

        # List all types
        print(f"All {types.total_values} creature types:")
        for creature_type in sorted(types.data):
            print(f"  - {creature_type}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/creature-types"


class PlaneswalkerTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all planeswalker types in Magic.

    Endpoint: GET /catalog/planeswalker-types

    Returns a Catalog object containing an array of all planeswalker types
    (e.g., "Jace", "Chandra", "Liliana").

    Example:
        # Get all planeswalker types
        types = scrython.catalogs.PlaneswalkerTypes()

        if "Jace" in types.data:
            print("Jace is a planeswalker type")

        print(f"Total planeswalker types: {types.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/planeswalker-types"


class CardTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all card types in Magic.

    Endpoint: GET /catalog/card-types

    Returns a Catalog object containing an array of all card types
    (e.g., "Creature", "Instant", "Sorcery", "Artifact").

    Example:
        # Get all card types
        types = scrython.catalogs.CardTypes()

        print("All card types:")
        for card_type in types.data:
            print(f"  - {card_type}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/card-types"


class KeywordAbilities(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all keyword abilities in Magic.

    Endpoint: GET /catalog/keyword-abilities

    Returns a Catalog object containing an array of all keyword abilities
    (e.g., "Flying", "Trample", "Haste"). Useful for rules reference and
    card text parsing.

    Example:
        # Get all keyword abilities
        keywords = scrython.catalogs.KeywordAbilities()

        # Check for specific keywords
        if "Flying" in keywords.data:
            print("Flying is a keyword ability")

        # List all keywords
        print(f"Total keyword abilities: {keywords.total_values}")
        for keyword in sorted(keywords.data):
            print(f"  - {keyword}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/keyword-abilities"


class KeywordActions(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all keyword actions in Magic.

    Endpoint: GET /catalog/keyword-actions

    Returns a Catalog object containing an array of all keyword actions
    (e.g., "Destroy", "Exile", "Sacrifice"). These are action words with
    specific rules meanings.

    Example:
        # Get all keyword actions
        actions = scrython.catalogs.KeywordActions()

        if "Destroy" in actions.data:
            print("Destroy is a keyword action")

        print(f"Total keyword actions: {actions.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/keyword-actions"


class ArtifactTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all artifact types in Magic.

    Endpoint: GET /catalog/artifact-types

    Returns a Catalog object containing an array of all artifact types
    (e.g., "Equipment", "Vehicle", "Treasure").

    Example:
        # Get all artifact types
        types = scrython.catalogs.ArtifactTypes()

        if "Equipment" in types.data:
            print("Equipment is an artifact type")

        print("All artifact types:", ", ".join(sorted(types.data)))

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/artifact-types"


class EnchantmentTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all enchantment types in Magic.

    Endpoint: GET /catalog/enchantment-types

    Returns a Catalog object containing an array of all enchantment types
    (e.g., "Aura", "Saga", "Shrine").

    Example:
        # Get all enchantment types
        types = scrython.catalogs.EnchantmentTypes()

        if "Aura" in types.data:
            print("Aura is an enchantment type")

        print(f"Found {types.total_values} enchantment types")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/enchantment-types"


class LandTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all land types in Magic.

    Endpoint: GET /catalog/land-types

    Returns a Catalog object containing an array of all land types
    (e.g., "Plains", "Island", "Swamp", "Mountain", "Forest", "Desert", "Lair").

    Example:
        # Get all land types
        types = scrython.catalogs.LandTypes()

        # Check for basic land types
        basic_types = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
        for land_type in basic_types:
            if land_type in types.data:
                print(f"{land_type} is a land type")

        print(f"Total land types: {types.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/land-types"


class SpellTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all spell types in Magic.

    Endpoint: GET /catalog/spell-types

    Returns a Catalog object containing an array of all spell types
    (e.g., "Arcane", "Trap", "Adventure").

    Example:
        # Get all spell types
        types = scrython.catalogs.SpellTypes()

        if "Arcane" in types.data:
            print("Arcane is a spell type")

        print("All spell types:", types.data)

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/spell-types"


class ArtistNames(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all artist names in Magic.

    Endpoint: GET /catalog/artist-names

    Returns a Catalog object containing an array of all artist names that have
    illustrated Magic cards. Useful for artist search and attribution features.

    Example:
        # Get all artist names
        artists = scrython.catalogs.ArtistNames()

        # Check for a specific artist
        if "Rebecca Guay" in artists.data:
            print("Rebecca Guay has illustrated cards")

        print(f"Total artists: {artists.total_values}")

        # List all artists alphabetically
        for artist in sorted(artists.data):
            print(f"  - {artist}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/artist-names"


class WordBank(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all English words that appear in card text.

    Endpoint: GET /catalog/word-bank

    Returns a Catalog object containing an array of all English words that appear
    in oracle text on cards. Useful for card text search and analysis.

    Example:
        # Get all words from card text
        words = scrython.catalogs.WordBank()

        if "destroy" in words.data:
            print("'destroy' appears in card text")

        print(f"Total words: {words.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/word-bank"


class Supertypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all supertypes in Magic.

    Endpoint: GET /catalog/supertypes

    Returns a Catalog object containing an array of all supertypes
    (e.g., "Legendary", "Basic", "Snow", "World").

    Example:
        # Get all supertypes
        supertypes = scrython.catalogs.Supertypes()

        if "Legendary" in supertypes.data:
            print("Legendary is a supertype")

        print("All supertypes:", supertypes.data)

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/supertypes"


class BattleTypes(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all battle types in Magic.

    Endpoint: GET /catalog/battle-types

    Returns a Catalog object containing an array of all battle card types
    (e.g., "Siege").

    Example:
        # Get all battle types
        battles = scrython.catalogs.BattleTypes()

        if "Siege" in battles.data:
            print("Siege is a battle type")

        print(f"Total battle types: {battles.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/battle-types"


class Powers(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all possible power values for creatures.

    Endpoint: GET /catalog/powers

    Returns a Catalog object containing an array of all power values that appear
    on creature cards (e.g., "0", "1", "2", "*", "1+*").

    Example:
        # Get all power values
        powers = scrython.catalogs.Powers()

        if "*" in powers.data:
            print("* is a valid power value")

        print(f"Total power values: {powers.total_values}")
        print("Power values:", sorted(powers.data))

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/powers"


class Toughnesses(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all possible toughness values for creatures.

    Endpoint: GET /catalog/toughnesses

    Returns a Catalog object containing an array of all toughness values that appear
    on creature cards (e.g., "0", "1", "2", "*", "1+*").

    Example:
        # Get all toughness values
        toughnesses = scrython.catalogs.Toughnesses()

        if "*" in toughnesses.data:
            print("* is a valid toughness value")

        print(f"Total toughness values: {toughnesses.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/toughnesses"


class Loyalties(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all possible loyalty values for planeswalkers.

    Endpoint: GET /catalog/loyalties

    Returns a Catalog object containing an array of all loyalty values that appear
    on planeswalker cards (e.g., "3", "4", "5", "X").

    Example:
        # Get all loyalty values
        loyalties = scrython.catalogs.Loyalties()

        if "3" in loyalties.data:
            print("3 is a valid starting loyalty")

        print("Loyalty values:", sorted(loyalties.data))

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/loyalties"


class Watermarks(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all watermarks that appear on cards.

    Endpoint: GET /catalog/watermarks

    Returns a Catalog object containing an array of all watermark identifiers
    (e.g., "set", "planeswalker", "boros").

    Example:
        # Get all watermarks
        watermarks = scrython.catalogs.Watermarks()

        if "boros" in watermarks.data:
            print("Boros guild watermark exists")

        print(f"Total watermarks: {watermarks.total_values}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/watermarks"


class AbilityWords(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all ability words in Magic.

    Endpoint: GET /catalog/ability-words

    Returns a Catalog object containing an array of all ability words
    (e.g., "Adamant", "Addendum", "Alliance"). Ability words are italicized
    words that appear before triggered or activated abilities.

    Example:
        # Get all ability words
        words = scrython.catalogs.AbilityWords()

        if "Landfall" in words.data:
            print("Landfall is an ability word")

        print(f"Total ability words: {words.total_values}")
        for word in sorted(words.data):
            print(f"  - {word}")

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/ability-words"


class FlavorWords(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get a catalog of all flavor words in Magic.

    Endpoint: GET /catalog/flavor-words

    Returns a Catalog object containing an array of all flavor words that appear
    on cards. Flavor words are italicized words in card text that don't have
    rules meaning.

    Example:
        # Get all flavor words
        words = scrython.catalogs.FlavorWords()

        print(f"Total flavor words: {words.total_values}")
        print("Flavor words:", words.data)

    See: https://scryfall.com/docs/api/catalogs
    """

    _endpoint = "/catalog/flavor-words"


class Catalogs:
    """
    Smart factory for Catalogs API endpoints.

    Routes to the correct catalog endpoint based on the catalog_type parameter.

    Supported catalog types:
        - "card-names": All card names → CardNames
        - "creature-types": All creature types → CreatureTypes
        - "planeswalker-types": All planeswalker types → PlaneswalkerTypes
        - "card-types": All card types → CardTypes
        - "keyword-abilities": All keyword abilities → KeywordAbilities
        - "keyword-actions": All keyword actions → KeywordActions
        - "artifact-types": All artifact types → ArtifactTypes
        - "enchantment-types": All enchantment types → EnchantmentTypes
        - "land-types": All land types → LandTypes
        - "spell-types": All spell types → SpellTypes
        - "artist-names": All artist names → ArtistNames
        - "word-bank": All words in card text → WordBank
        - "supertypes": All supertypes → Supertypes
        - "battle-types": All battle types → BattleTypes
        - "powers": All power values → Powers
        - "toughnesses": All toughness values → Toughnesses
        - "loyalties": All loyalty values → Loyalties
        - "watermarks": All watermarks → Watermarks
        - "ability-words": All ability words → AbilityWords
        - "flavor-words": All flavor words → FlavorWords

    Example:
        # Get all creature types
        creatures = scrython.Catalogs("creature-types")
        print(f"Total creature types: {creatures.total_values}")

        # Get all keyword abilities
        keywords = scrython.Catalogs("keyword-abilities")
        if "Flying" in keywords.data:
            print("Flying is a keyword")

        # Get all card names
        names = scrython.Catalogs("card-names")
        print(f"Total cards: {names.total_values}")
    """

    def __new__(cls, catalog_type: str, **kwargs):
        catalog_map = {
            "card-names": CardNames,
            "creature-types": CreatureTypes,
            "planeswalker-types": PlaneswalkerTypes,
            "card-types": CardTypes,
            "keyword-abilities": KeywordAbilities,
            "keyword-actions": KeywordActions,
            "artifact-types": ArtifactTypes,
            "enchantment-types": EnchantmentTypes,
            "land-types": LandTypes,
            "spell-types": SpellTypes,
            "artist-names": ArtistNames,
            "word-bank": WordBank,
            "supertypes": Supertypes,
            "battle-types": BattleTypes,
            "powers": Powers,
            "toughnesses": Toughnesses,
            "loyalties": Loyalties,
            "watermarks": Watermarks,
            "ability-words": AbilityWords,
            "flavor-words": FlavorWords,
        }

        if catalog_type in catalog_map:
            return catalog_map[catalog_type](**kwargs)
        else:
            raise ValueError(
                f"Unknown catalog type: {catalog_type}. "
                f"Valid types: {', '.join(catalog_map.keys())}"
            )
