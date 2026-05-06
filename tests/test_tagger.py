"""Tests for scrython.tagger module — CardTags, TagObject, rate limiting, graphql client,
serialization, caching, and card integration."""

import gzip
import json
import threading
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from scrython.cards.cards import Object as CardObject
from scrython.tagger import CardTags, TagBySlug, TagObject, TagSearch
from scrython.tagger.tagger_graphql import TaggerSession
from scrython.tagger.tagger_mixins import CardTagsMixin
from scrython.types import TaggerEdgeData

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "tagger"


# ── Fixture helpers ─────────────────────────────────────────────────────


def load_tag_fixture(filename: str) -> dict:
    """Load a tagger fixture JSON file."""
    with open(FIXTURES_DIR / filename) as f:
        return json.load(f)


@pytest.fixture
def mock_tagger_session():
    """Mock TaggerSession.execute_graphql to return fixture data."""
    with patch.object(TaggerSession, "execute_graphql") as mock_exec:

        def _set_fixture(fixture_name: str):
            mock_exec.return_value = load_tag_fixture(fixture_name)

        yield _set_fixture


@pytest.fixture(autouse=True)
def reset_tagger_session():
    """Reset TaggerSession state before each test."""
    TaggerSession.reset()
    yield
    TaggerSession.reset()


@pytest.fixture(autouse=True)
def restore_tagger_opener():
    """Save and restore TaggerSession._opener around each test."""
    original = TaggerSession._opener
    yield
    TaggerSession._opener = original


# ── TagObject tests ─────────────────────────────────────────────────────


class TestTagObject:
    """Test TagObject wrapper for individual tag/edge data."""

    def test_tag_object_from_tagging(self):
        """Test TagObject created from a TAGGING edge with nested tag data."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Test Card",
            "relatedName": None,
            "subjectName": "Test Card",
            "namespace": "card",
            "annotation": None,
            "metadata": None,
            "tag": {"name": "evasion", "description": "Hard to block"},
        }
        obj = TagObject(TaggerEdgeData(**data))
        assert obj.name == "evasion"
        assert obj.card_name == "Test Card"
        assert obj.classifier == "ORACLE_CARD_TAG"
        assert obj.type == "TAGGING"
        assert obj.namespace == "card"
        assert obj.is_tag is True
        assert obj.is_relationship is False
        assert obj.is_oracle_tag is True
        assert obj.is_printing_tag is False
        assert obj.is_illustration_tag is False

    def test_tag_object_from_relationship(self):
        """Test TagObject created from a RELATIONSHIP edge."""
        data = {
            "classifier": "SIMILAR_TO",
            "type": "RELATIONSHIP",
            "name": "Test Card",
            "relatedName": "Young Pyromancer",
            "subjectName": "Test Card",
            "namespace": "relationship",
            "annotation": None,
            "metadata": None,
        }
        obj = TagObject(TaggerEdgeData(**data))
        assert obj.name == "Young Pyromancer"  # Falls back to relatedName
        assert obj.classifier == "SIMILAR_TO"
        assert obj.type == "RELATIONSHIP"
        assert obj.is_tag is False
        assert obj.is_relationship is True

    def test_tag_object_name_fallback(self):
        """Test TagObject.name falls back to edge 'name' when no tag/relatedName."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Card Name",
            "relatedName": None,
            "subjectName": None,
            "namespace": "card",
            "annotation": None,
            "metadata": None,
        }
        obj = TagObject(TaggerEdgeData(**data))
        assert obj.name == "Card Name"

    def test_tag_object_repr(self):
        """Test TagObject.__repr__."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Card",
            "relatedName": None,
            "subjectName": "Card",
            "namespace": "card",
            "annotation": None,
            "metadata": None,
            "tag": {"name": "evasion", "description": ""},
        }
        obj = TagObject(TaggerEdgeData(**data))
        r = repr(obj)
        assert "TagObject" in r
        assert "evasion" in r
        assert "ORACLE_CARD_TAG" in r

    def test_tag_object_str(self):
        """Test TagObject.__str__."""
        data = {
            "classifier": "ILLUSTRATION_TAG",
            "type": "TAGGING",
            "name": "Card",
            "relatedName": None,
            "subjectName": "Card",
            "namespace": "artwork",
            "annotation": None,
            "metadata": None,
            "tag": {"name": "digital painting", "description": None},
        }
        obj = TagObject(TaggerEdgeData(**data))
        assert str(obj) == "digital painting (ILLUSTRATION_TAG)"

    def test_tag_object_eq(self):
        """Test TagObject equality based on name + classifier."""
        d1 = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "removal"},
        }
        d2 = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "removal"},
        }
        d3 = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "draw"},
        }
        assert TagObject(TaggerEdgeData(**d1)) == TagObject(TaggerEdgeData(**d2))
        assert TagObject(TaggerEdgeData(**d1)) != TagObject(TaggerEdgeData(**d3))
        assert TagObject(TaggerEdgeData(**d1)) != "removal"

    def test_tag_object_hash(self):
        """Test TagObject is hashable."""
        d1 = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "removal"},
        }
        d2 = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "removal"},
        }
        obj1 = TagObject(TaggerEdgeData(**d1))
        obj2 = TagObject(TaggerEdgeData(**d2))
        assert hash(obj1) == hash(obj2)
        s = {obj1, obj2}
        assert len(s) == 1

    def test_tag_object_to_dict(self):
        """Test TagObject.to_dict() returns a copy."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "removal"},
        }
        obj = TagObject(TaggerEdgeData(**data))
        d = obj.to_dict()
        assert d == data
        assert d is not obj._data

    def test_tag_object_illustration_tag(self):
        """Test is_illustration_tag property."""
        data = {
            "classifier": "ILLUSTRATION_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "moon"},
        }
        obj = TagObject(TaggerEdgeData(**data))
        assert obj.is_illustration_tag is True
        assert obj.is_oracle_tag is False
        assert obj.is_printing_tag is False

    def test_tag_object_printing_tag(self):
        """Test is_printing_tag property."""
        data = {
            "classifier": "PRINTING_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "extended art"},
        }
        obj = TagObject(TaggerEdgeData(**data))
        assert obj.is_printing_tag is True


