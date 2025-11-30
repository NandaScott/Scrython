"""Tests for scrython.base module - ScryfallError and ScrythonRequestHandler."""

import pytest

from scrython.base import ScryfallError, ScrythonRequestHandler


class TestScryfallError:
    """Test the ScryfallError exception class."""

    def test_scryfall_error_initialization(self):
        """Test that ScryfallError initializes with correct attributes."""
        error_data = {
            "status": 404,
            "code": "not_found",
            "details": "No cards found matching criteria",
            "type": "ambiguous",
            "warnings": ["Check your spelling"],
        }

        error = ScryfallError(error_data, "Test error message")

        assert error.status == 404
        assert error.code == "not_found"
        assert error.details == "No cards found matching criteria"
        assert error.type == "ambiguous"
        assert error.warnings == ["Check your spelling"]

    def test_scryfall_error_is_exception(self):
        """Test that ScryfallError is an Exception."""
        error_data = {
            "status": 500,
            "code": "internal_error",
            "details": "Something went wrong",
            "type": None,
            "warnings": None,
        }

        error = ScryfallError(error_data)

        assert isinstance(error, Exception)


class TestRequestHandlerPathBuilding:
    """Test the _build_path functionality of ScrythonRequestHandler."""

    def test_simple_path_no_params(self):
        """Test building a path with no parameters."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

            def __init__(self, **kwargs):
                # Only build path, don't fetch
                self._build_path(**kwargs)

        handler = TestHandler()
        assert handler.endpoint == "cards/named"

    def test_path_with_required_param(self):
        """Test building a path with a required parameter."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/:id"

            def __init__(self, **kwargs):
                self._build_path(**kwargs)

        handler = TestHandler(id="abc123")
        assert handler.endpoint == "cards/abc123"

    def test_path_with_multiple_required_params(self):
        """Test building a path with multiple required parameters."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/:code/:number"

            def __init__(self, **kwargs):
                self._build_path(**kwargs)

        handler = TestHandler(code="m21", number="123")
        assert handler.endpoint == "cards/m21/123"

    def test_path_with_optional_param_provided(self):
        """Test building a path with an optional parameter that is provided."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/:code/:number/:lang?"

            def __init__(self, **kwargs):
                self._build_path(**kwargs)

        handler = TestHandler(code="m21", number="123", lang="en")
        assert handler.endpoint == "cards/m21/123/en"

    def test_path_with_optional_param_not_provided(self):
        """Test building a path with an optional parameter that is not provided."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/:code/:number/:lang?"

            def __init__(self, **kwargs):
                self._build_path(**kwargs)

        handler = TestHandler(code="m21", number="123")
        assert handler.endpoint == "cards/m21/123"

    def test_missing_required_param_raises_error(self):
        """Test that missing required parameters raise KeyError."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/:id"

            def __init__(self, **kwargs):
                self._build_path(**kwargs)

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            TestHandler()

    def test_path_with_leading_trailing_slashes(self):
        """Test that leading/trailing slashes are handled correctly."""

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "/cards/named/"

            def __init__(self, **kwargs):
                self._build_path(**kwargs)

        handler = TestHandler()
        assert handler.endpoint == "cards/named"


class TestRequestHandlerParamBuilding:
    """Test the _build_params functionality of ScrythonRequestHandler."""

    def test_default_params(self):
        """Test that default parameters are set correctly."""

        class TestHandler(ScrythonRequestHandler):
            def __init__(self, **kwargs):
                self._build_params(**kwargs)

        handler = TestHandler()
        assert handler._query_params["format"] == "json"
        assert handler._query_params["face"] == ""
        assert handler._query_params["version"] == ""
        assert handler._query_params["pretty"] == ""

    def test_custom_params_override_defaults(self):
        """Test that custom parameters override defaults."""

        class TestHandler(ScrythonRequestHandler):
            def __init__(self, **kwargs):
                self._build_params(**kwargs)

        handler = TestHandler(format="image", pretty="true")
        assert handler._query_params["format"] == "image"
        assert handler._query_params["pretty"] == "true"

    def test_additional_params_included(self):
        """Test that additional parameters are included."""

        class TestHandler(ScrythonRequestHandler):
            def __init__(self, **kwargs):
                self._build_params(**kwargs)

        handler = TestHandler(fuzzy="Black Lotus", set="lea")
        assert handler._query_params["fuzzy"] == "Black Lotus"
        assert handler._query_params["set"] == "lea"

    def test_params_are_url_encoded(self):
        """Test that parameters are URL encoded."""

        class TestHandler(ScrythonRequestHandler):
            def __init__(self, **kwargs):
                self._build_params(**kwargs)

        handler = TestHandler(q="type:instant color:red")
        # Check that the encoded params string is created
        assert "q=" in handler._encoded_query_params
        # URL encoding converts spaces to +
        assert (
            "type%3Ainstant+color%3Ared" in handler._encoded_query_params
            or "type:instant+color:red" in handler._encoded_query_params
        )


