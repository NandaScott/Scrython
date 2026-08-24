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
from scrython.cards.cards_mixins import CardFaceMixin, RelatedCardsObjectMixin
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


def _alias_parts(path: AliasPath) -> tuple[str, str | None]:
    """Split an alias path into its top-level fixture key and optional nested child key."""
    if isinstance(path, tuple):
        return path[0], path[1]
    return path, None


def _resolve_alias(fixture: dict[str, Any], path: AliasPath) -> Any:
    """Look up a value via a simple key or a (parent, child) key path."""
    key, child = _alias_parts(path)
    value = fixture.get(key)
    if child is None:
        return value
    return value.get(child) if isinstance(value, dict) else None


def _alias_reachable(fixture: dict[str, Any], path: AliasPath) -> bool:
    """True when the alias target key (or its parent) exists in the fixture."""
    return _alias_parts(path)[0] in fixture


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


class _BareCardFace(CardFaceMixin):
    """Instantiable from a face dict; used to sweep CardFaceMixin in isolation."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._scryfall_data = data  # type: ignore[assignment]


class _BareRelatedCard(RelatedCardsObjectMixin):
    """Instantiable from a part dict; used to sweep RelatedCardsObjectMixin in isolation."""

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
        aliases: Accessor to backing fixture path, for accessors whose name
            differs from the key they read.
            str -> fixture[key]; tuple[str, str] -> fixture[t[0]][t[1]].
        covered_elsewhere: Accessor to the pytest node id of the test that owns
            its coverage. Node ids rather than prose so the self-tests can
            resolve them; a renamed owning test turns its entry red instead of
            rotting silently.
        wrappers: Fixture key to accessor(s) that read it, for keys reachable
            only through a wrapper whose name differs from the key.

    Declaring an accessor in aliases or covered_elsewhere is what excludes it
    from the passthrough sweep — see `exceptions`. The self-tests in
    test_sweep_engine_self.py resolve every covered_elsewhere node id to a real
    test function.
    """

    name: str
    cls: type
    build: Callable[[Any], Any]
    corpus: dict[str, dict[str, Any]]
    aliases: dict[str, AliasPath] = field(default_factory=dict)
    covered_elsewhere: dict[str, str] = field(default_factory=dict)
    wrappers: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def exceptions(self) -> frozenset[str]:
        """Accessors excluded from the passthrough sweep.

        Derived rather than declared: an accessor is exempt exactly when it
        declares where its coverage lives instead, so the two cannot drift.
        """
        return frozenset(self.aliases) | frozenset(self.covered_elsewhere)

    @property
    def properties(self) -> frozenset[str]:
        return frozenset(_properties(self.cls))

    @property
    def alias_targets(self) -> frozenset[str]:
        """Top-level fixture keys reachable via the alias map.

        String values are direct key aliases; tuple values expose their parent key.
        """
        return frozenset(_alias_parts(path)[0] for path in self.aliases.values())

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


def _load_subitem_corpus(*fixture_names: str, key: str) -> dict[str, dict[str, Any]]:
    """Extract sub-array items from card fixtures, keyed by fixture stem and item index.

    Each item in payload[key] becomes a separate corpus entry, so every face or
    related-card object can be swept independently as a first-class fixture row.

    Raises:
        ValueError: A named fixture carries no items under `key`. Such a fixture
            would contribute no rows and no signal, so it fails loudly instead.
    """
    corpus: dict[str, dict[str, Any]] = {}
    for name in fixture_names:
        payload = _load_json(f"{name}.json")
        items: list[dict[str, Any]] = payload.get(key) or []
        if not items:
            raise ValueError(
                f"Sweep fixture '{name}' has no '{key}' items and so contributes nothing "
                f"to this corpus. Drop it from the corpus list, or re-capture it from a "
                f"card that carries {key}."
            )
        stem = name.split("__", 1)[-1]
        for idx, item in enumerate(items):
            corpus[f"{stem}_{idx}"] = item
    return corpus


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

# Card face fixtures: one entry per face object extracted from multi-face card
# captures. Together these 9 fixtures cover all 23 CardFaceMixin accessors.
CARD_FACE_CORPUS: dict[str, dict[str, Any]] = _load_subitem_corpus(
    "cards_by_id__adventure",
    "cards_by_id__battle_dfc",
    "cards_by_id__flip",
    "cards_by_id__japanese_dfc",
    "cards_by_id__modal_dfc",
    "cards_by_id__planeswalker_transform",
    "cards_by_id__reversible",
    "cards_by_id__split",
    "cards_by_id__transform",
    key="card_faces",
)

