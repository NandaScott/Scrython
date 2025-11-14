import json
import types
import urllib.error
import urllib.parse
from typing import Any
from urllib.request import Request, urlopen

from .cache import generate_cache_key, get_global_cache
from .rate_limiter import RateLimiter


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
        # Caching (disabled by default)
        use_cache = kwargs.get("cache", False)
        cache_ttl = kwargs.get("cache_ttl", 3600)  # Default 1 hour

        # Check cache first if enabled
        if use_cache:
            cache = get_global_cache()
            cache_key = generate_cache_key(self.endpoint, self._query_params)
            cached_data = cache.get(cache_key)

            if cached_data is not None:
                # Cache hit - use cached data
                self._scryfall_data = cached_data
                # Invalidate namespace cache
                if hasattr(self, "_scryfall_namespace"):
                    delattr(self, "_scryfall_namespace")
                return

        # Rate limiting (enabled by default)
        rate_limit = kwargs.get("rate_limit", True)

        if rate_limit:
            # Get rate limit setting
            rate_limit_per_second = kwargs.get("rate_limit_per_second", 10.0)

            # Get or create global rate limiter
            limiter = RateLimiter.get_global_limiter(rate_limit_per_second)

            # Wait if necessary to respect rate limit
            limiter.wait()

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

                # Store in cache if enabled and not an error
                if use_cache and self._scryfall_data.get("object") != "error":
                    cache = get_global_cache()
                    cache_key = generate_cache_key(self.endpoint, self._query_params)
                    cache.set(cache_key, self._scryfall_data, cache_ttl)

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

    def __repr__(self) -> str:
        """
        Developer-friendly representation showing class name and key identifiers.

        Returns a string in the format: ClassName(id='...', key_field='...')

        Example:
            Named(id='bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd', name='Lightning Bolt')
        """
        class_name = self.__class__.__name__

        # Try to get the ID field (common for most objects)
        obj_id = self._scryfall_data.get("id")

        # Try to get a meaningful identifier (name, code, etc.)
        name = self._scryfall_data.get("name")
        code = self._scryfall_data.get("code")

        parts = [f"id='{obj_id}'"] if obj_id else []

        if name:
            parts.append(f"name='{name}'")
        elif code:
            parts.append(f"code='{code}'")

        return f"{class_name}({', '.join(parts)})"

    def __str__(self) -> str:
        """
        User-friendly string representation.

        For cards: Returns "Card Name (SET)" format
        For sets: Returns "Set Name (CODE)" format
        For other objects: Returns the name or a basic representation

        Example:
            "Lightning Bolt (LEA)"
            "Limited Edition Alpha (LEA)"
        """
        obj_type = self._scryfall_data.get("object", "")
        name = self._scryfall_data.get("name", "")

        if obj_type == "card":
            set_code = self._scryfall_data.get("set", "").upper()
            return f"{name} ({set_code})" if set_code else name
        elif obj_type == "set":
            code = self._scryfall_data.get("code", "").upper()
            return f"{name} ({code})" if code else name
        elif obj_type == "list":
            # For list objects, show summary
            total = self._scryfall_data.get("total_cards", 0)
            return f"List with {total} items"
        elif obj_type == "catalog":
            # For catalog objects, show summary
            data = self._scryfall_data.get("data", [])
            return f"Catalog with {len(data)} items"
        else:
            # Fallback to name or class name
            return name if name else f"{self.__class__.__name__} object"

    def __eq__(self, other: object) -> bool:
        """
        Compare objects by their Scryfall ID.

        Two objects are considered equal if:
        1. They are both ScrythonRequestHandler instances
        2. They have the same Scryfall ID

        Args:
            other: Another object to compare with

        Returns:
            True if objects have the same Scryfall ID, False otherwise

        Example:
            card1 = scrython.cards.Named(fuzzy='Lightning Bolt')
            card2 = scrython.cards.Named(exact='Lightning Bolt')
            card1 == card2  # True (same card, same ID)
        """
        if not isinstance(other, ScrythonRequestHandler):
            return False

        # Compare by ID if both objects have one
        self_id = self._scryfall_data.get("id")
        other_id = other._scryfall_data.get("id")

        if self_id and other_id:
            return self_id == other_id

        # Fallback to object comparison if no IDs
        return self is other

    def __hash__(self) -> int:
        """
        Generate hash based on Scryfall ID to enable use in sets and dicts.

        Returns:
            Hash of the Scryfall ID, or hash of class name if no ID available

        Example:
            unique_cards = {card1, card2, card3}
            card_lookup = {card1: 'owned', card2: 'wanted'}
        """
        obj_id = self._scryfall_data.get("id")
        if obj_id:
            return hash(obj_id)

        # Fallback to instance hash if no ID
        # Note: This makes objects without IDs unhashable across instances
        return hash(id(self))

    def to_dict(self) -> dict[str, Any]:
        """
        Export object data as a dictionary.

        Returns a copy of the internal Scryfall data dictionary. Modifications
        to the returned dict will not affect the object's internal state.

        Returns:
            Dictionary containing all Scryfall API response data

        Example:
            card = scrython.cards.Named(fuzzy='Lightning Bolt')
            card_dict = card.to_dict()
            print(card_dict['name'])  # 'Lightning Bolt'
        """
        return self._scryfall_data.copy()

    def to_json(self, **kwargs: Any) -> str:
        """
        Export object data as a JSON string.

        Args:
            **kwargs: Additional arguments passed to json.dumps()
                     Common options: indent, sort_keys, ensure_ascii

        Returns:
            JSON string representation of the object data

        Example:
            card = scrython.cards.Named(fuzzy='Lightning Bolt')

            # Compact JSON
            json_str = card.to_json()

            # Pretty-printed JSON
            json_str = card.to_json(indent=2, sort_keys=True)

            # Save to file
            with open('card.json', 'w') as f:
                f.write(card.to_json(indent=2))
        """
        return json.dumps(self._scryfall_data, **kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScrythonRequestHandler":
        """
        Construct an object from a dictionary without making an API request.

        This is useful for rehydrating cached objects or constructing objects
        from saved data. The object is created without making any HTTP requests.

        Args:
            data: Dictionary containing Scryfall API response data

        Returns:
            Instance of the class populated with the provided data

        Example:
            # Save card data
            card = scrython.cards.Named(fuzzy='Lightning Bolt')
            card_dict = card.to_dict()

            # Later, restore from dict (no API call)
            restored_card = scrython.cards.Named.from_dict(card_dict)
            print(restored_card.name)  # 'Lightning Bolt'
        """
        # Create instance without calling __init__
        instance = cls.__new__(cls)
        instance._scryfall_data = data.copy()
        return instance
