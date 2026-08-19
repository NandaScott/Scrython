"""Self-tests for the property sweep engine.

The sweep in test_property_sweep.py is data-driven: its guarantees live in
SweepSpec and in the parametrize lists built from the specs. These tests pin
those guarantees directly — a synthetic spec exercises the reverse guard and
the alias resolver in isolation, and the real card spec pins the split between
the passthrough sweep and the exception sweep.
"""

from typing import Any

import pytest

from tests.sweep.test_property_sweep import (
    _EXCEPTION_PARAMS,
    _PASSTHROUGH_PARAMS,
    _SPECS_BY_NAME,
    CARD_ALIASES,
    CARD_COVERED_ELSEWHERE,
    CARD_EXCEPTIONS,
    SweepSpec,
    _resolve_alias,
    _run_passthrough_check,
)


class _SynthObject:
    """Minimal accessor surface: one passthrough, one renamed, one nested."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def name(self) -> Any:
        return self._data["name"]

    @property
    def synth_id(self) -> Any:
        return self._data["id"]

    @property
    def previewed_at(self) -> Any:
        return self._data["preview"]["previewed_at"]


SYNTH_FIXTURE: dict[str, Any] = {
    "name": "Llanowar Elves",
    "id": "11111111-2222-3333-4444-555555555555",
    "preview": {"previewed_at": "2026-01-01"},
}

SYNTH_SPEC = SweepSpec(
    name="synth",
    cls=_SynthObject,
    build=_SynthObject,
    corpus={"synth": SYNTH_FIXTURE},
    exceptions=frozenset({"synth_id", "previewed_at"}),
    aliases={"synth_id": "id", "previewed_at": ("preview", "previewed_at")},
    wrappers={"preview": ("previewed_at",)},
)


def test_reverse_guard_flags_unexposed_key() -> None:
    """A fixture key with no accessor, alias, or wrapper entry is unreachable."""
    assert not SYNTH_SPEC.reaches("__synth_unexposed__")


def test_reverse_guard_accepts_alias_target() -> None:
    """A key reachable only under a renamed accessor counts as covered."""
    assert SYNTH_SPEC.reaches("id")


def test_reverse_guard_accepts_wrapper_parent_key() -> None:
    """A parent key whose children are read by named accessors counts as covered."""
    assert SYNTH_SPEC.reaches("preview")


def test_reverse_guard_rejects_stale_wrapper_entry() -> None:
    """A wrapper entry naming an accessor that no longer exists stops covering its key."""
    stale_spec = SweepSpec(
        name="synth-stale",
        cls=_SynthObject,
        build=_SynthObject,
        corpus={"synth": SYNTH_FIXTURE},
        wrappers={"preview": ("renamed_away",)},
    )

    assert not stale_spec.reaches("preview")


def test_alias_resolves_nested_path() -> None:
    """A (parent, child) alias resolves to the same value its accessor returns."""
    obj = SYNTH_SPEC.build(SYNTH_FIXTURE)

    resolved = _resolve_alias(SYNTH_FIXTURE, SYNTH_SPEC.aliases["previewed_at"])
    assert obj.previewed_at == resolved == "2026-01-01"


def test_exception_accessors_excluded_from_passthrough_sweep() -> None:
    """No accessor in a spec's exception set is swept as a passthrough."""
    card_spec = _SPECS_BY_NAME["card"]
    swept = {param.values[2] for param in _PASSTHROUGH_PARAMS if param.values[0] == "card"}

    assert not swept & card_spec.exceptions


def test_aliased_accessors_covered_by_exception_sweep() -> None:
    """A renamed accessor is asserted by the exception sweep instead."""
    swept = {param.values[2] for param in _EXCEPTION_PARAMS if param.values[0] == "card"}

    assert "card_id" in swept


def test_wrong_valued_passthrough_fails() -> None:
    """The passthrough assertion fires when an accessor returns the wrong value."""

    class _BrokenSynthObject:
        """Accessor that ignores fixture data and always returns a hardcoded value."""

        def __init__(self, data: dict[str, Any]) -> None:
            self._data = data

        @property
        def name(self) -> str:
            return "Hardcoded Wrong Value"

    broken_spec = SweepSpec(
        name="synth-broken",
        cls=_BrokenSynthObject,
        build=_BrokenSynthObject,
        corpus={"synth": SYNTH_FIXTURE},
    )

    with pytest.raises(AssertionError):
        _run_passthrough_check(broken_spec, "synth", "name")


def test_all_card_exceptions_covered() -> None:
    """Every card exception must appear in CARD_ALIASES or CARD_COVERED_ELSEWHERE."""
    uncovered = CARD_EXCEPTIONS - frozenset(CARD_ALIASES) - frozenset(CARD_COVERED_ELSEWHERE)
    assert not uncovered, (
        f"Card exceptions with no coverage declaration: {sorted(uncovered)}. "
        "Add each to CARD_ALIASES (if renamed/nested) or CARD_COVERED_ELSEWHERE "
        "(if tested by another test or issue)."
    )
