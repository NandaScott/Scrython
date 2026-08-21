"""Property sweep engine: auto-asserts accessor passthroughs against the fixture corpus.

Every object type registers one SweepSpec below. The three parametrized tests
then run against all specs, so extending coverage to a new object type is a
single table entry rather than a new copy of the engine.
"""

import inspect
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from scrython.base_mixins import ScryfallCatalogMixin, ScryfallListMixin
from scrython.bulk_data import Object as BulkDataObject
from scrython.cards import Object
from scrython.sets import Object as SetsObject

FIXTURES_DIR = Path(__file__).parent / "fixtures"

AliasPath = str | tuple[str, str]


def _load_json(rel_path: str) -> dict[str, Any]:
    with open(FIXTURES_DIR / rel_path) as fh:
        data: dict[str, Any] = json.load(fh)
    payload = data.get("payload")
    if not isinstance(payload, dict):
        raise ValueError(
            f"Sweep fixture '{rel_path}' is missing a 'payload' field. "
            "Re-run the fixture capture script to refresh it."
        )
    return payload


def _properties(cls: type) -> list[str]:
    """Return all non-private @property names on a class."""
    return sorted(
        name
        for name, attr in inspect.getmembers(cls, predicate=lambda v: isinstance(v, property))
        if not name.startswith("_")
    )


def _resolve_alias(fixture: dict[str, Any], path: AliasPath) -> Any:
    """Look up a value via a simple key or a (parent, child) key path."""
    if isinstance(path, tuple):
        parent = fixture.get(path[0])
        return parent.get(path[1]) if isinstance(parent, dict) else None
    return fixture.get(path)


def _alias_reachable(fixture: dict[str, Any], path: AliasPath) -> bool:
    """True when the alias target key (or its parent) exists in the fixture."""
    if isinstance(path, tuple):
        return path[0] in fixture
    return path in fixture


# ─── Bare wrapper classes for list/catalog ────────────────────────────────────


class _BareList(ScryfallListMixin):
    """Instantiable from a dict; list_data_type=None keeps data as a raw passthrough."""

    list_data_type: type | None = None

    def __init__(self, data: dict[str, Any]) -> None:
        self._scryfall_data = data  # type: ignore[assignment]


class _WrappedList(_BareList):
    """List envelope that wraps its items, mirroring how cards.Search is configured."""

    list_data_type = Object


