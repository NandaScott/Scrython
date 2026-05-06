#!/usr/bin/env python3
"""
Discovery script for tagger.scryfall.com.

Probes various URL patterns to determine:
- Response format (JSON vs HTML)
- Tag data model structure
- Available listing/browse endpoints

Uses only urllib from stdlib -- no dependencies.
Run: python scripts/discover_tagger.py
"""

import gzip
import json
import urllib.error
import urllib.request
import time
from html.parser import HTMLParser

BASE = "https://tagger.scryfall.com"

# -- HTML Content Extractor --------------------------------------------------

class HTMLTextExtractor(HTMLParser):
    """Extracts visible text content and tag attributes from HTML."""
    def __init__(self):
        super().__init__()
        self.text_lines: list[str] = []
        self.tag_counts: dict[str, int] = {}
        self.current_tag = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        self.current_tag = tag

    def handle_data(self, data: str):
        text = data.strip()
        if text:
            self.text_lines.append(f"  [{self.current_tag}] {text}")

# -- HTTP Fetcher ------------------------------------------------------------

def fetch(url: str, accept_json: bool = False, timeout: int = 15
          ) -> tuple[int, str, str, bytes | None]:
    """
    Fetch a URL and return (status_code, content_type, effective_url, raw_body).
    raw_body may be gzip-compressed; caller should decompress if needed.
    """
    headers = {
        "User-Agent": "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)",
        "Accept-Encoding": "gzip, deflate",
    }
    if accept_json:
        headers["Accept"] = "application/json"
    else:
        headers["Accept"] = "text/html, application/json, */*"

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            content_type = resp.headers.get("Content-Type", "unknown")
            final_url = resp.geturl()
            code = resp.getcode()
            return code, content_type, final_url, raw
    except urllib.error.HTTPError as e:
        try:
            raw_err = e.read()
        except Exception:
            raw_err = b""
        return e.code, e.headers.get("Content-Type", "unknown"), e.geturl(), raw_err
    except Exception as e:
        return 0, str(e), url, None


def decompress(data: bytes) -> bytes:
    """Decompress gzip data if needed."""
    if data is None:
        return b""
    try:
        return gzip.decompress(data)
    except Exception:
        return data


# -- Analyzers ---------------------------------------------------------------

def analyze_html(html: str, label: str) -> dict:
    """Parse HTML and extract structural information."""
    extractor = HTMLTextExtractor()
    extractor.feed(html)

    result = {
        "label": label,
        "size_bytes": len(html),
        "tag_counts": dict(extractor.tag_counts),
        "sample_text": extractor.text_lines[:40],
        "text_line_count": len(extractor.text_lines),
    }

    # Look for key structural elements
    key_elements = {}
    for el in ["table", "ul", "ol", "li", "a", "span", "div", "section", "nav", "main"]:
        key_elements[el] = extractor.tag_counts.get(el, 0)
    result["key_elements"] = key_elements

    # Check for specific patterns
    lower = html.lower()
    result["has_tag_keyword"] = "tag" in lower
    result["has_card_name_pattern"] = "card" in lower
    result["has_json_ld"] = 'application/ld+json' in lower

    return result


def analyze_response(status: int, content_type: str, final_url: str,
                     raw: bytes | None, label: str):
    """Print a formatted analysis of a response."""
    print(f"\n{'='*70}")
    print(f"URL: {label}")
    print(f"  Status: {status}")
    print(f"  Content-Type: {content_type}")
    print(f"  Final URL: {final_url}")

    if raw is None:
        print("  [ERR] No response body")
        return None

    decoded = decompress(raw)
    text = decoded.decode("utf-8", errors="replace")

    print(f"  Raw size: {len(raw):,} bytes | Decompressed: {len(decoded):,} bytes")

    is_json = ("application/json" in content_type
               or text.strip().startswith("{"))
    is_html = ("text/html" in content_type
               or text.strip().startswith("<!")
               or text.strip().startswith("<html"))

    if is_json:
        try:
            data = json.loads(text)
            print(f"  [JSON] parsed successfully")
            top_keys = list(data.keys()) if isinstance(data, dict) else "list"
            print(f"  Top-level keys: {top_keys}")
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        print(f"    {k}: list[{len(v)}]")
                        if v and len(v) <= 3:
                            for item in v:
                                if isinstance(item, dict):
                                    snippet = json.dumps(item, indent=6)
                                    print(f"      {snippet[:300]}")
                                else:
                                    print(f"      {item}")
                    elif isinstance(v, dict):
                        print(f"    {k}: dict keys={list(v.keys())[:10]}")
                    else:
                        val_str = str(v)[:100]
                        print(f"    {k}: {val_str}")
            return data
        except json.JSONDecodeError as e:
            print(f"  [WARN] Content looks like JSON but failed to parse: {e}")
            print(f"  First 200 chars: {text[:200]}")

    elif is_html:
        analysis = analyze_html(text, label)
        print(f"  [HTML] page | {analysis['text_line_count']} text lines")
        print(f"  Key elements: {analysis['key_elements']}")
        print(f"  Has 'tag' keyword: {analysis['has_tag_keyword']}")
        print(f"  Has 'card' keyword: {analysis['has_card_name_pattern']}")
        print(f"  Has JSON-LD: {analysis['has_json_ld']}")
        if analysis["sample_text"]:
            limit = min(25, len(analysis["sample_text"]))
            print(f"\n  First {limit} text items:")
            for line in analysis["sample_text"][:limit]:
                print(f"    {line}")
        return analysis

    else:
        print(f"  [WARN] Unknown content type. First 300 chars:")
        print(f"  {text[:300]}")
        return None


