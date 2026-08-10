"""Usage tests for serialization round-tripping."""

import json

import scrython.cards


def test_named__to_dict__mutation_does_not_leak(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    result = card.to_dict()
    result["name"] = "MUTATED"
    assert card.name == "Black Lotus"


def test_named__to_json__round_trips(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    reconstructed = scrython.cards.Named.from_dict(json.loads(card.to_json()))
    assert reconstructed.name == card.name
    assert reconstructed.type_line == card.type_line


def test_named__from_dict__exposes_same_surface(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    reconstructed = scrython.cards.Named.from_dict(card.to_dict())
    assert reconstructed.name == card.name
    assert reconstructed.type_line == card.type_line


def test_named__from_dict__constructs_without_network():
    # No payload fixture — if urlopen were called this test would fail because
    # no stub is armed and the sandbox blocks outbound connections.
    data = {
        "object": "card",
        "name": "Test Card",
        "id": "00000000-0000-0000-0000-000000000001",
        "type_line": "Artifact",
    }
    card = scrython.cards.Named.from_dict(data)
    assert card.name == "Test Card"
    assert card.type_line == "Artifact"