# ── CardTags tests ──────────────────────────────────────────────────────


class TestCardTags:
    """Test CardTags endpoint class."""

    def test_card_tags_basic(self, mock_tagger_session):
        """Test CardTags retrieves and categorizes tags correctly."""
        mock_tagger_session("card_tags_sos170.json")

        tags = CardTags(code="sos", number="170")

        assert tags.card_name == "Abigale, Poet Laureate // Heroic Stanza"
        assert tags.oracle_id == "2f5f46ed-b8aa-4864-bd20-17281d4632bf"
        assert tags.printing_id == "77285d12-e658-4eb3-ba13-ff202afab9c8"
        assert tags.card_id == "77285d12-e658-4eb3-ba13-ff202afab9c8"

    def test_card_tags_count(self, mock_tagger_session):
        """Test tag/relationship counts are correct."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170")

        assert len(tags.tags) == 6  # 3 oracle + 2 illustration + 1 printing
        assert len(tags.relationships) == 1
        assert len(tags.oracle_tags) == 3
        assert len(tags.illustration_tags) == 2
        assert len(tags.printing_tags) == 1

    def test_card_tags_names(self, mock_tagger_session):
        """Test tag names are extracted correctly from nested tag.name."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170")

        assert "repeatable pp counters" in tags.tag_names
        assert "evasion" in tags.tag_names
        assert "removal" in tags.tag_names
        assert "hearing aid" in tags.tag_names
        assert "digital painting" in tags.tag_names
        assert "extended art" in tags.tag_names

    def test_card_tags_has_tag(self, mock_tagger_session):
        """Test has_tag helper method."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170")

        assert tags.has_tag("evasion") is True
        assert tags.has_tag("removal") is True
        assert tags.has_tag("nonexistent") is False

    def test_card_tags_by_namespace(self, mock_tagger_session):
        """Test tags_by_namespace filters correctly."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170")

        card_tags = tags.tags_by_namespace("card")
        assert len(card_tags) == 3
        assert all(t.namespace == "card" for t in card_tags)

        artwork_tags = tags.tags_by_namespace("artwork")
        assert len(artwork_tags) == 2

    def test_card_tags_repr(self, mock_tagger_session):
        """Test CardTags.__repr__."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170")
        r = repr(tags)
        assert "CardTags" in r
        assert "Abigale" in r

    def test_card_tags_str(self, mock_tagger_session):
        """Test CardTags.__str__."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170")
        s = str(tags)
        assert "Tags for" in s
        assert "Abigale" in s


