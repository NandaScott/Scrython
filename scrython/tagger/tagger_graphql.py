"""
GraphQL client for tagger.scryfall.com.

Provides session management (cookie + CSRF token) and GraphQL query
execution for the Scryfall Tagger API. Used internally by endpoint
classes; not exposed directly to library consumers.

The session is shared at class level with a threading lock, so all
TaggerRequestHandler instances share one connection to the tagger
server with one CSRF token per session.
"""

import gzip
import json
import re
import threading
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from typing import Any, ClassVar

# A well-known card page to use for obtaining session cookies + CSRF token.
_DEFAULT_SESSION_PAGE = "https://tagger.scryfall.com/card/sos/170"

_AGENT = "Scrython/2.0 (https://github.com/NandaScott/Scrython)"


class TaggerSession:
    """
    Thread-safe shared session for tagger.scryfall.com.

    Maintains a persistent cookie jar, opener, and CSRF token.
    Automatically initializes on first use and refreshes the CSRF
    token when needed.
    """

    _cookie_jar: ClassVar[CookieJar] = CookieJar()
    _opener: ClassVar[urllib.request.OpenerDirector] = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(_cookie_jar)
    )
    _csrf_token: ClassVar[str | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _initialized: ClassVar[bool] = False

    @classmethod
    def _refresh_session(cls) -> None:
        """
        Fetch a fresh session cookie and CSRF token from the tagger server.

        Makes a GET request to a known card page on tagger.scryfall.com,
        extracts the CSRF token from the <meta> tag, and stores the
        session cookie.
        """
        headers = {
            "User-Agent": _AGENT,
            "Accept": "text/html,application/json,*/*",
            "Accept-Encoding": "gzip, deflate",
        }
        req = urllib.request.Request(_DEFAULT_SESSION_PAGE, headers=headers)

        try:
            with cls._opener.open(req, timeout=15) as resp:
                raw = resp.read()
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    pass
                html = raw.decode("utf-8", errors="replace")

            # Extract CSRF token from <meta name="csrf-token" content="...">
            match = re.search(r'<meta[^>]+name="csrf-token"[^>]+content="([^"]+)"', html)
            if match:
                cls._csrf_token = match.group(1)
            else:
                raise RuntimeError("Could not extract CSRF token from tagger.scryfall.com")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Failed to establish tagger session: HTTP {e.code}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to tagger.scryfall.com: {e.reason}") from e

    @classmethod
    def ensure_session(cls) -> None:
        """
        Ensure a valid session + CSRF token exists.

        Initializes the session on first call and refreshes if needed.
        Thread-safe via internal lock.
        """
        with cls._lock:
            if not cls._initialized:
                cls._refresh_session()
                cls._initialized = True

    @classmethod
    def execute_graphql(cls, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute a GraphQL query against tagger.scryfall.com.

        Automatically handles session initialization and CSRF token
        management. On CSRF failure, refreshes the session once and retries.

        Args:
            query: GraphQL query string
            variables: Optional query variables dictionary

        Returns:
            Parsed JSON response data dict (the 'data' field from GraphQL)

        Raises:
            RuntimeError: On network errors, CSRF failures, or GraphQL errors
        """
        cls.ensure_session()

        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")

        headers = {
            "User-Agent": _AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "X-CSRF-Token": cls._csrf_token or "",
        }
        req = urllib.request.Request(
            "https://tagger.scryfall.com/graphql",
            data=payload,
            headers=headers,
            method="POST",
        )

        try:
            with cls._opener.open(req, timeout=15) as resp:
                raw = resp.read()
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    pass
                data = json.loads(raw.decode("utf-8", errors="replace"))

            # Check for CSRF failure (Rails returns 422 in body sometimes)
            if isinstance(data, dict) and data.get("message") == "invalid authenticity token":
                # Refresh CSRF and retry once
                with cls._lock:
                    cls._refresh_session()
                headers["X-CSRF-Token"] = cls._csrf_token or ""
                req = urllib.request.Request(
                    "https://tagger.scryfall.com/graphql",
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with cls._opener.open(req, timeout=15) as resp:
                    raw = resp.read()
                    try:
                        raw = gzip.decompress(raw)
                    except Exception:
                        pass
                    data = json.loads(raw.decode("utf-8", errors="replace"))

            # Check for GraphQL errors
            if isinstance(data, dict) and "errors" in data:
                error_messages = [err.get("message", str(err)) for err in data["errors"]]
                raise RuntimeError(f"GraphQL errors: {'; '.join(error_messages)}")

            # Unwrap the 'data' envelope
            if isinstance(data, dict) and "data" in data:
                return data["data"]

            return data

        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            raise RuntimeError(
                f"GraphQL request failed (HTTP {e.code}): "
                f"{body.decode('utf-8', errors='replace')[:300]}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to tagger.scryfall.com: {e.reason}") from e

    @classmethod
    def reset(cls) -> None:
        """
        Reset the session state.

        Clears cookies, CSRF token, and initialization flag.
        Useful for testing to ensure a clean state between tests.
        """
        with cls._lock:
            cls._cookie_jar = CookieJar()
            cls._opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(cls._cookie_jar)
            )
            cls._csrf_token = None
            cls._initialized = False