class TestRequestHandlerFetch:
    """Test the _fetch functionality and full request flow."""

    def test_successful_fetch(self, mock_urlopen, sample_card):
        """Test successful API request."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        assert handler.scryfall_data.name == "Black Lotus"
        assert handler.scryfall_data.object == "card"
        assert len(mock_urlopen.calls) == 1
        assert "api.scryfall.com" in mock_urlopen.calls[0]["url"]

    def test_fetch_with_error_response_raises_scryfall_error(self, mock_urlopen):
        """Test that error responses raise ScryfallError."""
        mock_urlopen.set_error_response(
            {
                "status": 404,
                "code": "not_found",
                "details": "No card found",
                "type": None,
                "warnings": None,
            }
        )

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        with pytest.raises(ScryfallError) as exc_info:
            TestHandler(fuzzy="Nonexistent Card")

        assert exc_info.value.status == 404
        assert exc_info.value.code == "not_found"
        assert exc_info.value.details == "No card found"

    def test_request_headers(self, mock_urlopen, sample_card):
        """Test that correct headers are sent with requests."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        _handler = TestHandler(fuzzy="Black Lotus")

        # Check that the request was made
        assert len(mock_urlopen.calls) == 1
        call = mock_urlopen.calls[0]

        # Headers should include User-Agent, Accept, Content-Type
        # Note: Python's urllib uses 'User-agent' (lowercase 'a')
        assert "User-agent" in call["headers"]
        assert "Scrython" in call["headers"]["User-agent"]

    def test_endpoint_property(self, mock_urlopen, sample_card):
        """Test that endpoint property returns the built endpoint."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")
        assert handler.endpoint == "cards/named"


class TestScryfallDataReadOnly:
    """Test that scryfall_data is read-only via SimpleNamespace."""

    def test_scryfall_data_returns_simplenamespace(self, mock_urlopen, sample_card):
        """Test that scryfall_data returns a SimpleNamespace object."""
        import types

        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        # Check that scryfall_data is a SimpleNamespace
        assert isinstance(handler.scryfall_data, types.SimpleNamespace)

    def test_scryfall_data_dot_notation_access(self, mock_urlopen, sample_card):
        """Test that scryfall_data allows dot-notation access."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        # Dot notation should work
        assert handler.scryfall_data.name == "Black Lotus"
        assert handler.scryfall_data.object == "card"

    def test_scryfall_data_mutations_dont_affect_internal_data(self, mock_urlopen, sample_card):
        """Test that mutations to scryfall_data don't affect internal data."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        # Get original value
        original_name = handler.scryfall_data.name

        # Try to mutate (this creates a new attribute on the SimpleNamespace)
        handler.scryfall_data.name = "Modified Name"

        # Internal data should be unchanged - accessing scryfall_data again
        # should return a fresh SimpleNamespace from the cached internal data
        assert handler._scryfall_data["name"] == original_name
        assert handler._scryfall_data["name"] == "Black Lotus"

    def test_scryfall_data_caching(self, mock_urlopen, sample_card):
        """Test that scryfall_data property is cached."""
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Black Lotus")

        # Get scryfall_data twice
        first_access = handler.scryfall_data
        second_access = handler.scryfall_data

        # Should return the same cached object
        assert first_access is second_access

    def test_scryfall_data_nested_objects(self, mock_urlopen):
        """Test that nested dictionaries are converted to SimpleNamespace."""
        mock_urlopen.set_response(
            data={
                "object": "card",
                "name": "Test Card",
                "image_uris": {
                    "small": "https://example.com/small.jpg",
                    "normal": "https://example.com/normal.jpg",
                },
            }
        )

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Test Card")

        # Nested objects should also be SimpleNamespace
        import types

        assert isinstance(handler.scryfall_data.image_uris, types.SimpleNamespace)
        assert handler.scryfall_data.image_uris.small == "https://example.com/small.jpg"
        assert handler.scryfall_data.image_uris.normal == "https://example.com/normal.jpg"

    def test_scryfall_data_with_lists(self, mock_urlopen):
        """Test that lists within scryfall_data are handled correctly."""
        mock_urlopen.set_response(
            data={
                "object": "card",
                "name": "Test Card",
                "colors": ["R", "G"],
                "keywords": ["Flying", "Trample"],
            }
        )

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        handler = TestHandler(fuzzy="Test Card")

        # Lists should remain as lists
        assert isinstance(handler.scryfall_data.colors, list)
        assert handler.scryfall_data.colors == ["R", "G"]
        assert handler.scryfall_data.keywords == ["Flying", "Trample"]