# Related-card fixtures: one entry per all_parts item. All 6 RelatedCardsObjectMixin
# accessors appear in every fixture, so a single fixture would suffice, but including
# several gives richer parametrization.
RELATED_CARD_CORPUS: dict[str, dict[str, Any]] = _load_subitem_corpus(
    "cards_named__black_lotus",
    "cards_by_id__adventure",
    "cards_by_id__attraction",
    "cards_by_id__etched",
    "cards_by_id__meld",
    "cards_by_id__modal_dfc",
    "cards_by_id__planeswalker_transform",
    "cards_by_id__reversible",
    "cards_by_id__transform",
    key="all_parts",
)


# ─── Hand-maintained artifacts (one line to extend each) ─────────────────────

# Card accessors whose name differs from the fixture key they read: "card_id" is
# renamed, the preview trio is nested under fixture["preview"].
CARD_ALIASES: dict[str, AliasPath] = {
    "card_id": "id",
    "previewed_at": ("preview", "previewed_at"),
    "preview_source_uri": ("preview", "source_uri"),
    "preview_source": ("preview", "source"),
}

# Card accessors the passthrough sweep cannot assert, each mapped to the pytest
# node id of the test that owns its coverage. all_parts and card_faces return
# wrapper objects rather than the raw dicts (the card_face and related_card specs
# sweep the unwrapped items, so the wrapping itself is owned by a test apiece at
# the foot of this module); the is_* predicates are computed from type_line and
# have no fixture key at all.
CARD_COVERED_ELSEWHERE: dict[str, str] = {
    "all_parts": "tests/sweep/test_property_sweep.py::test_all_parts_wraps_every_raw_part",
    "card_faces": "tests/sweep/test_property_sweep.py::test_card_faces_wraps_every_raw_face",
    "is_creature": "tests/usage/test_predicates.py::test_named__is_creature__returns_true",
    "is_instant": "tests/usage/test_predicates.py::test_named__is_instant__returns_true",
    "is_sorcery": "tests/usage/test_predicates.py::test_named__is_sorcery__returns_true",
    "is_enchantment": "tests/usage/test_predicates.py::test_named__is_enchantment__returns_true",
    "is_artifact": "tests/usage/test_predicates.py::test_named__is_artifact__returns_true",
    "is_planeswalker": "tests/usage/test_predicates.py::test_named__is_planeswalker__returns_true",
}

CARD_WRAPPERS: dict[str, tuple[str, ...]] = {
    "preview": ("previewed_at", "preview_source_uri", "preview_source"),
}

# Sets, bulk data, list and catalog envelopes have no renamed or nested
# accessors, so they need no aliases. Their `object` accessor is a hardcoded
# literal rather than a dict read; the passthrough sweep is still meaningful
# there because it pins that literal to the value Scryfall returns.
SWEEP_SPECS: tuple[SweepSpec, ...] = (
    SweepSpec(
        name="card",
        cls=Object,
        build=Object.from_dict,
        corpus=CARD_CORPUS,
        aliases=CARD_ALIASES,
        covered_elsewhere=CARD_COVERED_ELSEWHERE,
        wrappers=CARD_WRAPPERS,
    ),
    SweepSpec(name="set", cls=SetsObject, build=SetsObject, corpus=SET_CORPUS),
    SweepSpec(name="bulk_data", cls=BulkDataObject, build=BulkDataObject, corpus=BULK_DATA_CORPUS),
    SweepSpec(name="list", cls=_BareList, build=_BareList, corpus=LIST_CORPUS),
    SweepSpec(name="catalog", cls=_BareCatalog, build=_BareCatalog, corpus=CATALOG_CORPUS),
    SweepSpec(
        name="card_face",
        cls=CardFaceMixin,
        build=_BareCardFace,
        corpus=CARD_FACE_CORPUS,
    ),
    SweepSpec(
        name="related_card",
        cls=RelatedCardsObjectMixin,
        build=_BareRelatedCard,
        corpus=RELATED_CARD_CORPUS,
    ),
)

# ─────────────────────────────────────────────────────────────────────────────