class TestCardTagsErrorHandling:
    """Test CardTags error handling."""

    def test_missing_required_params(self):
        """Test that missing code/number raises ValueError."""
        with pytest.raises(ValueError, match="CardTags requires"):
            CardTags(code="sos")
        with pytest.raises(ValueError, match="CardTags requires"):
            CardTags(number="170")
        with pytest.raises(ValueError, match="CardTags requires"):
            CardTags()

    def test_empty_response(self, mock_tagger_session):
        """Test CardTags with empty cardBySet data."""
        TaggerSession.execute_graphql = Mock(return_value={})
        tags = CardTags(code="xxx", number="999")
        assert tags.card_name is None
        assert len(tags.tags) == 0

    def test_no_edges(self, mock_tagger_session):
        """Test CardTags with card but no edges."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "cardBySet": {
                    "name": "Test Card",
                    "oracleId": "oracle-1",
                    "printingId": "print-1",
                    "edges": [],
                }
            }
        )
        tags = CardTags(code="tst", number="1")
        assert tags.card_name == "Test Card"
        assert len(tags.tags) == 0
        assert len(tags.relationships) == 0


# ── CardTagsMixin tests ─────────────────────────────────────────────────


class TestCardTagsMixin:
    """Test CardTagsMixin independently."""

    def test_process_tags_empty(self):
        """Test _process_tags with no data."""
        mixin = CardTagsMixin()
        mixin._scryfall_data = {}
        mixin._process_tags()
        assert mixin.card_name is None
        assert mixin.tags == []

    def test_process_tags_with_edges(self):
        """Test _process_tags categorizes edges."""
        mixin = CardTagsMixin()
        mixin._scryfall_data = {
            "cardBySet": {
                "name": "Test",
                "oracleId": "o1",
                "printingId": "p1",
                "edges": [
                    {
                        "classifier": "ORACLE_CARD_TAG",
                        "type": "TAGGING",
                        "name": "C",
                        "tag": {"name": "evasion"},
                    },
                    {
                        "classifier": "SIMILAR_TO",
                        "type": "RELATIONSHIP",
                        "name": "C",
                        "relatedName": "Other",
                    },
                ],
            }
        }
        mixin._process_tags()
        assert len(mixin.tags) == 1
        assert len(mixin.relationships) == 1
        assert mixin.card_name == "Test"
        assert mixin.oracle_id == "o1"


# ── Rate limiting on TaggerRequestHandler ──────────────────────────────


class TestTaggerRateLimiting:
    """Test rate limiting on tagger endpoints."""

    def test_rate_limit_default_class(self):
        """Test that TaggerRequestHandler uses TaggerRateLimiter."""
        from scrython.rate_limiter import TaggerRateLimiter
        from scrython.tagger.tagger import TaggerRequestHandler

        assert TaggerRequestHandler._rate_limiter_class is TaggerRateLimiter

    def test_rate_limit_per_second_override(self, mock_tagger_session):
        """Test that rate_limit_per_second creates override limiter."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170", rate_limit_per_second=3.0)
        assert tags._override_limiter is not None
        assert tags._override_limiter.calls_per_second == 3.0

    def test_rate_limit_disabled(self, mock_tagger_session):
        """Test that rate_limit=False disables rate limiting."""
        mock_tagger_session("card_tags_sos170.json")
        tags = CardTags(code="sos", number="170", rate_limit=False)
        assert tags._rate_limited is False


# ── TaggerRateLimiter tests ─────────────────────────────────────────────


class TestTaggerRateLimiter:
    """Test TaggerRateLimiter class."""

    def test_default_rate(self):
        """Test TaggerRateLimiter defaults to 5 req/s."""
        from scrython.rate_limiter import TaggerRateLimiter

        limiter = TaggerRateLimiter()
        assert limiter.calls_per_second == 5.0
        assert limiter.min_interval == 0.2

    def test_custom_rate(self):
        """Test TaggerRateLimiter with custom rate."""
        from scrython.rate_limiter import TaggerRateLimiter

        limiter = TaggerRateLimiter(calls_per_second=10.0)
        assert limiter.calls_per_second == 10.0

    def test_independent_registry(self):
        """Test TaggerRateLimiter has its own global instance."""
        from scrython.rate_limiter import RateLimiter, TaggerRateLimiter

        RateLimiter.reset_all_limiters()
        fast = RateLimiter.get_global_limiter()
        tagger = TaggerRateLimiter.get_global_limiter()
        assert fast is not tagger
        assert fast.calls_per_second != tagger.calls_per_second


# ── TaggerSession tests ────────────────────────────────────────────────


def _mock_opener(body: bytes):
    """Create a mock response on TaggerSession._opener that returns body."""
    resp = MagicMock()
    resp.read.return_value = body
    resp.__enter__ = Mock(return_value=resp)
    resp.__exit__ = Mock(return_value=False)
    TaggerSession._opener = MagicMock()
    TaggerSession._opener.open = Mock(return_value=resp)


class TestTaggerSessionRefresh:
    """Test TaggerSession._refresh_session."""

    def test_extracts_csrf_token(self):
        """CSRF token extracted from HTML meta tag."""
        _mock_opener(b'<meta name="csrf-token" content="abc-123">')
        TaggerSession._refresh_session()
        assert TaggerSession._csrf_token == "abc-123"

    def test_missing_csrf_raises(self):
        """Missing CSRF meta tag raises RuntimeError."""
        _mock_opener(b"<html>no csrf</html>")
        with pytest.raises(RuntimeError, match="Could not extract CSRF token"):
            TaggerSession._refresh_session()

    def test_gzip_decompressed(self):
        """Gzip-compressed HTML is decompressed before parsing."""
        html = b'<meta name="csrf-token" content="gzip-csrf">'
        _mock_opener(gzip.compress(html))
        TaggerSession._refresh_session()
        assert TaggerSession._csrf_token == "gzip-csrf"

    def test_http_error_raises(self):
        """HTTP errors raise RuntimeError."""
        _mock_opener(b"")
        err = urllib.error.HTTPError("url", 500, "Error", MagicMock(), BytesIO(b""))
        TaggerSession._opener.open.side_effect = err
        with pytest.raises(RuntimeError, match="HTTP 500"):
            TaggerSession._refresh_session()

    def test_connection_error_raises(self):
        """Connection errors raise RuntimeError."""
        TaggerSession._opener = MagicMock()
        TaggerSession._opener.open = Mock(side_effect=urllib.error.URLError("refused"))
        with pytest.raises(RuntimeError, match="Failed to connect"):
            TaggerSession._refresh_session()

    def test_csrf_with_extra_attrs(self):
        """CSRF extraction works with additional meta attributes present."""
        _mock_opener(b'<meta charset="utf-8"><meta name="csrf-token" content="multi-attr">')
        TaggerSession._refresh_session()
        assert TaggerSession._csrf_token == "multi-attr"


