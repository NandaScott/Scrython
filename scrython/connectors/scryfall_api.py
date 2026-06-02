import json
import urllib.error
import urllib.parse
import warnings
from typing import Any
from urllib.request import Request, urlopen

from ..connector import Connector
from ..rate_limiter import NullRateLimiter, RateLimiter, RateLimitWarning, SlowRateLimiter


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

    # Scryfall throttles these endpoints harder than the 10/s default.
    _SLOW_ENDPOINTS: frozenset[str] = frozenset(
        {"cards/search", "cards/named", "cards/random", "cards/collection"}
    )

    def __init__(self, rate_limiter: RateLimiter | None = None) -> None:
        # An injected limiter overrides per-endpoint tiering for every request.
        # Left as None, each request uses the limiter for its endpoint's tier.
        self._rate_limiter = rate_limiter

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
        return self._fetch_url(url, limiter=self._limiter_for(endpoint), data=data)

    def _tier_class(self, endpoint: str) -> type[RateLimiter]:
        if endpoint.strip("/") in self._SLOW_ENDPOINTS:
            return SlowRateLimiter
        return RateLimiter

    def _limiter_for(self, endpoint: str) -> RateLimiter:
        tier_default = self._tier_class(endpoint).get_global_limiter()
        limiter = self._rate_limiter if self._rate_limiter is not None else tier_default
        self._warn_if_over_limit(limiter, tier_default, endpoint)
        return limiter

    def _warn_if_over_limit(
        self, limiter: RateLimiter, tier_default: RateLimiter, endpoint: str
    ) -> None:
        if isinstance(limiter, NullRateLimiter):
            return
        if limiter.calls_per_second > tier_default.calls_per_second:
            warnings.warn(
                f"Rate limiter is set to {limiter.calls_per_second}/s for "
                f"'{endpoint}', exceeding Scryfall's {tier_default.calls_per_second}/s "
                f"limit for this endpoint; requests risk being throttled or banned.",
                RateLimitWarning,
                stacklevel=2,
            )

    def _fetch_url(
        self,
        url: str,
        *,
        limiter: RateLimiter | None = None,
        data: dict[str, Any] | None = None,
        rate_limit: bool = True,
    ) -> dict[str, Any]:
        if rate_limit and limiter is not None:
            limiter.wait()

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