# -- Main Discovery ----------------------------------------------------------

def main():
    print("=" * 70)
    print("Scryfall Tagger Discovery Script")
    print("=" * 70)

    results = {}

    # -- Primary: Known card URL pattern --
    card_urls = [
        ("/card/sos/170 (known card page)", f"{BASE}/card/sos/170", False),
        ("/card/sos/170 + Accept:json", f"{BASE}/card/sos/170", True),
        ("/card/sos/170.json", f"{BASE}/card/sos/170.json", False),
        ("/api/card/sos/170", f"{BASE}/api/card/sos/170", False),
        ("/api/card/sos/170.json", f"{BASE}/api/card/sos/170.json", False),
        ("/api/card/sos/170 + Accept:json", f"{BASE}/api/card/sos/170", True),
    ]

    for label, url, accept_json in card_urls:
        status, ct, final, raw = fetch(url, accept_json=accept_json)
        result = analyze_response(status, ct, final, raw, label)
        results[label] = result
        time.sleep(0.5)  # Be polite

    # -- Secondary: Browse/listing pages --
    list_urls = [
        ("/tags (tag index)", f"{BASE}/tags", False),
        ("/tags.json", f"{BASE}/tags.json", False),
        ("/tags + Accept:json", f"{BASE}/tags", True),
        ("/tag (singular)", f"{BASE}/tag", False),
        ("/tag/function (category browse)", f"{BASE}/tag/function", False),
        ("/tag/function + Accept:json", f"{BASE}/tag/function", True),
        ("/tag/function/removal (specific tag)", f"{BASE}/tag/function/removal", False),
        ("/api/tags", f"{BASE}/api/tags", False),
        ("/api/tags + Accept:json", f"{BASE}/api/tags", True),
        ("/tag/function/removal.json", f"{BASE}/tag/function/removal.json", False),
        ("/tags/function (plural)", f"{BASE}/tags/function", False),
        ("/tags/function/removal (plural)", f"{BASE}/tags/function/removal", False),
    ]

    for label, url, accept_json in list_urls:
        status, ct, final, raw = fetch(url, accept_json=accept_json)
        result = analyze_response(status, ct, final, raw, label)
        results[label] = result
        time.sleep(0.5)

    # -- Summary --
    print(f"\n\n{'='*70}")
    print("DISCOVERY SUMMARY")
    print("=" * 70)

    json_endpoints = []
    html_card_endpoints = []
    html_list_endpoints = []
    errors = []

    for label, result in results.items():
        if result is None:
            errors.append(label)
        elif isinstance(result, dict) and "key_elements" not in result:
            # It's a parsed JSON dict (not an HTML analysis dict)
            json_endpoints.append(label)
        elif isinstance(result, dict) and "key_elements" in result:
            if "/card/" in label:
                html_card_endpoints.append(label)
            else:
                html_list_endpoints.append(label)
        else:
            html_list_endpoints.append(label)

    print(f"\n[JSON] endpoints found: {len(json_endpoints)}")
    for ep in json_endpoints:
        print(f"   - {ep}")

    print(f"\n[HTML] card pages: {len(html_card_endpoints)}")
    for ep in html_card_endpoints:
        print(f"   - {ep}")

    print(f"\n[HTML] list/catalog pages: {len(html_list_endpoints)}")
    for ep in html_list_endpoints:
        print(f"   - {ep}")

    print(f"\n[ERR] Failed requests: {len(errors)}")
    for ep in errors:
        print(f"   - {ep}")

    print(f"\n{'='*70}")
    print("Discovery complete. Use results to inform implementation.")
    print("=" * 70)


if __name__ == "__main__":
    main()