class TestTaggerSessionEnsure:
    """Test TaggerSession.ensure_session."""

    def test_first_call_initializes(self):
        """First call to ensure_session initializes the session."""
        _mock_opener(b'<meta name="csrf-token" content="first-init">')
        assert TaggerSession._initialized is False
        TaggerSession.ensure_session()
        assert TaggerSession._initialized is True
        assert TaggerSession._csrf_token == "first-init"

    def test_second_call_is_noop(self):
        """Second call does not re-initialize."""
        _mock_opener(b'<meta name="csrf-token" content="only-once">')
        TaggerSession.ensure_session()
        TaggerSession._csrf_token = "overwritten-in-test"
        TaggerSession.ensure_session()
        assert TaggerSession._csrf_token == "overwritten-in-test"

    def test_thread_safety(self):
        """Multiple threads calling ensure_session only initialize once."""
        _mock_opener(b'<meta name="csrf-token" content="thread-safe">')
        TaggerSession._initialized = False

        def worker():
            TaggerSession.ensure_session()

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert TaggerSession._csrf_token == "thread-safe"
        assert TaggerSession._initialized is True


class TestTaggerSessionExecute:
    """Test TaggerSession.execute_graphql."""

    def _setup(self, csrf="csrf-exec"):
        _mock_opener(f'<meta name="csrf-token" content="{csrf}">'.encode())
        TaggerSession.ensure_session()

    def _mock_graphql(self, data: dict):
        body = json.dumps(data).encode()
        TaggerSession._opener = MagicMock()
        resp = MagicMock()
        resp.read.return_value = body
        resp.__enter__ = Mock(return_value=resp)
        resp.__exit__ = Mock(return_value=False)
        TaggerSession._opener.open = Mock(return_value=resp)

    def test_simple_query(self):
        """Basic query returns unwrapped data."""
        self._setup()
        self._mock_graphql({"data": {"__typename": "Query"}})
        assert TaggerSession.execute_graphql("{x}") == {"__typename": "Query"}

    def test_with_variables(self):
        """Query with variables works."""
        self._setup()
        self._mock_graphql({"data": {"cardBySet": {"name": "Test"}}})
        result = TaggerSession.execute_graphql("query($s:String!){cardBySet(set:$s)}", {"s": "lea"})
        assert result == {"cardBySet": {"name": "Test"}}

    def test_graphql_errors_raise(self):
        """GraphQL errors raise RuntimeError with messages."""
        self._setup()
        self._mock_graphql(
            {"errors": [{"message": "Field badField not found"}, {"message": "Error 2"}]}
        )
        with pytest.raises(RuntimeError, match="GraphQL errors.*badField.*Error 2"):
            TaggerSession.execute_graphql("{x}")

    def test_graphql_error_no_message_key(self):
        """Error entries without 'message' key are handled."""
        self._setup()
        self._mock_graphql({"errors": [{"code": "UNKNOWN"}]})
        with pytest.raises(RuntimeError, match="GraphQL errors"):
            TaggerSession.execute_graphql("{x}")

    def test_csrf_failure_retry(self):
        """CSRF failure triggers refresh and retry succeeds."""
        self._setup("expired-csrf")
        opener = MagicMock()
        # 1st POST: CSRF fail
        r1 = MagicMock()
        r1.read.return_value = b'{"message":"invalid authenticity token"}'
        r1.__enter__ = Mock(return_value=r1)
        r1.__exit__ = Mock(return_value=False)
        # 2nd: GET refresh
        r2 = MagicMock()
        r2.read.return_value = b'<meta name="csrf-token" content="new-csrf">'
        r2.__enter__ = Mock(return_value=r2)
        r2.__exit__ = Mock(return_value=False)
        # 3rd POST: success
        r3 = MagicMock()
        r3.read.return_value = b'{"data":{"ok":true}}'
        r3.__enter__ = Mock(return_value=r3)
        r3.__exit__ = Mock(return_value=False)
        opener.open = Mock(side_effect=[r1, r2, r3])
        TaggerSession._opener = opener
        assert TaggerSession.execute_graphql("{x}") == {"ok": True}
        assert TaggerSession._csrf_token == "new-csrf"

    def test_http_error_raises(self):
        """HTTP 500 raises RuntimeError."""
        self._setup()
        err = urllib.error.HTTPError("url", 500, "Error", MagicMock(), BytesIO(b"boom"))
        TaggerSession._opener = MagicMock()
        TaggerSession._opener.open = Mock(side_effect=err)
        with pytest.raises(RuntimeError, match="GraphQL request failed"):
            TaggerSession.execute_graphql("{x}")

    def test_connection_error_raises(self):
        """URLError raises RuntimeError."""
        self._setup()
        TaggerSession._opener = MagicMock()
        TaggerSession._opener.open = Mock(side_effect=urllib.error.URLError("timeout"))
        with pytest.raises(RuntimeError, match="Failed to connect"):
            TaggerSession.execute_graphql("{x}")

    def test_gzip_decompressed(self):
        """Gzip-compressed GraphQL response is decompressed."""
        self._setup()
        TaggerSession._opener = MagicMock()
        resp = MagicMock()
        resp.read.return_value = gzip.compress(b'{"data":{"z":"gzip"}}')
        resp.__enter__ = Mock(return_value=resp)
        resp.__exit__ = Mock(return_value=False)
        TaggerSession._opener.open = Mock(return_value=resp)
        assert TaggerSession.execute_graphql("{x}") == {"z": "gzip"}

    def test_no_data_envelope(self):
        """Response without 'data' key returned as-is."""
        self._setup()
        self._mock_graphql({"direct": "value"})
        assert TaggerSession.execute_graphql("{x}") == {"direct": "value"}

    def test_list_response(self):
        """List response returned as-is."""
        self._setup()
        TaggerSession._opener = MagicMock()
        resp = MagicMock()
        resp.read.return_value = b'[{"a":1}]'
        resp.__enter__ = Mock(return_value=resp)
        resp.__exit__ = Mock(return_value=False)
        TaggerSession._opener.open = Mock(return_value=resp)
        assert TaggerSession.execute_graphql("{x}") == [{"a": 1}]

    def test_auto_initializes_session(self):
        """execute_graphql auto-initializes session if not already done."""
        TaggerSession.reset()
        _mock_opener(b'<meta name="csrf-token" content="auto-csrf">')
        self._mock_graphql({"data": {"ok": True}})
        opener = MagicMock()
        r1 = MagicMock()
        r1.read.return_value = b'<meta name="csrf-token" content="auto-csrf">'
        r1.__enter__ = Mock(return_value=r1)
        r1.__exit__ = Mock(return_value=False)
        r2 = MagicMock()
        r2.read.return_value = b'{"data":{"ok":true}}'
        r2.__enter__ = Mock(return_value=r2)
        r2.__exit__ = Mock(return_value=False)
        opener.open = Mock(side_effect=[r1, r2])
        TaggerSession._opener = opener
        TaggerSession._csrf_token = None
        TaggerSession._initialized = False
        assert TaggerSession.execute_graphql("{x}") == {"ok": True}
        assert TaggerSession._initialized is True