class _BareCatalog(ScryfallCatalogMixin):
    """Instantiable from a dict."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._scryfall_data = data  # type: ignore[assignment]


# ─── Sweep spec ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SweepSpec:
    """One object type's sweep configuration.

    Args:
        name: Spec label; prefixes every generated test id.
        cls: Class introspected for @property accessors.
        build: Builds an instance from a fixture dict. Typed loosely because
            fixture dicts cross into TypedDict-annotated constructors here;
            this is the rehydration boundary.
        corpus: Fixture name to fixture JSON.
        exceptions: Accessors excluded from the passthrough sweep.
        aliases: Exception-set accessor to backing fixture path.
            str -> fixture[key]; tuple[str, str] -> fixture[t[0]][t[1]].
        covered_elsewhere: Exception-set accessor to the pytest node id of the
            test that owns its coverage. Node ids rather than prose so the
            self-tests can resolve them; a renamed owning test turns its entry
            red instead of rotting silently.
        wrappers: Fixture key to accessor(s) that read it, for keys reachable
            only through a wrapper whose name differs from the key.

    Every exception must appear in aliases or covered_elsewhere. The self-tests
    in test_sweep_engine_self.py enforce that across all specs, and resolve
    every covered_elsewhere node id to a real test function.
    """

    name: str
    cls: type
    build: Callable[[Any], Any]
    corpus: dict[str, dict[str, Any]]
    exceptions: frozenset[str] = frozenset()
    aliases: dict[str, AliasPath] = field(default_factory=dict)
    covered_elsewhere: dict[str, str] = field(default_factory=dict)
    wrappers: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def properties(self) -> frozenset[str]:
        return frozenset(_properties(self.cls))

    @property
    def alias_targets(self) -> frozenset[str]:
        """Top-level fixture keys reachable via the alias map.

        String values are direct key aliases; tuple values expose their parent key.
        """
        return frozenset(
            path if isinstance(path, str) else path[0] for path in self.aliases.values()
        )

    def reaches(self, key: str) -> bool:
        """True when some accessor exposes this top-level fixture key.

        A wrapper entry only counts while every accessor it names still exists,
        so renaming or deleting those accessors turns a stale entry red.
        """
        wrapper_accessors = self.wrappers.get(key, ())
        wrapper_covered = bool(wrapper_accessors) and all(
            accessor in self.properties for accessor in wrapper_accessors
        )
        return key in self.properties or key in self.alias_targets or wrapper_covered


# ─── Corpora ──────────────────────────────────────────────────────────────────

# Every corpus below names captured fixtures from tests/sweep/fixtures/. See the
# README there for why each fixture was captured and which fields it pins.


def _load_corpus(*fixture_names: str) -> dict[str, dict[str, Any]]:
    """Load the named captured fixtures, keyed by the name minus its endpoint prefix."""
    return {name.split("__", 1)[-1]: _load_json(f"{name}.json") for name in fixture_names}


# Card object fixtures: 12 layout pins plus 11 accessor pins, so that between
# them every optional card field lands on at least one fixture.
CARD_CORPUS: dict[str, dict[str, Any]] = _load_corpus(
    "cards_named__black_lotus",
    "cards_by_id__normal",
    "cards_by_id__transform",
    "cards_by_id__modal_dfc",
    "cards_by_id__split",
    "cards_by_id__adventure",
    "cards_by_id__saga",
    "cards_by_id__meld",
    "cards_by_id__flip",
    "cards_by_id__leveler",
    "cards_by_id__class",
    "cards_by_id__token",
    "cards_by_id__vanguard",
    "cards_by_id__japanese",
    "cards_by_id__japanese_dfc",
    "cards_by_id__attraction",
    "cards_by_id__indicator",
    "cards_by_id__content_warning",
    "cards_by_id__battle",
    "cards_by_id__battle_dfc",
    "cards_by_id__flavor_name",
    "cards_by_id__planeswalker",
    "cards_by_id__planeswalker_transform",
    "cards_by_id__reversible",
    "cards_by_id__etched",
    "cards_by_id__variation",
    "cards_by_id__watermark",
)

SET_CORPUS: dict[str, dict[str, Any]] = _load_corpus("sets_by_code__onc")

BULK_DATA_CORPUS: dict[str, dict[str, Any]] = _load_corpus("bulk_data_by_id__oracle_cards")

# List envelope fixtures (object == "list"). Only the paginated search carries
# next_page and only the mana_t search carries warnings, so those two fixtures
# are what cover those accessors.
LIST_CORPUS: dict[str, dict[str, Any]] = _load_corpus(
    "cards_search__lea_red",
    "cards_search__paginated",
    "cards_search__mana_t_warning",
)

# Catalog envelope fixtures (object == "catalog")
CATALOG_CORPUS: dict[str, dict[str, Any]] = _load_corpus("catalogs_creature_types")


# ─── Hand-maintained artifacts (one line to extend each) ─────────────────────

# Card accessor names excluded from the passthrough auto-sweep
CARD_EXCEPTIONS: frozenset[str] = frozenset(
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

CARD_ALIASES: dict[str, AliasPath] = {
    "card_id": "id",
    "previewed_at": ("preview", "previewed_at"),
    "preview_source_uri": ("preview", "source_uri"),
    "preview_source": ("preview", "source"),
}

# Alias-less exceptions: each maps to the pytest node id of the test that owns
# its coverage. The wrapped list accessors are covered by the gameplay-field
# type sweep, which parametrizes over them; the computed predicates are covered
# one test apiece.
CARD_COVERED_ELSEWHERE: dict[str, str] = {
    "all_parts": "tests/test_property_types.py::TestCardGameplayFields::test_gameplay_field_type",
    "card_faces": "tests/test_property_types.py::TestCardGameplayFields::test_gameplay_field_type",
    "is_creature": "tests/test_convenience.py::TestCardConvenienceMethods::test_is_creature",
    "is_instant": "tests/test_convenience.py::TestCardConvenienceMethods::test_is_instant",
    "is_sorcery": "tests/test_convenience.py::TestCardConvenienceMethods::test_is_sorcery",
    "is_enchantment": "tests/test_convenience.py::TestCardConvenienceMethods::test_is_enchantment",
    "is_artifact": "tests/test_convenience.py::TestCardConvenienceMethods::test_is_artifact",
    "is_planeswalker": "tests/test_convenience.py::TestCardConvenienceMethods::test_is_planeswalker",
}

CARD_WRAPPERS: dict[str, tuple[str, ...]] = {
    "preview": ("previewed_at", "preview_source_uri", "preview_source"),
}

# Sets, bulk data, list and catalog envelopes have no renamed or nested
# accessors, so they need no exceptions or aliases. Their `object` accessor is a
# hardcoded literal rather than a dict read; the passthrough sweep is still
# meaningful there because it pins that literal to the value Scryfall returns.
SWEEP_SPECS: tuple[SweepSpec, ...] = (
    SweepSpec(
        name="card",
        cls=Object,
        build=Object.from_dict,
        corpus=CARD_CORPUS,
        exceptions=CARD_EXCEPTIONS,
        aliases=CARD_ALIASES,
        covered_elsewhere=CARD_COVERED_ELSEWHERE,
        wrappers=CARD_WRAPPERS,
    ),
    SweepSpec(name="set", cls=SetsObject, build=SetsObject, corpus=SET_CORPUS),
    SweepSpec(name="bulk_data", cls=BulkDataObject, build=BulkDataObject, corpus=BULK_DATA_CORPUS),
    SweepSpec(name="list", cls=_BareList, build=_BareList, corpus=LIST_CORPUS),
    SweepSpec(name="catalog", cls=_BareCatalog, build=_BareCatalog, corpus=CATALOG_CORPUS),
)

# ─────────────────────────────────────────────────────────────────────────────

_SPECS_BY_NAME: dict[str, SweepSpec] = {spec.name: spec for spec in SWEEP_SPECS}


# ─── Parametrize lists ────────────────────────────────────────────────────────

_PASSTHROUGH_PARAMS = [
    pytest.param(spec.name, fname, prop, id=f"{spec.name}-{fname}-{prop}")
    for spec in SWEEP_SPECS
    for fname, fixture in spec.corpus.items()
    for prop in sorted(spec.properties)
    if prop not in spec.exceptions and prop in fixture
]

_EXCEPTION_PARAMS = [
    pytest.param(spec.name, fname, prop, id=f"{spec.name}-{fname}-{prop}")
    for spec in SWEEP_SPECS
    for fname, fixture in spec.corpus.items()
    for prop, alias in spec.aliases.items()
    if _alias_reachable(fixture, alias)
]

_REVERSE_PARAMS = [
    pytest.param(spec.name, fname, key, id=f"{spec.name}-{fname}-key:{key}")
    for spec in SWEEP_SPECS
    for fname, fixture in spec.corpus.items()
    for key in fixture
]


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_passthrough_check(spec: SweepSpec, fixture_name: str, accessor: str) -> None:
    """Core passthrough assertion: accessor value must equal its fixture key value."""
    fixture = spec.corpus[fixture_name]
    obj = spec.build(fixture)
    assert (
        getattr(obj, accessor) == fixture[accessor]
    ), f"{spec.name} accessor '{accessor}' value mismatch for fixture '{fixture_name}'"


@pytest.mark.parametrize("spec_name,fixture_name,accessor", _PASSTHROUGH_PARAMS)
def test_passthrough_sweep(spec_name: str, fixture_name: str, accessor: str) -> None:
    """Each passthrough accessor returns the same value as its fixture key."""
    spec = _SPECS_BY_NAME[spec_name]
    _run_passthrough_check(spec, fixture_name, accessor)


@pytest.mark.parametrize("spec_name,fixture_name,accessor", _EXCEPTION_PARAMS)
def test_exception_sweep(spec_name: str, fixture_name: str, accessor: str) -> None:
    """Each exception-set accessor is asserted against its aliased fixture value."""
    spec = _SPECS_BY_NAME[spec_name]
    fixture = spec.corpus[fixture_name]
    obj = spec.build(fixture)
    alias = spec.aliases[accessor]
    assert getattr(obj, accessor) == _resolve_alias(
        fixture, alias
    ), f"{spec_name} accessor '{accessor}' (alias {alias!r}) mismatch for fixture '{fixture_name}'"


@pytest.mark.parametrize("spec_name,fixture_name,key", _REVERSE_PARAMS)
def test_reverse_coverage_guard(spec_name: str, fixture_name: str, key: str) -> None:
    """Every top-level fixture key must be reachable through some accessor.

    Passes when the key matches a property name directly, appears as a target
    in the spec's alias map, or is declared in the spec's wrapper map with
    accessors that still exist. A failure here means Scryfall added (or the
    fixture contains) a field with no accessor, or a wrapper entry has gone
    stale.
    """
    spec = _SPECS_BY_NAME[spec_name]
    assert spec.reaches(key), (
        f"Fixture key '{key}' in {spec_name} fixture '{fixture_name}' has no accessor — "
        f"add a property, an alias entry, or a wrapper entry naming the accessor(s) "
        f"that read it"
    )


# ─── Wrapped list envelope ────────────────────────────────────────────────────

# The specs above sweep _BareList (list_data_type=None), which leaves the
# item-wrapping half of ScryfallListMixin.data untested. Search-style endpoints
# set list_data_type, so assert that path against the same fixture.


def test_wrapped_list_data_wraps_every_item() -> None:
    """A list envelope with list_data_type builds one wrapper per raw item."""
    wrapped = _WrappedList(LIST_CORPUS["lea_red"])
    assert all(isinstance(item, Object) for item in wrapped.data)


def test_wrapped_list_data_preserves_items() -> None:
    """Wrapping items does not alter their underlying data."""
    fixture = LIST_CORPUS["lea_red"]
    wrapped = _WrappedList(fixture)
    assert wrapped.to_list() == fixture["data"]
