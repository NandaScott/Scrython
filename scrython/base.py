import json
import types
import urllib.error
import urllib.parse
from typing import Any
from urllib.request import Request, urlopen


class ScryfallError(Exception):
    def __init__(self, scryfall_data: dict[str, Any], *args: Any, **kwargs: Any) -> None:
        super(self.__class__, self).__init__(*args, **kwargs)

        self._status: int = scryfall_data["status"]
        self._code: str = scryfall_data["code"]
        self._details: str = scryfall_data["details"]
        self._type: str | None = scryfall_data["type"]
        self._warnings: list[str] | None = scryfall_data["warnings"]

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

    This class handles HTTP communication with the Scryfall API including
    path building, query parameter encoding, and error handling.

    API Requirements:
        - User-Agent header is required (default: 'Scrython/2.0')
        - Accept header is required (default: 'application/json')
        - HTTPS with TLS 1.2+ is required
    """

    _scryfall_data: dict[str, Any] = {}
    _user_agent: str = "Scrython/2.0 (https://github.com/NandaScott/Scrython)"
    _accept: str = "application/json"
    _content_type: str = "application/json"
    _endpoint: str = ""

    @classmethod
    def set_user_agent(cls, user_agent: str) -> None:
        """
        Set a custom User-Agent header for all Scrython requests.

        Scryfall recommends identifying your application in the User-Agent.

        Args:
            user_agent: Custom User-Agent string

        Example:
            scrython.set_user_agent('MyMTGApp/1.0 (contact@example.com)')
        """
        cls._user_agent = user_agent

    @property
    def scryfall_data(self) -> types.SimpleNamespace:
        """
        Read-only access to Scryfall API response data.

        Returns a SimpleNamespace object allowing dot-notation access to all
        fields returned by the Scryfall API. This is a read-only view -
        modifications will not affect the internal data.

        Example:
            card = scrython.cards.Named(exact='Black Lotus')
            print(card.scryfall_data.name)  # 'Black Lotus'
            print(card.scryfall_data.mana_cost)  # '{0}'

        Returns:
            SimpleNamespace object with API response data
        """
        if not hasattr(self, "_scryfall_namespace"):
            self._scryfall_namespace = self._dict_to_namespace(self._scryfall_data)
        return self._scryfall_namespace

    def _dict_to_namespace(self, data: Any) -> Any:
        """
        Recursively convert dict to SimpleNamespace for nested objects.

        Args:
            data: The data to convert (dict, list, or other)

        Returns:
            SimpleNamespace for dicts, list of converted items for lists, or original data
        """
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
        self._build_path(**kwargs)
        self._build_params(**kwargs)
        self._fetch(**kwargs)

        if self._scryfall_data["object"] == "error":
            raise ScryfallError(self._scryfall_data, self._scryfall_data["details"])

    def _fetch(self, **kwargs: Any) -> None:
        data: bytes | None = None
        if data_param := kwargs.get("data"):
            data = json.dumps(data_param).encode("utf-8")

        request = Request(
            f"https://api.scryfall.com/{self.endpoint}?{self._encoded_query_params}", data=data
        )
        request.add_header("User-Agent", self._user_agent)
        request.add_header("Accept", self._accept)
        request.add_header("Content-Type", self._content_type)

        try:
            with urlopen(request) as response:
                charset = response.info().get_param("charset") or "utf-8"
                decoded = response.read().decode(charset)

                self._scryfall_data = json.loads(decoded)
                # Invalidate namespace cache when new data is fetched
                if hasattr(self, "_scryfall_namespace"):
                    delattr(self, "_scryfall_namespace")
        except urllib.error.HTTPError as exc:
            raise Exception(f"{exc}: {request.get_full_url()}") from exc

    def _build_params(self, **kwargs: Any) -> None:
        self._query_params: dict[str, Any] = {
            "format": kwargs.get("format", "json"),
            "face": kwargs.get("face", ""),
            "version": kwargs.get("version", ""),
            "pretty": kwargs.get("pretty", ""),
            **kwargs,
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

            if value is not None and not optional:
                resolved.append(str(value))

        self._endpoint = "/".join(resolved)
