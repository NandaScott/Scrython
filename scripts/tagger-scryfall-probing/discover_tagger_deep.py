#!/usr/bin/env python3
"""
Deep discovery: probe the API endpoints that the tagger SPA calls.

Based on edgeDefs found in the HTML <script> tag:
  ORACLE_CARD_TAG  -> foreign_key: oracleId
  PRINTING_TAG     -> foreign_key: printingId  
  ILLUSTRATION_TAG -> foreign_key: illustrationId
  Various RELATIONSHIP types -> foreign_key: oracleId or illustrationId

This script probes likely API paths the JavaScript frontend calls.
"""

import gzip
import json
import re
import urllib.error
import urllib.request
import time

BASE = "https://tagger.scryfall.com"

# Known: card page for sos/170 works and includes a <script> with edgeDefs
# The edgeDefs suggest API calls fetch by oracleId, printingId, or illustrationId

# First, get the full HTML to extract any API URLs embedded in scripts
def fetch_raw(url: str) -> bytes | None:
    headers = {
        "User-Agent": "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html, */*",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        print(f"  ERR: {e}")
        return None

def decompress(data: bytes) -> bytes:
    if data is None:
        return b""
    try:
        return gzip.decompress(data)
    except Exception:
        return data

def fetch_as_text(url: str) -> str:
    raw = fetch_raw(url)
    if raw is None:
        return ""
    return decompress(raw).decode("utf-8", errors="replace")

# Step 1: Get the full HTML and extract JS source URLs
print("=" * 70)
print("STEP 1: Extract JS source files from HTML")
print("=" * 70)

html = fetch_as_text(f"{BASE}/card/sos/170")
print(f"HTML size: {len(html):,} chars")

# Extract <script src="..."> URLs
script_srcs = re.findall(r'<script[^>]*src="([^"]+)"', html)
print(f"\nScript source URLs found: {len(script_srcs)}")
for src in script_srcs:
    full_url = src if src.startswith("http") else f"https://tagger.scryfall.com{src}"
    print(f"  {full_url}")

# Extract any fetch/XMLHttpRequest API paths from inline scripts
inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
api_urls_in_js = []
for script in inline_scripts:
    # Look for API paths
    api_urls_in_js.extend(re.findall(r'["\'](/[a-z][a-z0-9_/-]*[a-z0-9])["\']', script))
    # Look for fetch() calls
    api_urls_in_js.extend(re.findall(r'fetch\(["\']([^"\']+)["\']', script))
    # Look for axios / ajax calls
    api_urls_in_js.extend(re.findall(r'url:\s*["\']([^"\']+)["\']', script))

print(f"\nPotential API URLs found in inline scripts: {len(api_urls_in_js)}")
for u in sorted(set(api_urls_in_js)):
    if "/api" in u or "/tag" in u or "/edge" in u or "/card" in u:
        print(f"  {u}")

# Step 2: Probe API paths based on edgeDefs patterns
print(f"\n{'='*70}")
print("STEP 2: Probe derived API paths")
print("=" * 70)

# Card sos/170 = Abigale, Poet Laureate
# We need the oracleId and printingId for this card
# Scryfall API gives us the card data with oracle_id
print("\nFetching card data from Scryfall API to get oracle_id and illustration_id...")
sf_url = "https://api.scryfall.com/cards/sos/170"
sf_headers = {
    "User-Agent": "Scrython/2.0 (https://github.com/NandaScott/Scrython)",
    "Accept": "application/json",
}
req = urllib.request.Request(sf_url, headers=sf_headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    card_data = json.loads(resp.read().decode("utf-8"))

oracle_id = card_data.get("oracle_id", "unknown")
card_id = card_data.get("id", "unknown")
illustration_id = card_data.get("illustration_id", "unknown")
name = card_data.get("name", "unknown")
print(f"  Card: {name}")
print(f"  oracle_id: {oracle_id}")
print(f"  scryfall_id (printingId): {card_id}")
print(f"  illustration_id: {illustration_id}")

# Probe API endpoints with these IDs
probes = []

# Pattern: GET /api/tags?oracleId=...  (from ORACLE_CARD_TAG)
probes.append((f"/api/tags?oracleId={oracle_id}", f"{BASE}/api/tags?oracleId={oracle_id}"))
probes.append((f"/api/tags?printingId={card_id}", f"{BASE}/api/tags?printingId={card_id}"))
probes.append((f"/api/tags?illustrationId={illustration_id}", f"{BASE}/api/tags?illustrationId={illustration_id}"))

# Pattern: GET /api/edges?oracleId=...
probes.append((f"/api/edges?oracleId={oracle_id}", f"{BASE}/api/edges?oracleId={oracle_id}"))
probes.append((f"/api/edges?printingId={card_id}", f"{BASE}/api/edges?printingId={card_id}"))

# Pattern: GET /api/oracle_cards/:id/tags
probes.append((f"/api/oracle_cards/{oracle_id}/tags", f"{BASE}/api/oracle_cards/{oracle_id}/tags"))
probes.append((f"/api/printings/{card_id}/tags", f"{BASE}/api/printings/{card_id}/tags"))
probes.append((f"/api/illustrations/{illustration_id}/tags", f"{BASE}/api/illustrations/{illustration_id}/tags"))

# Pattern: GET /api/taggings?...
probes.append((f"/api/taggings?oracleId={oracle_id}", f"{BASE}/api/taggings?oracleId={oracle_id}"))
probes.append((f"/api/taggings?printingId={card_id}", f"{BASE}/api/taggings?printingId={card_id}"))

# Pattern: RESTful
probes.append((f"/api/tags/oracle/{oracle_id}", f"{BASE}/api/tags/oracle/{oracle_id}"))
probes.append((f"/api/tags/printing/{card_id}", f"{BASE}/api/tags/printing/{card_id}"))
probes.append((f"/api/tags/illustration/{illustration_id}", f"{BASE}/api/tags/illustration/{illustration_id}"))

# Pattern: GraphQL
probes.append((f"/api/graphql (POST probe)", "skip"))  # Can't probe with GET

# Try json suffix on base card endpoint (already tried but with IDs)
probes.append((f"/card/sos/170?format=json", f"{BASE}/card/sos/170?format=json"))
probes.append((f"/api/cards/{card_id}", f"{BASE}/api/cards/{card_id}"))
probes.append((f"/api/cards/{oracle_id}/taggings", f"{BASE}/api/cards/{oracle_id}/taggings"))

# Combined query params from edgeDefs  
probes.append((f"/api/search?type=ORACLE_CARD_TAG&oracleId={oracle_id}", 
               f"{BASE}/api/search?type=ORACLE_CARD_TAG&oracleId={oracle_id}"))

print(f"\nProbing {len(probes)} API endpoints...\n")

for label, url in probes:
    if url == "skip":
        print(f"  SKIP: {label}")
        continue
    
    headers = {
        "User-Agent": "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            try:
                decoded = gzip.decompress(raw)
            except Exception:
                decoded = raw
            text = decoded.decode("utf-8", errors="replace")
            
            ct = resp.headers.get("Content-Type", "")
            code = resp.getcode()
            
            if "application/json" in ct or text.strip().startswith("{"):
                try:
                    data = json.loads(text)
                    if isinstance(data, dict) and data.get("error"):
                        print(f"  [404/json] {label}")
                    else:
                        print(f"  [200/JSON!] {label} -> keys: {list(data.keys()) if isinstance(data, dict) else f'list[{len(data)}]'}")
                        if isinstance(data, dict):
                            for k, v in list(data.items())[:5]:
                                if isinstance(v, list):
                                    print(f"    {k}: list[{len(v)}]")
                                elif isinstance(v, dict):
                                    print(f"    {k}: {list(v.keys())[:10]}")
                                else:
                                    print(f"    {k}: {str(v)[:80]}")
                except json.JSONDecodeError:
                    print(f"  [{code}] {label} -> {text[:80]}")
            else:
                # HTML response
                if code == 200:
                    print(f"  [200/HTML] {label} -> {len(text):,} chars")
                else:
                    print(f"  [{code}] {label}")
                    
    except urllib.error.HTTPError as e:
        print(f"  [{e.code}] {label}")
    except Exception as e:
        print(f"  [ERR] {label}: {e}")
    
    time.sleep(0.3)

# Step 3: Also check if the JS bundles reference API paths
print(f"\n{'='*70}")
print("STEP 3: Check JS bundles for API paths")
print("=" * 70)

for src in script_srcs[:3]:  # Only check first 3 to save time
    full_url = src if src.startswith("http") else f"https://tagger.scryfall.com{src}"
    print(f"\nFetching: {full_url}")
    js = fetch_as_text(full_url)
    if not js:
        print("  EMPTY")
        continue
    print(f"  Size: {len(js):,} chars")
    
    # Search for API paths in JS
    api_matches = set()
    for pattern in [r'fetch\(["\']([^"\']+)["\']', 
                    r'["\']([/]api[^"\']+)["\']',
                    r'["\']([/]edge[^"\']+)["\']',
                    r'["`](https?://[^"`]+tags[^"`]*)["`]']:
        for m in re.findall(pattern, js, re.IGNORECASE):
            api_matches.add(m)
    
    if api_matches:
        print(f"  Found {len(api_matches)} potential API references:")
        for m in sorted(api_matches)[:20]:
            print(f"    {m[:120]}")
    else:
        print("  No API paths found")

print(f"\n{'='*70}")
print("Deep discovery complete.")
print("=" * 70)