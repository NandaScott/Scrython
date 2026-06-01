"""Property sweep engine: auto-asserts card accessor passthroughs against the fixture corpus."""

import inspect
import json
from pathlib import Path
from typing import Any

import pytest

from scrython.cards import Object

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_json(rel_path: str) -> dict[str, Any]:
    with open(FIXTURES_DIR / rel_path) as fh:
        return json.load(fh)


# Card object fixtures (direct card JSON, not list/catalog wrappers)
CARD_CORPUS: dict[str, dict[str, Any]] = {
    "named": _load_json("cards/named.json"),
    "random": _load_json("cards/random.json"),
}


# ─── Hand-maintained artifacts (one line to extend each) ─────────────────────

# Accessor names excluded from the passthrough auto-sweep
EXCEPTION_SET: frozenset[str] = frozenset(
    {
        "card_id",  # renamed: fixture key is "id"
        "all_parts",  # wrapped: returns RelatedCardObject list, not raw dicts
        "card_faces",  # wrapped: returns CardFaceObject list, not raw dicts
        "previewed_at",  # nested: fixture["preview"]["previewed_at"]
        "preview_source_uri",  # nested: fixture["preview"]["source_uri"]
        "preview_source",  # nested: fixture["preview"]["source"]
        "is_creature",  # computed from type_line; no matching fixture key
        "is_instant",  # computed from type_line; no matching fixture key
        "is_sorcery",  # computed from type_line; no matching fixture key
        "is_enchantment",  # computed from type_line; no matching fixture key
        "is_artifact",  # computed from type_line; no matching fixture key
        "is_planeswalker",  # computed from type_line; no matching fixture key
    }
)

# Maps assertable exception-set accessors to their backing fixture path.
# str  → fixture[key]
# tuple[str, str] → fixture[t[0]][t[1]]
ALIAS_MAP: dict[str, str | tuple[str, str]] = {
    "card_id": "id",
    "previewed_at": ("preview", "previewed_at"),
    "preview_source_uri": ("preview", "source_uri"),
    "preview_source": ("preview", "source"),
}

# ─────────────────────────────────────────────────────────────────────────────


def _card_properties() -> list[str]:
    """Return all non-private @property names on the card Object class."""
    return sorted(
        name
        for name, attr in inspect.getmembers(Object, predicate=lambda v: isinstance(v, property))
        if not name.startswith("_")
    )


def _resolve_alias(fixture: dict[str, Any], path: str | tuple[str, str]) -> Any:
    """Look up a value via a simple key or a (parent, child) key path."""
    if isinstance(path, tuple):
        parent = fixture.get(path[0])
        return parent.get(path[1]) if isinstance(parent, dict) else None
    return fixture.get(path)


def _alias_reachable(fixture: dict[str, Any], path: str | tuple[str, str]) -> bool:
    """True when the alias target key (or its parent) exists in the fixture."""
    if isinstance(path, tuple):
        return path[0] in fixture
    return path in fixture


# ─── Parametrize lists: (fixture_name, accessor) ─────────────────────────────

_PASSTHROUGH_PARAMS = [
    pytest.param(fname, prop, id=f"{fname}-{prop}")
    for fname, fixture in CARD_CORPUS.items()
    for prop in _card_properties()
    if prop not in EXCEPTION_SET and prop in fixture
]

_EXCEPTION_PARAMS = [
    pytest.param(fname, prop, id=f"{fname}-{prop}")
    for fname, fixture in CARD_CORPUS.items()
    for prop, alias in ALIAS_MAP.items()
    if _alias_reachable(fixture, alias)
]


# ─── Tests ────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("fixture_name,accessor", _PASSTHROUGH_PARAMS)
def test_passthrough_sweep(fixture_name: str, accessor: str) -> None:
    """Each passthrough accessor returns the same value as its fixture key."""
    fixture = CARD_CORPUS[fixture_name]
    card = Object.from_dict(fixture)
    assert (
        getattr(card, accessor) == fixture[accessor]
    ), f"accessor '{accessor}' value mismatch for fixture '{fixture_name}'"


@pytest.mark.parametrize("fixture_name,accessor", _EXCEPTION_PARAMS)
def test_exception_sweep(fixture_name: str, accessor: str) -> None:
    """Each exception-set accessor is asserted against its aliased fixture value."""
    fixture = CARD_CORPUS[fixture_name]
    card = Object.from_dict(fixture)
    expected = _resolve_alias(fixture, ALIAS_MAP[accessor])
    assert (
        getattr(card, accessor) == expected
    ), f"accessor '{accessor}' (alias {ALIAS_MAP[accessor]!r}) mismatch for fixture '{fixture_name}'"
