from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, ClassVar


class Connector(ABC):
    # Connector resolution state lives on the type: a per-context override set
    # by use(), and a process-wide default set by set_default().
    _connector_var: ClassVar[ContextVar["Connector | None"]] = ContextVar(
        "scrython_connector", default=None
    )
    _default: ClassVar["Connector | None"] = None

    @abstractmethod
    def fetch(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a Scryfall-shaped response dict, including error dicts."""

    @classmethod
    def set_default(cls, connector: "Connector | None") -> None:
        """Set the process-wide default connector (lowest precedence after builtin)."""
        cls._default = connector

    @classmethod
    @contextmanager
    def use(cls, connector: "Connector") -> Generator[None, None, None]:
        """Scope a connector to the current context (overrides the default)."""
        token = cls._connector_var.set(connector)
        try:
            yield
        finally:
            cls._connector_var.reset(token)

    @classmethod
    def current(cls) -> "Connector":
        """Resolve the active connector: use() scope, then default, then builtin."""
        ctx = cls._connector_var.get()
        if ctx is not None:
            return ctx
        if cls._default is not None:
            return cls._default
        from .connectors.scryfall_api import ScryfallConnector

        return ScryfallConnector()


# Module-level aliases keep the documented `scrython.set_default_connector(...)`
# call site working while the implementation lives on Connector.
set_default_connector = Connector.set_default
use_connector = Connector.use
get_connector = Connector.current