class TestTaggerSessionReset:
    """Test TaggerSession.reset."""

    def test_reset_clears_state(self):
        """Reset clears CSRF, init flag, and cookie jar."""
        TaggerSession._csrf_token = "fake-token"
        TaggerSession._initialized = True
        TaggerSession.reset()
        assert TaggerSession._csrf_token is None
        assert TaggerSession._initialized is False
        assert len(TaggerSession._cookie_jar) == 0

    def test_can_reinitialize_after_reset(self):
        """After reset, session can be re-initialized."""
        TaggerSession.reset()
        _mock_opener(b'<meta name="csrf-token" content="post-reset">')
        TaggerSession.ensure_session()
        assert TaggerSession._csrf_token == "post-reset"
        assert TaggerSession._initialized is True


# ── TagSearch tests ────────────────────────────────────────────────────


class TestTagSearch:
    """Test TagSearch endpoint."""

    def test_tag_search_basic(self):
        """Test TagSearch with mock data."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "tags": {
                    "page": 1,
                    "perPage": 25,
                    "total": 100,
                    "results": [
                        {
                            "id": "1",
                            "name": "evasion",
                            "namespace": "function",
                            "description": "Evasion abilities",
                            "category": False,
                        },
                        {
                            "id": "2",
                            "name": "removal",
                            "namespace": "function",
                            "description": "Removal",
                            "category": False,
                        },
                    ],
                }
            }
        )
        results = TagSearch()
        assert results.total == 100
        assert len(results.data) == 2
        assert results.data[0]["name"] == "evasion"

    def test_tag_search_with_input(self):
        """Test TagSearch with input filter."""
        TaggerSession.execute_graphql = Mock(
            return_value={"tags": {"page": 1, "perPage": 25, "total": 5, "results": []}}
        )
        results = TagSearch(input={"namespace": "function"})
        assert results.total == 5

    def test_tag_search_repr(self):
        """Test TagSearch.__repr__."""
        TaggerSession.execute_graphql = Mock(
            return_value={"tags": {"page": 1, "perPage": 25, "total": 42, "results": []}}
        )
        results = TagSearch()
        assert "TagSearch" in repr(results)
        assert "42" in repr(results)


# ── TagBySlug tests ────────────────────────────────────────────────────


class TestTagBySlug:
    """Test TagBySlug endpoint."""

    def test_tag_by_slug_basic(self):
        """Test TagBySlug with mock data."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "tagBySlug": {
                    "id": "tag-1",
                    "name": "evasion",
                    "namespace": "function",
                    "description": "Evasion abilities",
                    "category": False,
                    "aliases": [{"name": "unblockable"}],
                }
            }
        )
        tag = TagBySlug(slug="evasion", type="ORACLE_CARD_TAG")
        assert tag.name == "evasion"
        assert tag.namespace == "function"
        assert tag.description == "Evasion abilities"
        assert tag.is_category is False
        assert tag.aliases == ["unblockable"]

    def test_tag_by_slug_missing_args(self):
        """Test TagBySlug raises ValueError for missing args."""
        with pytest.raises(ValueError, match="TagBySlug requires"):
            TagBySlug(slug="test")

    def test_tag_by_slug_no_aliases(self):
        """Test TagBySlug with no aliases."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "tagBySlug": {
                    "id": "tag-1",
                    "name": "removal",
                    "namespace": "function",
                    "description": None,
                    "category": True,
                    "aliases": [],
                }
            }
        )
        tag = TagBySlug(slug="removal", type="ORACLE_CARD_TAG")
        assert tag.aliases == []
        assert tag.is_category is True


# ── Serialization tests ─────────────────────────────────────────────────


class TestTagObjectSerialization:
    """Test TagObject serialization methods."""

    def test_to_json(self):
        """Test TagObject.to_json() exports valid JSON."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Card",
            "tag": {"name": "evasion", "description": "Hard to block"},
        }
        obj = TagObject(TaggerEdgeData(**data))
        json_str = obj.to_json()
        parsed = json.loads(json_str)
        assert parsed["classifier"] == "ORACLE_CARD_TAG"
        assert parsed["tag"]["name"] == "evasion"

    def test_to_json_pretty(self):
        """Test TagObject.to_json() with indent."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Card",
            "tag": {"name": "removal"},
        }
        obj = TagObject(TaggerEdgeData(**data))
        json_str = obj.to_json(indent=2)
        assert "\n" in json_str
        parsed = json.loads(json_str)
        assert parsed["tag"]["name"] == "removal"

    def test_from_dict(self):
        """Test TagObject.from_dict() rehydrates correctly."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Card",
            "tag": {"name": "evasion", "description": ""},
        }
        obj = TagObject.from_dict(data)
        assert obj.name == "evasion"
        assert obj.classifier == "ORACLE_CARD_TAG"
        assert obj.is_tag is True

    def test_from_dict_copy(self):
        """Test TagObject.from_dict() creates independent copy."""
        data = {
            "classifier": "ILLUSTRATION_TAG",
            "type": "TAGGING",
            "name": "C",
            "tag": {"name": "moon"},
        }
        obj = TagObject.from_dict(data)
        data["tag"]["name"] = "sun"
        assert obj.name == "moon"  # Unchanged

    def test_roundtrip(self):
        """Test TagObject to_dict -> from_dict roundtrip."""
        data = {
            "classifier": "ORACLE_CARD_TAG",
            "type": "TAGGING",
            "name": "Card",
            "relatedName": None,
            "subjectName": "Card",
            "namespace": "card",
            "annotation": None,
            "metadata": None,
            "tag": {"name": "evasion", "description": ""},
        }
        obj1 = TagObject(TaggerEdgeData(**data))
        obj2 = TagObject.from_dict(obj1.to_dict())
        assert obj1 == obj2
        assert obj1.name == obj2.name
        assert obj1.classifier == obj2.classifier


