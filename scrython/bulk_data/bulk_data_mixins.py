from typing import Any


class BulkDataObjectMixin:
    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        """
        A content type for this object, always bulk_data.

        Type: String (Required)
        """
        return "bulk_data"

    @property
    def id(self) -> str:
        """
        A unique ID for this bulk item.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def uri(self) -> str:
        """
        The Scryfall API URI for this file.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]

    @property
    def type(self) -> str:
        """
        A computer-readable string for the kind of bulk item.

        Type: String (Required)
        """
        return self._scryfall_data["type"]

    @property
    def name(self) -> str:
        """
        A human-readable name for this file.

        Type: String (Required)
        """
        return self._scryfall_data["name"]

    @property
    def description(self) -> str:
        """
        A human-readable description for this file.

        Type: String (Required)
        """
        return self._scryfall_data["description"]

    @property
    def download_uri(self) -> str:
        """
        The URI that hosts this bulk file for fetching.

        Type: URI (Required)

        Note: Files are compressed with gzip. Download and decompress to process.
        """
        return self._scryfall_data["download_uri"]

    @property
    def updated_at(self) -> str:
        """
        The time when this file was last updated.

        Type: Timestamp (Required)

        Note: Bulk data files are updated approximately every 12 hours.
        """
        return self._scryfall_data["updated_at"]

    @property
    def size(self) -> int:
        """
        The size of this file in integer bytes.

        Type: Integer (Required)
        """
        return self._scryfall_data["size"]

    @property
    def content_type(self) -> str:
        """
        The MIME type of this file.

        Type: String (Required)
        """
        return self._scryfall_data["content_type"]

    @property
    def content_encoding(self) -> str:
        """
        The Content-Encoding encoding that will be used to transmit this file when you download it.

        Type: String (Required)
        """
        return self._scryfall_data["content_encoding"]
