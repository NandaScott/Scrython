import gzip
import io
import json
from typing import Any
from urllib.request import Request, urlopen

from ..base import ScrythonRequestHandler
from ..types import ScryfallBulkDataData


class BulkDataObjectMixin:
    _scryfall_data: ScryfallBulkDataData

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
    def jsonl_download_uri(self) -> str:
        """
        The URI to download this bulk file in gzip-compressed JSONL format.

        Type: URI (Required)
        """
        return self._scryfall_data["jsonl_download_uri"]

    @property
    def compressed_size(self) -> int:
        """
        The size of the compressed file in integer bytes.

        Type: Integer (Required)
        """
        return self._scryfall_data["compressed_size"]

    @property
    def updated_at(self) -> str:
        """
        The time when this file was last updated.

        Type: Timestamp (Required)

        Note: Bulk data files are updated approximately every 12 hours.
        """
        return self._scryfall_data["updated_at"]

    def download(
        self,
        filepath: str | None = None,
        return_data: bool = True,
        chunk_size: int = 8192,
        progress: bool = False,
    ) -> list[dict[str, Any]] | None:
        """
        Download and parse the bulk JSONL file from Scryfall.

        Scryfall documents jsonl_download_uri as hosting this bulk file as
        .jsonl.gz, so the response body is always a gzip file. It is decompressed
        and parsed one line at a time, and each line is a separate JSON object.

        Args:
            filepath: Optional path to save the parsed data as a JSON file.
                     If None, file is not saved to disk.
            return_data: If True, return parsed data. If False and
                        filepath is provided, only saves file without returning data.
                        Default: True.
            chunk_size: Read size in bytes for the progress bar. Ignored when
                       progress is False. Default: 8192.
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
        if progress:
            try:
                from tqdm.auto import tqdm
            except ImportError as exc:
                raise ImportError(
                    "tqdm is required for progress bars. "
                    "Install with: pip install scrython[progress] or pip install tqdm"
                ) from exc

        request = Request(self.jsonl_download_uri)
        request.add_header("User-Agent", ScrythonRequestHandler._user_agent)

        with urlopen(request) as response:
            if progress:
                pbar = tqdm(
                    total=self.compressed_size, unit="B", unit_scale=True, desc="Downloading"
                )
                chunks = []
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    pbar.update(len(chunk))
                pbar.close()
                compressed_stream: Any = io.BytesIO(b"".join(chunks))
            else:
                compressed_stream = response

            # Parse JSONL: each non-empty line is a separate JSON object.
            with gzip.GzipFile(fileobj=compressed_stream) as jsonl_stream:
                parsed_data: list[dict[str, Any]] = [
                    json.loads(line) for line in jsonl_stream if line.strip()
                ]

        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=2)

        return parsed_data if return_data else None