class TestCardTagsSerialization:
    """Test CardTags serialization (inherited from ScrythonRequestHandler)."""

    def test_card_tags_to_dict(self):
        """Test CardTags.to_dict() returns scryfall_data."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "cardBySet": {
                    "name": "Test Card",
                    "oracleId": "oracle-1",
                    "printingId": "print-1",
                    "edges": [],
                }
            }
        )
        tags = CardTags(code="tst", number="1")
        d = tags.to_dict()
        assert d["cardBySet"]["name"] == "Test Card"

    def test_card_tags_to_json(self):
        """Test CardTags.to_json() returns valid JSON."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "cardBySet": {
                    "name": "Test",
                    "oracleId": "o1",
                    "printingId": "p1",
                    "edges": [],
                }
            }
        )
        tags = CardTags(code="tst", number="1")
        json_str = tags.to_json()
        parsed = json.loads(json_str)
        assert parsed["cardBySet"]["name"] == "Test"

    def test_card_tags_from_dict(self):
        """Test CardTags.from_dict() rehydrates without API call."""
        data = {
            "cardBySet": {
                "name": "Rehydrated",
                "oracleId": "o1",
                "printingId": "p1",
                "edges": [
                    {
                        "classifier": "ORACLE_CARD_TAG",
                        "type": "TAGGING",
                        "name": "C",
                        "tag": {"name": "evasion"},
                    }
                ],
            }
        }
        tags = CardTags.from_dict(data)
        assert tags.card_name == "Rehydrated"
        assert len(tags.tags) == 1
        assert tags.tags[0].name == "evasion"

    def test_card_tags_from_dict_independent(self):
        """Test CardTags.from_dict() copy is independent."""
        data = {
            "cardBySet": {
                "name": "Original",
                "oracleId": "o1",
                "printingId": "p1",
                "edges": [],
            }
        }
        tags = CardTags.from_dict(data)
        data["cardBySet"]["name"] = "Modified"
        assert tags.card_name == "Original"

    def test_card_tags_hashable(self):
        """Test CardTags objects are hashable (by id)."""
        fixture = load_tag_fixture("card_tags_sos170.json")
        TaggerSession.execute_graphql = Mock(return_value=fixture)
        tags1 = CardTags(code="sos", number="170")
        tags2 = CardTags(code="sos", number="170")
        # Both should be hashable (hash based on instance id for tagger objects
        # since there's no 'id' in the root scryfall_data dict)
        s = {tags1, tags2}
        assert len(s) == 2  # Different instances, no shared 'id' field


