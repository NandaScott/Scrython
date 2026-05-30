from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

_connector_var: ContextVar["Connector | None"] = ContextVar("scrython_connector", default=None)
_default_connector: "Connector | None" = None


class Connector(ABC):
    @abstractmethod
    def fetch(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a Scryfall-shaped response dict, including error dicts."""


def set_default_connector(connector: "Connector | None") -> None:
    global _default_connector
    _default_connector = connector


@contextmanager
def use_connector(connector: "Connector") -> Generator[None, None, None]:
    token = _connector_var.set(connector)
    try:
        yield
    finally:
        _connector_var.reset(token)


def get_connector() -> "Connector":
    ctx = _connector_var.get()
    if ctx is not None:
        return ctx
    if _default_connector is not None:
        return _default_connector
    from .connectors.scryfall_api import ScryfallConnector

    return ScryfallConnector()
