"""Self-tests for the property sweep engine.

The sweep in test_property_sweep.py is data-driven: its guarantees live in
SweepSpec and in the parametrize lists built from the specs. These tests pin
those guarantees directly — a synthetic spec exercises the reverse guard and
the alias resolver in isolation, and the real card spec pins the split between
the passthrough sweep and the exception sweep.
"""

from importlib import import_module
from typing import Any, cast

import pytest

from tests.sweep.test_property_sweep import (
    _EXCEPTION_PARAMS,
    _PASSTHROUGH_PARAMS,
    _SPECS_BY_NAME,
    SWEEP_SPECS,
    SweepSpec,
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


def _referenced_names(func: Any) -> frozenset[str]:
    """Names a function's own body reads, as attributes, globals, or string literals.

    Read off the code object rather than the source text, so a test that merely
    carries an accessor's name in its own function name does not count as
    referencing it.
    """
    code = func.__code__
    literals = {const for const in code.co_consts if isinstance(const, str)}
    return frozenset(set(code.co_names) | literals)


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


@pytest.mark.parametrize("spec_name,accessor,node_id", _COVERAGE_REFERENCE_PARAMS)
def test_covered_elsewhere_owner_reads_the_accessor(
    spec_name: str, accessor: str, node_id: str
) -> None:
    """Each covered_elsewhere owner must actually read the accessor it claims.

    Resolving to a callable is not coverage. Without this, an entry can name any
    test at all — including one of the engine's own parametrized sweeps, which
    reads accessors through getattr and so covers no accessor in particular.
    """
    owning_test = _resolve_node_id(node_id)

    assert accessor in _referenced_names(owning_test), (
        f"{spec_name} accessor '{accessor}' names owning test '{node_id}', "
        f"whose body never reads '{accessor}' — point the entry at a test that "
        f"asserts this accessor, or write one"
    )


# ─── Hard-fail completeness guard ─────────────────────────────────────────────

_COMPLETENESS_PARAMS = [
    pytest.param(spec.name, accessor, id=f"{spec.name}-{accessor}")
    for spec in SWEEP_SPECS
    for accessor in sorted(spec.properties)
]

# Read off the sweep's own parametrize lists rather than re-deriving which
# accessors they reach, so an accessor that drops out of both sweeps cannot stay
# green here through a second copy of the selection logic drifting out of step.
_SWEPT_ACCESSORS: frozenset[tuple[str, str]] = frozenset(
    cast("tuple[str, str]", (param.values[0], param.values[2]))
    for param in _PASSTHROUGH_PARAMS + _EXCEPTION_PARAMS
)


@pytest.mark.parametrize("spec_name,accessor", _COMPLETENESS_PARAMS)
def test_every_accessor_is_asserted(spec_name: str, accessor: str) -> None:
    """Every accessor must be value-asserted by passthrough, exception, or covered_elsewhere.

    Fails when an accessor is reached by neither sweep and has no covered_elsewhere
    entry. Deleting the fixture that carries a field turns this test red, as does
    dropping an alias for a renamed or nested field.
    """
    spec = _SPECS_BY_NAME[spec_name]

    if accessor in spec.covered_elsewhere:
        return

    assert (spec_name, accessor) in _SWEPT_ACCESSORS, (
        f"{spec_name} accessor '{accessor}' is asserted by neither sweep — "
        "add a fixture carrying its field, add an alias if the fixture key is "
        "renamed or nested, or declare covered_elsewhere naming the owning test"
    )
