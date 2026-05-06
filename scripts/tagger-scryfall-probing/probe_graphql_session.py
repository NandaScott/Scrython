#!/usr/bin/env python3
"""
Final attempt: use a persistent session (cookie jar + opener) to:
1. GET the HTML page (gets session cookie + CSRF meta tag)
2. POST to /graphql with the SAME session cookie AND CSRF token

The meta tags say: csrf-param=authenticity_token, csrf-token=<value>
So the token should be sent as a form parameter: authenticity_token=<value>
"""

import gzip
import json
import re
import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar
import time

BASE = "https://tagger.scryfall.com"
CARD_URL = f"{BASE}/card/sos/170"
GRAPHQL_URL = f"{BASE}/graphql"

ORACLE_ID = "2f5f46ed-b8aa-4864-bd20-17281d4632bf"
PRINTING_ID = "77285d12-e658-4eb3-ba13-ff202afab9c8"

# ── Persistent session ────────────────────────────────────────────────

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

AGENT = "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)"

def session_get(url: str, accept: str = "text/html,application/json,*/*"):
    headers = {
        "User-Agent": AGENT,
        "Accept": accept,
        "Accept-Encoding": "gzip, deflate",
    }
    req = urllib.request.Request(url, headers=headers)
    resp = opener.open(req, timeout=15)
    raw = resp.read()
    try:
        raw = gzip.decompress(raw)
    except Exception:
        pass
    return resp.getcode(), dict(resp.headers), raw.decode("utf-8", errors="replace")

def session_post(url: str, data: bytes, extra_headers: dict | None = None):
    headers = {
        "User-Agent": AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        resp = opener.open(req, timeout=15)
        raw = resp.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        return resp.getcode(), dict(resp.headers), raw.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        return e.code, dict(e.headers), raw.decode("utf-8", errors="replace")


print("=" * 70)
print("STEP 1: GET HTML to establish session + get CSRF token")
print("=" * 70)

code, headers, html = session_get(CARD_URL)
print(f"  Status: {code}")
print(f"  HTML size: {len(html):,} chars")

# Extract CSRF token
csrf_token = re.findall(r'<meta[^>]+name="csrf-token"[^>]+content="([^"]+)"', html)
csrf_param = re.findall(r'<meta[^>]+name="csrf-param"[^>]+content="([^"]+)"', html)
print(f"  CSRF param: {csrf_param}")
print(f"  CSRF token: {csrf_token[0][:50] if csrf_token else 'NONE'}...")

# Print cookies
print(f"\n  Session cookies:")
for cookie in cj:
    print(f"    {cookie.name} = {cookie.value[:60]}...")

# ── STEP 2: Try POST with various CSRF approaches ─────────────────────
print(f"\n{'='*70}")
print("STEP 2: GraphQL POST with persistent session")
print("=" * 70)

query = "{ __typename }"
payload = json.dumps({"query": query}).encode("utf-8")

# Approach A: X-CSRF-Token header (standard Rails + JS pattern)
if csrf_token:
    print(f"\n  [A] Sending X-CSRF-Token header...")
    code, headers, text = session_post(GRAPHQL_URL, payload, {"X-CSRF-Token": csrf_token[0]})
    print(f"  Status: {code}")
    print(f"  Response: {text[:400]}")

# Approach B: authenticity_token as query parameter? No - that's for forms
# Approach C: Send as application/x-www-form-urlencoded with authenticity_token
if csrf_token:
    print(f"\n  [C] Sending as URL-encoded form with authenticity_token...")
    import urllib.parse
    form_data = urllib.parse.urlencode({
        "query": query,
        csrf_param[0]: csrf_token[0],
    }).encode("utf-8")
    form_code, form_headers, form_text = session_post(GRAPHQL_URL, form_data, 
        {"Content-Type": "application/x-www-form-urlencoded"})
    print(f"  Status: {form_code}")
    print(f"  Response: {form_text[:400]}")

# Approach D: Send CSRF in URL query string + POST body
if csrf_token:
    print(f"\n  [D] CSRF as URL parameter...")
    url_with_csrf = f"{GRAPHQL_URL}?{csrf_param[0]}={urllib.parse.quote(csrf_token[0])}"
    headers = {
        "User-Agent": AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url_with_csrf, data=payload, headers=headers, method="POST")
    try:
        resp = opener.open(req, timeout=15)
        raw = resp.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        text = raw.decode("utf-8", errors="replace")
        print(f"  Status: {resp.getcode()}")
        print(f"  Response: {text[:400]}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        print(f"  Status: {e.code}")
        print(f"  Response: {raw.decode('utf-8', errors='replace')[:400]}")

# Approach E: Try without JSON Content-Type (Rails may expect form data)
print(f"\n  [E] POST without CSRF, with x-www-form-urlencoded...")
form_data = urllib.parse.urlencode({"query": query}).encode("utf-8")
form_code2, form_headers2, form_text2 = session_post(GRAPHQL_URL, form_data,
    {"Content-Type": "application/x-www-form-urlencoded"})
print(f"  Status: {form_code2}")
print(f"  Response: {form_text2[:400]}")

# Approach F: Try the GraphQL introspection query specifically  
# Maybe basic queries require auth but introspection is open?
if csrf_token:
    print(f"\n  [F] Introspection with X-CSRF-Token...")
    introspect = """
    query {
      __schema { queryType { name } }
    }
    """
    payload2 = json.dumps({"query": introspect}).encode("utf-8")
    code, headers, text = session_post(GRAPHQL_URL, payload2, {"X-CSRF-Token": csrf_token[0]})
    print(f"  Status: {code}")
    print(f"  Response: {text[:500]}")

# Step 3: Look at the HTML more carefully for the actual data
# The inline <script> tag had edgeDefs — maybe the card data is embedded too
print(f"\n{'='*70}")
print("STEP 3: Search HTML for embedded tag data")
print("=" * 70)

# Extract all <script> tag contents (not src=)
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for i, script in enumerate(scripts):
    if len(script) > 100:
        print(f"\n  Script block #{i}: {len(script):,} chars")
        # Try to parse as JSON
        try:
            data = json.loads(script.strip())
            print(f"  [JSON!] keys: {list(data.keys())}")
            for k, v in data.items():
                if isinstance(v, list):
                    print(f"    {k}: list[{len(v)}]")
                elif isinstance(v, dict):
                    print(f"    {k}: {list(v.keys())[:10]}")
                else:
                    print(f"    {k}: {str(v)[:80]}")
        except (json.JSONDecodeError, ValueError):
            print(f"  First 200 chars: {script.strip()[:200]}")

# Look for any JSON data island in the HTML
json_islands = re.findall(r'window\[["\']([^"\']+)["\']\]\s*=\s*({.*?});\s*</script>', html, re.DOTALL)
print(f"\n  window[key] JSON islands: {len(json_islands)}")
for key, data_str in json_islands:
    print(f"  window['{key}']")

# Check if the <div id="app"> has data attributes
data_divs = re.findall(r'<div[^>]+data-([^=]+)="([^"]*)"', html)
print(f"\n  data- attributes on divs:")
for key, val in data_divs[:20]:
    print(f"    {key}: {val[:80]}")

print(f"\n{'='*70}")
print("Session-based probing complete.")
print("=" * 70)