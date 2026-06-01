"""Tests for connector resolution (issue #170 review).

Resolution lives on the Connector type as classmethods; module-level aliases
keep the documented scrython.set_default_connector(...) call site working.
"""

import pytest

import scrython
from scrython.connector import (
    Connector,
    get_connector,
    set_default_connector,
    use_connector,
)
from scrython.connectors.scryfall_api import ScryfallConnector


class DummyConnector(Connector):
    """A no-network connector that echoes its name into the response."""

    def __init__(self, name: str = "dummy") -> None:
        self.name = name

    def fetch(self, endpoint, params, *, data=None):
        return {"object": "card", "id": self.name, "name": self.name}


@pytest.fixture(autouse=True)
def reset_connector_default():
    Connector.set_default(None)
    yield
    Connector.set_default(None)


class TestConnectorResolution:
    def test_builtin_default_is_scryfall_connector(self):
        assert isinstance(Connector.current(), ScryfallConnector)

    def test_set_default_is_resolved(self):
        dummy = DummyConnector()
        Connector.set_default(dummy)
        assert Connector.current() is dummy

    def test_use_scope_overrides_default(self):
        default = DummyConnector("default")
        scoped = DummyConnector("scoped")
        Connector.set_default(default)
        with Connector.use(scoped):
            assert Connector.current() is scoped
        assert Connector.current() is default

    def test_per_request_kwarg_beats_scope_and_default(self):
        Connector.set_default(DummyConnector("default"))
        with Connector.use(DummyConnector("scoped")):
            card = scrython.cards.ById(id="x", connector=DummyConnector("kwarg"))
        assert card.to_dict()["id"] == "kwarg"


class TestModuleAliases:
    def test_aliases_point_at_classmethods(self):
        assert set_default_connector == Connector.set_default
        assert get_connector == Connector.current
        assert use_connector == Connector.use

    def test_alias_set_default_and_get(self):
        dummy = DummyConnector()
        set_default_connector(dummy)
        assert get_connector() is dummy

    def test_alias_use_scope(self):
        dummy = DummyConnector()
        with use_connector(dummy):
            assert get_connector() is dummy
        assert get_connector() is not dummy

    def test_scrython_namespace_call_site(self):
        dummy = DummyConnector()
        scrython.set_default_connector(dummy)
        assert scrython.get_connector() is dummy
