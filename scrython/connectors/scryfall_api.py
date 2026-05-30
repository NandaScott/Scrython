import json
import urllib.error
import urllib.parse
from typing import Any
from urllib.request import Request, urlopen

from ..connector import Connector
from ..rate_limiter import RateLimiter


class ScryfallConnector(Connector):
    """
    Default HTTP connector for the Scryfall API.

    Handles urllib, User-Agent/Accept/Content-Type headers, and rate limiting.
    Inject a custom instance via the connector= kwarg or set_default_connector()
    to control rate limiting or headers on a per-use basis.
    """

    _user_agent: str = "Scrython/2.0 (https://github.com/NandaScott/Scrython)"
    _accept: str = "application/json"
    _content_type: str = "application/json"
    _BASE_URL: str = "https://api.scryfall.com"

    def __init__(self, rate_limiter: RateLimiter | None = None) -> None:
        self._rate_limiter = rate_limiter if rate_limiter is not None else RateLimiter.get_global_limiter()

    @classmethod
    def set_user_agent(cls, user_agent: str) -> None:
        """
        Set a custom User-Agent header for all Scrython requests.

        Scryfall recommends identifying your application in the User-Agent.

        Args:
            user_agent: Custom User-Agent string

        Example:
            ScryfallConnector.set_user_agent('MyMTGApp/1.0 (contact@example.com)')
        """
        cls._user_agent = user_agent

    def fetch(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a Scryfall-shaped response dict, including error dicts."""
        url = f"{self._BASE_URL}/{endpoint}?{urllib.parse.urlencode(params)}"
        return self._fetch_url(url, data=data)

    def _fetch_url(
        self,
        url: str,
        *,
        data: dict[str, Any] | None = None,
        rate_limit: bool = True,
    ) -> dict[str, Any]:
        if rate_limit:
            self._rate_limiter.wait()

        post_data: bytes | None = None
        if data is not None:
            post_data = json.dumps(data).encode("utf-8")

        request = Request(url, data=post_data)
        request.add_header("User-Agent", self._user_agent)
        request.add_header("Accept", self._accept)
        request.add_header("Content-Type", self._content_type)

        try:
            with urlopen(request) as response:
                charset = response.info().get_param("charset") or "utf-8"
                return json.loads(response.read().decode(charset))
        except urllib.error.HTTPError as exc:
            try:
                charset = exc.headers.get_param("charset")
                if not isinstance(charset, str):
                    charset = "utf-8"
                error_data: dict[str, Any] = json.loads(exc.read().decode(charset))
            except (json.JSONDecodeError, UnicodeDecodeError):
                raise Exception(f"{exc}: {request.get_full_url()}") from exc

            if error_data.get("object") == "error":
                return error_data

            raise Exception(f"{exc}: {request.get_full_url()}") from exc
