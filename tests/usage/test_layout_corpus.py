"""
Smoke tests: one per Scryfall card layout.

Each test loads a committed fixture, stubs the HTTP layer, constructs via the
public API, and asserts a stable identity field.  Volatile fields (prices) are
never asserted.

Covered layouts (update this list when Scryfall exposes a new layout value):
    adventure   - front face + adventure instant/sorcery on one card
    class       - enchantment with leveling class abilities
    flip        - two-faced card rotated 180° on a single physical card
    leveler     - creature with level counters and banded stat blocks
    meld        - two separate cards that combine into a single double-sized card
    modal_dfc   - double-faced card where the player chooses which face to play
    normal      - standard single-faced Magic card
    saga        - enchantment with chapter I/II/III lore counter abilities
    split       - two halves on one card, each castable independently
    token       - token permanent (no mana cost, not in booster packs)
    transform   - double-faced card with a triggered or automatic flip
"""

import scrython.cards


def test_layout_normal(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_named_black_lotus"))
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
    assert card.layout == "normal"


def test_layout_transform(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_transform"))
    card = scrython.cards.Named(exact="Delver of Secrets // Insectile Aberration")
    assert card.name == "Delver of Secrets // Insectile Aberration"
    assert card.layout == "transform"


def test_layout_modal_dfc(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_modal_dfc"))
    card = scrython.cards.Named(exact="Emeria's Call // Emeria, Shattered Skyclave")
    assert card.name == "Emeria's Call // Emeria, Shattered Skyclave"
    assert card.layout == "modal_dfc"


def test_layout_split(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_split"))
    card = scrython.cards.Named(exact="Fire // Ice")
    assert card.name == "Fire // Ice"
    assert card.layout == "split"


def test_layout_adventure(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_adventure"))
    card = scrython.cards.Named(exact="Bonecrusher Giant // Stomp")
    assert card.name == "Bonecrusher Giant // Stomp"
    assert card.layout == "adventure"


def test_layout_saga(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_saga"))
    card = scrython.cards.Named(exact="Binding the Old Gods")
    assert card.name == "Binding the Old Gods"
    assert card.layout == "saga"


def test_layout_meld(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_meld"))
    card = scrython.cards.Named(exact="Gisela, the Broken Blade")
    assert card.name == "Gisela, the Broken Blade"
    assert card.layout == "meld"


def test_layout_token(stub_response, load_fixture):
    # Tokens cannot be fetched by name, so construct by id the way the fixture
    # was captured (and the way a user would actually retrieve a token).
    stub_response("cards/id", load_fixture("cards_layout_token"))
    card = scrython.cards.ById(id="6adb8607-1066-451d-a719-74ad32358278")
    assert card.name == "Zombie"
    assert card.layout == "token"


def test_layout_flip(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_flip"))
    card = scrython.cards.Named(exact="Nezumi Shortfang // Stabwhisker the Odious")
    assert card.name == "Nezumi Shortfang // Stabwhisker the Odious"
    assert card.layout == "flip"


def test_layout_leveler(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_leveler"))
    card = scrython.cards.Named(exact="Transcendent Master")
    assert card.name == "Transcendent Master"
    assert card.layout == "leveler"


def test_layout_class(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_layout_class"))
    card = scrython.cards.Named(exact="Fighter Class")
    assert card.name == "Fighter Class"
    assert card.layout == "class"