_SPECS_BY_NAME: dict[str, SweepSpec] = {spec.name: spec for spec in SWEEP_SPECS}


# ─── Parametrize lists ────────────────────────────────────────────────────────

# One case per accessor (or per fixture key), not per accessor × fixture. The
# swept accessors are plain dict reads with no data-dependent branch, and
# `reaches()` does not look at the fixture at all, so running either against a
# second fixture re-executes the same line and proves nothing further. The
# corpus stays broad because *which keys exist* differs per fixture — that is
# what feeds the reverse guard — but each key only needs asserting once.


def _witness_fixtures(spec: SweepSpec) -> dict[str, str]:
    """Map each top-level corpus key to the fixture that best witnesses it.

    Prefers a fixture whose value for the key is non-null: a null value makes the
    passthrough assertion vacuous (None == None) and so proves nothing about the
    accessor. Falls back to the first fixture carrying the key at all, so a key
    that is null everywhere is still swept and still reaches the reverse guard.
    """
    non_null: dict[str, str] = {}
    present: dict[str, str] = {}
    for fixture_name, fixture in spec.corpus.items():
        for key, value in fixture.items():
            present.setdefault(key, fixture_name)
            if value is not None:
                non_null.setdefault(key, fixture_name)
    return {key: non_null.get(key, fixture_name) for key, fixture_name in present.items()}


def _alias_witness_fixture(spec: SweepSpec, path: AliasPath) -> str | None:
    """Return the fixture that best witnesses an alias, or None if none reaches it.

    Same preference as `_witness_fixtures`, applied to the resolved value rather
    than a top-level key, so a nested alias lands on a fixture that actually
    carries the child key.
    """
    fallback: str | None = None
    for fixture_name, fixture in spec.corpus.items():
        if not _alias_reachable(fixture, path):
            continue
        if _resolve_alias(fixture, path) is not None:
            return fixture_name
        fallback = fallback or fixture_name
    return fallback


_WITNESSES: dict[str, dict[str, str]] = {spec.name: _witness_fixtures(spec) for spec in SWEEP_SPECS}

_PASSTHROUGH_PARAMS = [
    pytest.param(spec.name, _WITNESSES[spec.name][prop], prop, id=f"{spec.name}-{prop}")
    for spec in SWEEP_SPECS
    for prop in sorted(spec.properties)
    if prop not in spec.exceptions and prop in _WITNESSES[spec.name]
]

_EXCEPTION_PARAMS = [
    pytest.param(spec.name, fixture_name, prop, id=f"{spec.name}-{prop}")
    for spec in SWEEP_SPECS
    for prop, alias in spec.aliases.items()
    if (fixture_name := _alias_witness_fixture(spec, alias)) is not None
]

_REVERSE_PARAMS = [
    pytest.param(spec.name, fixture_name, key, id=f"{spec.name}-key:{key}")
    for spec in SWEEP_SPECS
    for key, fixture_name in sorted(_WITNESSES[spec.name].items())
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


# ─── Wrapped card sub-object accessors ────────────────────────────────────────

# card_faces and all_parts wrap their raw items, so the passthrough sweep skips
# them and the card_face/related_card specs sweep the unwrapped items instead.
# That leaves the wrapping itself unasserted, which is what these two tests own.

_WRAPPING_FIXTURE = CARD_CORPUS["transform"]


def test_card_faces_wraps_every_raw_face() -> None:
    """Card.card_faces builds one CardFaceMixin per raw face, in fixture order."""
    faces = Object.from_dict(_WRAPPING_FIXTURE).card_faces
    assert (
        faces is not None
    ), "fixture 'transform' must carry card_faces for this test to mean anything"

    assert all(isinstance(face, CardFaceMixin) for face in faces)
    assert [face.name for face in faces] == [raw["name"] for raw in _WRAPPING_FIXTURE["card_faces"]]


def test_all_parts_wraps_every_raw_part() -> None:
    """Card.all_parts builds one RelatedCardsObjectMixin per raw part, in fixture order."""
    parts = Object.from_dict(_WRAPPING_FIXTURE).all_parts
    assert (
        parts is not None
    ), "fixture 'transform' must carry all_parts for this test to mean anything"

    assert all(isinstance(part, RelatedCardsObjectMixin) for part in parts)
    assert [part.id for part in parts] == [raw["id"] for raw in _WRAPPING_FIXTURE["all_parts"]]
