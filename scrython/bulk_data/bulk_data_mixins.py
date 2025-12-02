import gzip
import json
from typing import Any
from urllib.request import urlopen


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

        Note: Files may be compressed with gzip depending on CDN/proxy configuration.
        The download() method automatically detects encoding from HTTP headers.
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

    def download(
        self,
        filepath: str | None = None,
        return_data: bool = True,
        chunk_size: int = 8192,
        progress: bool = False,
    ) -> list[dict[str, Any]] | None:
        """
        Download and parse bulk data file from Scryfall.

        The bulk data file is downloaded from Scryfall's CDN. The method automatically
        detects if the response is gzip-compressed by checking HTTP Content-Encoding
        headers and handles decompression accordingly. The JSON data is then parsed
        and optionally saved to a file.

        Args:
            filepath: Optional path to save the decompressed JSON file.
                     If None, file is not saved to disk.
            return_data: If True, return parsed JSON data. If False and
                        filepath is provided, only saves file without returning data.
                        Default: True.
            chunk_size: Download chunk size in bytes. Default: 8192.
            progress: If True, display a progress bar during download (requires tqdm).
                     Default: False.

        Returns:
            List of card/set objects if return_data=True, otherwise None.

        Raises:
            Exception: If download fails or file is invalid.
            ImportError: If progress=True but tqdm is not installed.

        Example:
            >>> from scrython.bulk_data import ByType
            >>> bulk = ByType(type='oracle_cards')
            >>> cards = bulk.download()
            >>> print(f"Downloaded {len(cards)} cards")

            >>> # Or save to file
            >>> bulk.download(filepath='oracle_cards.json', return_data=False)

            >>> # With progress bar
            >>> cards = bulk.download(progress=True)

        Note:
            Bulk data files can be very large (100+ MB compressed, 500+ MB uncompressed).
            Be mindful of memory usage when loading entire files into memory.
        """
        download_url = self.download_uri

        # Optional progress bar
        if progress:
            try:
                from tqdm import tqdm
            except ImportError as exc:
                raise ImportError(
                    "tqdm is required for progress bars. "
                    "Install with: pip install scrython[progress] or pip install tqdm"
                ) from exc

            # Download with progress bar
            with urlopen(download_url) as response:
                # Check actual HTTP Content-Encoding header
                content_encoding = response.info().get("Content-Encoding", "").lower()

                total_size = int(response.headers.get("Content-Length", 0))
                pbar = tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading")

                # Read in chunks
                chunks = []
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    pbar.update(len(chunk))
                pbar.close()

                downloaded_data = b"".join(chunks)

            # Conditionally decompress based on HTTP header
            if content_encoding == "gzip":
                with tqdm(
                    total=len(downloaded_data), unit="B", unit_scale=True, desc="Decompressing"
                ):
                    data = gzip.decompress(downloaded_data)
            else:
                # Already decompressed or plain JSON
                data = downloaded_data
        else:
            # Download without progress bar
            with urlopen(download_url) as response:
                # Check actual HTTP Content-Encoding header
                content_encoding = response.info().get("Content-Encoding", "").lower()

                if content_encoding == "gzip":
                    # Decompress with streaming
                    with gzip.GzipFile(fileobj=response) as gz_file:
                        data = gz_file.read()
                else:
                    # Read plain JSON
                    data = response.read()

        # Parse JSON
        parsed_data = json.loads(data.decode("utf-8"))

        # Save to file if requested
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=2)

        # Return data if requested
        return parsed_data if return_data else None