class TestTagSearchSerialization:
    """Test TagSearch serialization."""

    def test_tag_search_to_dict(self):
        """Test TagSearch.to_dict()."""
        TaggerSession.execute_graphql = Mock(
            return_value={"tags": {"page": 1, "perPage": 25, "total": 42, "results": []}}
        )
        results = TagSearch()
        d = results.to_dict()
        assert d["tags"]["total"] == 42

    def test_tag_search_to_json(self):
        """Test TagSearch.to_json()."""
        TaggerSession.execute_graphql = Mock(
            return_value={"tags": {"page": 1, "perPage": 25, "total": 10, "results": []}}
        )
        results = TagSearch()
        json_str = results.to_json()
        parsed = json.loads(json_str)
        assert parsed["tags"]["total"] == 10

    def test_tag_search_from_dict(self):
        """Test TagSearch.from_dict()."""
        data = {"tags": {"page": 1, "perPage": 25, "total": 7, "results": []}}
        results = TagSearch.from_dict(data)
        assert results.total == 7


class TestTagBySlugSerialization:
    """Test TagBySlug serialization."""

    def test_to_dict(self):
        """Test TagBySlug.to_dict()."""
        TaggerSession.execute_graphql = Mock(
            return_value={
                "tagBySlug": {
                    "id": "tag-1",
                    "name": "evasion",
                    "namespace": "function",
                    "description": "Evasion",
                    "category": False,
                    "aliases": [],
                }
            }
        )
        tag = TagBySlug(slug="evasion", type="ORACLE_CARD_TAG")
        d = tag.to_dict()
        assert d["tagBySlug"]["name"] == "evasion"

    def test_from_dict(self):
        """Test TagBySlug.from_dict()."""
        data = {
            "tagBySlug": {
                "id": "tag-1",
                "name": "removal",
                "namespace": "function",
                "description": "Removal",
                "category": False,
                "aliases": [],
            }
        }
        tag = TagBySlug.from_dict(data)
        assert tag.name == "removal"
        assert tag.namespace == "function"


# ── Caching tests ───────────────────────────────────────────────────────


class TestTaggerCaching:
    """Test caching on tagger endpoints."""

    def test_cache_hit_skips_graphql(self):
        """Test that a cache hit skips the GraphQL call."""
        from scrython.cache import reset_global_cache

        reset_global_cache()

        data = {
            "cardBySet": {
                "name": "Cached Card",
                "oracleId": "o1",
                "printingId": "p1",
                "edges": [],
            }
        }

        call_count = 0
        original_execute = TaggerSession.execute_graphql

        def counting_execute(_query, _variables=None):
            nonlocal call_count
            call_count += 1
            return data

        TaggerSession.execute_graphql = counting_execute

        # First call: cache miss, should call GraphQL
        tags1 = CardTags(code="tst", number="1", cache=True, cache_ttl=3600)
        assert call_count == 1
        assert tags1.card_name == "Cached Card"

        # Second call: cache hit, should NOT call GraphQL
        tags2 = CardTags(code="tst", number="1", cache=True, cache_ttl=3600)
        assert call_count == 1  # Still 1
        assert tags2.card_name == "Cached Card"

        # Restore
        TaggerSession.execute_graphql = original_execute
        reset_global_cache()

    def test_cache_disabled_calls_graphql(self):
        """Test that cache=False always calls GraphQL."""
        data = {
            "cardBySet": {
                "name": "Fresh",
                "oracleId": "o1",
                "printingId": "p1",
                "edges": [],
            }
        }

        call_count = 0
        original = TaggerSession.execute_graphql

        def counting(_query, _variables=None):
            nonlocal call_count
            call_count += 1
            return data

        TaggerSession.execute_graphql = counting

        # First call
        CardTags(code="tst", number="1", cache=False)
        assert call_count == 1

        # Second call (no cache)
        CardTags(code="tst", number="1", cache=False)
        assert call_count == 2

        TaggerSession.execute_graphql = original

    def test_different_queries_have_different_cache_keys(self):
        """Test that different code/number combos have different cache keys."""
        from scrython.cache import reset_global_cache

        reset_global_cache()

        data1 = {
            "cardBySet": {
                "name": "Card A",
                "oracleId": "oa",
                "printingId": "pa",
                "edges": [],
            }
        }
        data2 = {
            "cardBySet": {
                "name": "Card B",
                "oracleId": "ob",
                "printingId": "pb",
                "edges": [],
            }
        }

        call_count = 0
        original = TaggerSession.execute_graphql

        def counting(_query, variables=None):
            nonlocal call_count
            call_count += 1
            if variables and variables.get("number") == "1":
                return data1
            return data2

        TaggerSession.execute_graphql = counting

        tags1 = CardTags(code="tst", number="1", cache=True)
        assert call_count == 1
        assert tags1.card_name == "Card A"

        tags2 = CardTags(code="tst", number="2", cache=True)
        assert call_count == 2  # Different cache key
        assert tags2.card_name == "Card B"

        tags3 = CardTags(code="tst", number="1", cache=True)
        assert call_count == 2  # Cache hit for number="1"
        assert tags3.card_name == "Card A"

        TaggerSession.execute_graphql = original
        reset_global_cache()


