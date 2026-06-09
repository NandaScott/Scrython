"""
Smoke tests: one per Scryfall card layout.

Each layout is discovered via ``is:<layout>`` (``t:<layout>`` where no ``is:``
filter exists), pinned by id in ``scripts/capture_fixtures.py``, and fetched
here through ``scrython.cards.ById``. Asserting the ``layout`` keeps the corpus
honest without depending on volatile fields.

Covered layouts (update this list when Scryfall exposes a new layout value):
    adventure, class, flip, leveler, meld, modal_dfc, normal, saga, split,
    token, transform
"""

import scrython.cards


def test_by_id__id__has_normal_layout(cards_by_id__normal):
    card = scrython.cards.ById(id="a59c24d9-804b-45d0-b60c-cfc7a6af7ef5")
    assert card.layout == "normal"


def test_by_id__id__has_transform_layout(cards_by_id__transform):
    card = scrython.cards.ById(id="f8b8f0b4-71e1-4822-99a1-b1b3c2f10cb2")
    assert card.layout == "transform"


def test_by_id__id__has_modal_dfc_layout(cards_by_id__modal_dfc):
    card = scrython.cards.ById(id="c470539a-9cc7-4175-8f7c-c982b6072b6d")
    assert card.layout == "modal_dfc"


def test_by_id__id__has_split_layout(cards_by_id__split):
    card = scrython.cards.ById(id="9dc20e14-e304-4c14-a87b-322a76e214d5")
    assert card.layout == "split"


def test_by_id__id__has_adventure_layout(cards_by_id__adventure):
    card = scrython.cards.ById(id="c7d5e394-8e41-442e-ae97-a478a61e1b9d")
    assert card.layout == "adventure"


def test_by_id__id__has_saga_layout(cards_by_id__saga):
    card = scrython.cards.ById(id="3a613a01-6145-4e34-987c-c9bdcb068370")
    assert card.layout == "saga"


def test_by_id__id__has_meld_layout(cards_by_id__meld):
    card = scrython.cards.ById(id="e2b826be-4256-4fd6-ad4d-6c80933ee940")
    assert card.layout == "meld"


def test_by_id__id__has_flip_layout(cards_by_id__flip):
    card = scrython.cards.ById(id="864ad989-19a6-4930-8efc-bbc077a18c32")
    assert card.layout == "flip"


def test_by_id__id__has_leveler_layout(cards_by_id__leveler):
    card = scrython.cards.ById(id="c48e9f90-4b13-4281-943c-126be4ff1ce0")
    assert card.layout == "leveler"


def test_by_id__id__has_class_layout(cards_by_id__class):
    card = scrython.cards.ById(id="47ce8b7e-d8e1-489a-a69e-99089eeb8739")
    assert card.layout == "class"


def test_by_id__id__has_token_layout(cards_by_id__token):
    card = scrython.cards.ById(id="40b9dcb9-05c1-4a2e-b0cb-6554483ca5c9")
    assert card.layout == "token"
