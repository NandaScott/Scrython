import json
import types
import urllib.parse
import warnings
from typing import Any

from .cache import generate_cache_key, get_global_cache
from .connector import Connector

_HANDLER_KWARGS: frozenset[str] = frozenset(
    {"rate_limit", "cache", "cache_ttl", "data", "connector"}
)


class ScryfallError(Exception):
    def __init__(self, scryfall_data: dict[str, Any], *args: Any, **kwargs: Any) -> None:
        super(self.__class__, self).__init__(*args, **kwargs)

        self._status: int = scryfall_data["status"]
        self._code: str = scryfall_data["code"]
        self._details: str = scryfall_data["details"]
        self._type: str | None = scryfall_data.get("type")
        self._warnings: list[str] | None = scryfall_data.get("warnings")

    @property
    def status(self) -> int:
        return self._status

    @property
    def code(self) -> str:
        return self._code

    @property
    def details(self) -> str:
        return self._details

    @property
    def type(self) -> str | None:
        return self._type

    @property
    def warnings(self) -> list[str] | None:
        return self._warnings


class ScrythonRequestHandler:
    """
    Base class for all Scryfall API requests.

    Builds endpoint paths and query parameters, then delegates HTTP execution
    to a Connector. The resolved connector is chosen by: per-request connector=
    kwarg, then use_connector() scope, then set_default_connector(), then the
    built-in ScryfallConnector default.
    """

    _scryfall_data: dict[str, Any] = {}
    _endpoint: str = ""

    @property
    def scryfall_data(self) -> types.SimpleNamespace:
        """
        Read-only access to Scryfall API response data as dot-notation namespace.

        Returns:
            SimpleNamespace object with API response data
        """
        if not hasattr(self, "_scryfall_namespace"):
            self._scryfall_namespace = self._dict_to_namespace(self._scryfall_data)
        return self._scryfall_namespace

    def _dict_to_namespace(self, data: Any) -> Any:
        if isinstance(data, dict):
            return types.SimpleNamespace(**{k: self._dict_to_namespace(v) for k, v in data.items()})
        elif isinstance(data, list):
            return [self._dict_to_namespace(item) for item in data]
        else:
            return data

    @property
    def endpoint(self) -> str:
        return self._endpoint

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a Scryfall API request handler.

        Args:
            **kwargs: Endpoint-specific parameters, plus optional:
                - connector (Connector): Override the connector for this request
                - cache (bool): Enable caching (default: False)
                - cache_ttl (int): Cache TTL in seconds (default: 3600)
        """
        self._warn_removed_kwargs(kwargs)
        self._build_path(**kwargs)
        self._build_params(**kwargs)
        self._fetch(**kwargs)

        if self._scryfall_data["object"] == "error":
            raise ScryfallError(self._scryfall_data, self._scryfall_data["details"])

    def _warn_removed_kwargs(self, kwargs: dict[str, Any]) -> None:
        if "rate_limit" in kwargs:
            warnings.warn(
                "rate_limit= is removed and has no effect; configure throttling on "
                "the connector instead, e.g. "
                "ScryfallConnector(rate_limiter=NullRateLimiter()).",
                DeprecationWarning,
                stacklevel=3,
            )

    def _get_connector(self, **kwargs: Any) -> Connector:
        connector: Connector | None = kwargs.get("connector")
        if connector is not None:
            return connector
        return Connector.current()

    def _fetch_raw(self, url: str, cache_key: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """
        Low-level fetch for absolute URLs (used by iter_all for pagination).

        Handles caching and delegates HTTP execution to the resolved connector.

        Args:
            url: Full absolute URL to fetch
            cache_key: Optional cache key (caching skipped if not provided)
            **kwargs: Optional parameters:
                - cache (bool): Enable caching (default: False)
                - cache_ttl (int): Cache TTL in seconds (default: 3600)
                - data (dict): POST body data (optional)
                - connector (Connector): Override the connector for this request

        Returns:
            dict: Parsed JSON response from Scryfall API

        Raises:
            Exception: On transport-level failures
        """
        use_cache = kwargs.get("cache", False)
        cache_ttl = kwargs.get("cache_ttl", 3600)

        if use_cache and cache_key is not None:
            cached_data = get_global_cache().get(cache_key)
            if cached_data is not None:
                return cached_data

        connector = self._get_connector(**kwargs)
        data_param: dict[str, Any] | None = kwargs.get("data")

        parsed = urllib.parse.urlparse(url)
        endpoint = parsed.path.lstrip("/")
        params: dict[str, Any] = dict(urllib.parse.parse_qsl(parsed.query))

        response_data = connector.fetch(endpoint, params, data=data_param)

        if use_cache and cache_key is not None and response_data.get("object") != "error":
            get_global_cache().set(cache_key, response_data, cache_ttl)

        return response_data

    def _fetch(self, **kwargs: Any) -> None:
        """
        Fetch data from Scryfall API using the endpoint template.

        Builds the full URL from self.endpoint and query parameters,
        then delegates to _fetch_raw() for caching and connector execution.

        Args:
            **kwargs: Optional parameters passed to _fetch_raw()
        """
        url = f"https://api.scryfall.com/{self.endpoint}?{self._encoded_query_params}"
        cache_key = generate_cache_key(self.endpoint, self._query_params)
        self._scryfall_data = self._fetch_raw(url, cache_key=cache_key, **kwargs)

        if hasattr(self, "_scryfall_namespace"):
            delattr(self, "_scryfall_namespace")

    def _build_params(self, **kwargs: Any) -> None:
        api_kwargs = {k: v for k, v in kwargs.items() if k not in _HANDLER_KWARGS}
        self._query_params: dict[str, Any] = {
            "format": api_kwargs.get("format", "json"),
            "face": api_kwargs.get("face", ""),
            "version": api_kwargs.get("version", ""),
            "pretty": api_kwargs.get("pretty", ""),
            **api_kwargs,
        }

        self._encoded_query_params: str = urllib.parse.urlencode(self._query_params)

    def _build_path(self, **kwargs: Any) -> None:
        parts = self.endpoint.strip("/").split("/")
        resolved: list[str] = []

        for part in parts:
            if not part.startswith(":"):
                resolved.append(part)
                continue

            key = part[1:]
            optional = key.endswith("?")

            if optional:
                key = key[:-1]

            value = kwargs.get(key)
            if value is None and not optional:
                raise KeyError(f"Missing required path parameter: '{key}'")

            if value is not None:
                resolved.append(str(value))

        self._endpoint = "/".join(resolved)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        obj_id = self._scryfall_data.get("id")
        name = self._scryfall_data.get("name")
        code = self._scryfall_data.get("code")

        parts = [f"id='{obj_id}'"] if obj_id else []

        if name:
            parts.append(f"name='{name}'")
        elif code:
            parts.append(f"code='{code}'")

        return f"{class_name}({', '.join(parts)})"

    def __str__(self) -> str:
        obj_type = self._scryfall_data.get("object", "")
        name = self._scryfall_data.get("name", "")

        if obj_type == "card":
            set_code = self._scryfall_data.get("set", "").upper()
            return f"{name} ({set_code})" if set_code else name
        elif obj_type == "set":
            code = self._scryfall_data.get("code", "").upper()
            return f"{name} ({code})" if code else name
        elif obj_type == "list":
            total = self._scryfall_data.get("total_cards", 0)
            return f"List with {total} items"
        elif obj_type == "catalog":
            data = self._scryfall_data.get("data", [])
            return f"Catalog with {len(data)} items"
        else:
            return name if name else f"{self.__class__.__name__} object"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScrythonRequestHandler):
            return False

        self_id = self._scryfall_data.get("id")
        other_id = other._scryfall_data.get("id")

        if self_id and other_id:
            return self_id == other_id

        return self is other

    def __hash__(self) -> int:
        obj_id = self._scryfall_data.get("id")
        if obj_id:
            return hash(obj_id)

        return hash(id(self))

    def to_dict(self) -> dict[str, Any]:
        return self._scryfall_data.copy()

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self._scryfall_data, **kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScrythonRequestHandler":
        instance = cls.__new__(cls)
        instance._scryfall_data = data.copy()
        return instance
