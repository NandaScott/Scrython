"""Self-tests for the property sweep engine.

The sweep in test_property_sweep.py is data-driven: its guarantees live in
SweepSpec and in the parametrize lists built from the specs. These tests pin
those guarantees directly — a synthetic spec exercises the reverse guard and
the alias resolver in isolation, and the real card spec pins the split between
the passthrough sweep and the exception sweep.
"""

from importlib import import_module
from typing import Any

import pytest

from tests.sweep.test_property_sweep import (
    _EXCEPTION_PARAMS,
    _PASSTHROUGH_PARAMS,
    _SPECS_BY_NAME,
    SWEEP_SPECS,
    SweepSpec,
    _alias_reachable,
    _resolve_alias,
    _run_passthrough_check,
)


def _resolve_node_id(node_id: str) -> Any:
    """Resolve a 'path/to/test_file.py::Class::func' node id to the object it names."""
    module_path, *attribute_names = node_id.split("::")
    target: Any = import_module(module_path.removesuffix(".py").replace("/", "."))
    for attribute_name in attribute_names:
        target = getattr(target, attribute_name)
    return target


_COVERAGE_REFERENCE_PARAMS = [
    pytest.param(spec.name, accessor, node_id, id=f"{spec.name}-{accessor}")
    for spec in SWEEP_SPECS
    for accessor, node_id in spec.covered_elsewhere.items()
]


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


@pytest.mark.parametrize("spec", SWEEP_SPECS, ids=lambda spec: spec.name)
def test_every_exception_declares_coverage(spec: SweepSpec) -> None:
    """Every exception-set accessor is either aliased or declared covered elsewhere."""
    undeclared = spec.exceptions - frozenset(spec.aliases) - frozenset(spec.covered_elsewhere)

    assert not undeclared, (
        f"{spec.name} exceptions with no coverage declaration: {sorted(undeclared)}. "
        "Add each to the spec's aliases (if renamed or nested) or to its "
        "covered_elsewhere (naming the pytest node id of the owning test)."
    )


@pytest.mark.parametrize("spec_name,accessor,node_id", _COVERAGE_REFERENCE_PARAMS)
def test_covered_elsewhere_reference_resolves(spec_name: str, accessor: str, node_id: str) -> None:
    """Each covered_elsewhere node id resolves to a test that still exists."""
    try:
        owning_test = _resolve_node_id(node_id)
    except (ImportError, AttributeError) as error:
        pytest.fail(
            f"{spec_name} accessor '{accessor}' names owning test '{node_id}', "
            f"which does not resolve: {error}"
        )

    assert callable(owning_test), f"'{node_id}' resolves to {owning_test!r}, not a test function"


# ─── Hard-fail completeness guard ─────────────────────────────────────────────

_COMPLETENESS_PARAMS = [
    pytest.param(spec.name, accessor, id=f"{spec.name}-{accessor}")
    for spec in SWEEP_SPECS
    for accessor in sorted(spec.properties)
]


@pytest.mark.parametrize("spec_name,accessor", _COMPLETENESS_PARAMS)
def test_every_accessor_is_asserted(spec_name: str, accessor: str) -> None:
    """Every accessor must be value-asserted by passthrough, exception, or covered_elsewhere.

    Fails when an accessor is present on the class but its key never appears in
    any fixture AND it has no alias AND it has no covered_elsewhere entry. Deleting
    a fixture or removing an assertion turns this test red.
    """
    spec = _SPECS_BY_NAME[spec_name]

    if accessor in spec.covered_elsewhere:
        return

    if accessor in spec.exceptions:
        if accessor in spec.aliases:
            alias = spec.aliases[accessor]
            asserted = any(_alias_reachable(fixture, alias) for fixture in spec.corpus.values())
            assert asserted, (
                f"{spec_name} accessor '{accessor}' is aliased to {alias!r} "
                "but that target appears in no fixture — "
                "add a fixture that exposes it or declare covered_elsewhere"
            )
        else:
            pytest.fail(
                f"{spec_name} accessor '{accessor}' is an exception with no alias "
                "and no covered_elsewhere entry"
            )
        return

    asserted = any(accessor in fixture for fixture in spec.corpus.values())
    assert asserted, (
        f"{spec_name} accessor '{accessor}' appears in no fixture — "
        "add a fixture that exposes this field or declare it covered_elsewhere"
    )