# ── Card integration tests ──────────────────────────────────────────────


class TestCardTaggerIntegration:
    """Test get_tags(), get_tag_names(), has_tag() on card objects."""

    @pytest.fixture(autouse=True)
    def mock_tagger_execute(self):
        """Mock TaggerSession.execute_graphql for all integration tests."""
        from scrython.cache import reset_global_cache

        reset_global_cache()

        fixture = load_tag_fixture("card_tags_sos170.json")
        with patch.object(TaggerSession, "execute_graphql", return_value=fixture):
            yield

    def _make_card(self, set_code="sos", collector_number="170"):
        """Create a minimal card Object with set and collector_number."""
        return CardObject(
            {
                "id": "77285d12-e658-4eb3-ba13-ff202afab9c8",
                "name": "Abigale, Poet Laureate",
                "object": "card",
                "lang": "en",
                "layout": "transform",
                "set": set_code,
                "collector_number": collector_number,
                "set_name": "Some Set",
                "rarity": "rare",
                "type_line": "Creature",
                "cmc": 3.0,
                "color_identity": ["W"],
                "keywords": [],
                "legalities": {},
                "reserved": False,
                "booster": True,
                "border_color": "black",
                "digital": False,
                "finishes": ["nonfoil"],
                "frame": "2015",
                "full_art": False,
                "games": ["paper"],
                "highres_image": True,
                "image_status": "highres_scan",
                "prices": {"usd": None},
                "promo": False,
                "released_at": "2024-01-01",
                "reprint": False,
                "scryfall_set_uri": "https://scryfall.com/sets/sos",
                "set_search_uri": "https://api.scryfall.com/cards/search?q=set:sos",
                "set_type": "expansion",
                "set_uri": "https://api.scryfall.com/sets/sos",
                "set_id": "set-id-1",
                "story_spotlight": False,
                "textless": False,
                "variation": False,
                "prints_search_uri": "https://api.scryfall.com/cards/search?q=prints",
                "rulings_uri": "https://api.scryfall.com/cards/rulings/1",
                "scryfall_uri": "https://scryfall.com/card/sos/170",
                "uri": "https://api.scryfall.com/cards/1",
                "card_back_id": "card-back-id",
                "related_uris": {},
            }
        )

    def test_get_tags_returns_card_tags(self):
        """Test get_tags() returns a CardTags object."""
        card = self._make_card()
        tags = card.get_tags()
        assert isinstance(tags, CardTags)
        assert tags.card_name is not None

    def test_get_tags_with_set_and_number(self):
        """Test get_tags() extracts set and collector_number correctly."""
        card = self._make_card()
        tags = card.get_tags()
        assert "evasion" in tags.tag_names
        assert "removal" in tags.tag_names

    def test_get_tags_caching(self):
        """Test get_tags() with caching enabled."""
        card = self._make_card()

        # First call
        tags1 = card.get_tags(cache=True, cache_ttl=3600)
        assert isinstance(tags1, CardTags)

        # Second call (should use cache)
        tags2 = card.get_tags(cache=True, cache_ttl=3600)
        assert tags2.card_name == tags1.card_name

    def test_get_tag_names_convenience(self):
        """Test get_tag_names() returns list of tag names."""
        card = self._make_card()
        names = card.get_tag_names()
        assert isinstance(names, list)
        assert "evasion" in names
        assert "removal" in names
        assert "extended art" in names

    def test_has_tag_convenience(self):
        """Test has_tag() convenience method."""
        card = self._make_card()
        assert card.has_tag("removal") is True
        assert card.has_tag("evasion") is True
        assert card.has_tag("nonexistent") is False

    def test_get_tags_missing_set(self):
        """Test get_tags() raises ValueError when set field is missing."""
        card = self._make_card()
        card._scryfall_data.pop("set")
        with pytest.raises(ValueError, match="missing 'set' or 'collector_number'"):
            card.get_tags()

    def test_get_tags_missing_collector_number(self):
        """Test get_tags() raises ValueError when collector_number is missing."""
        card = self._make_card()
        card._scryfall_data.pop("collector_number")
        with pytest.raises(ValueError, match="missing 'set' or 'collector_number'"):
            card.get_tags()

    def test_get_tags_rate_limit_kwargs(self):
        """Test get_tags() accepts rate_limit kwargs."""
        card = self._make_card()
        tags = card.get_tags(rate_limit=True, rate_limit_per_second=3.0)
        assert tags is not None

    def test_get_tags_caches_per_query(self):
        """Test that get_tags() caches are reused for the same card."""
        from scrython.cache import reset_global_cache

        reset_global_cache()

        card = self._make_card()

        tags1 = card.get_tags(cache=True, cache_ttl=3600)
        tags2 = card.get_tags(cache=True, cache_ttl=3600)

        # Both should return tags with the same data
        assert tags1.card_name == tags2.card_name
        assert tags1.tag_names == tags2.tag_names

        reset_global_cache()
