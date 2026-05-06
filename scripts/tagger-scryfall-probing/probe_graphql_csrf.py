#!/usr/bin/env python3
"""
Probe the GraphQL endpoint with CSRF token extracted from the HTML page.
The endpoint returns 422 "invalid authenticity token" — we need to:
1. GET the card HTML page, extract CSRF token from <meta> tag
2. POST to /graphql with the CSRF token in headers
"""

import gzip
import http.cookiejar
import json
import re
import time
import urllib.error
import urllib.request

BASE = "https://tagger.scryfall.com"
CARD_URL = f"{BASE}/card/sos/170"
GRAPHQL_URL = f"{BASE}/graphql"

ORACLE_ID = "2f5f46ed-b8aa-4864-bd20-17281d4632bf"
PRINTING_ID = "77285d12-e658-4eb3-ba13-ff202afab9c8"


def fetch_with_cookies(
    url: str, method: str = "GET", data: bytes | None = None, extra_headers: dict | None = None
):
    """Fetch URL, tracking cookies and returning (response, cookies, html_text)."""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    headers = {
        "User-Agent": "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)",
        "Accept": "text/html,application/json,*/*",
        "Accept-Encoding": "gzip, deflate",
    }
    if extra_headers:
        headers.update(extra_headers)

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        resp = opener.open(req, timeout=15)
        raw = resp.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        text = raw.decode("utf-8", errors="replace")
        return resp.getcode(), dict(resp.headers), text, cj
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        text = raw.decode("utf-8", errors="replace")
        return e.code, dict(e.headers), text, cj
    except Exception as e:
        return 0, {}, str(e), cj


print("=" * 70)
print("STEP 1: Fetch card HTML page to get CSRF token")
print("=" * 70)

code, resp_headers, html, cj = fetch_with_cookies(CARD_URL)
print(f"  Status: {code}")
print(f"  HTML size: {len(html):,} chars")
print(f"  Set-Cookie: {resp_headers.get('Set-Cookie', 'NONE')[:200]}")

# Extract CSRF token from meta tags
csrf_meta = re.findall(r'<meta[^>]+name="csrf-[^"]*"[^>]+content="([^"]+)"', html)
print(f"\n  CSRF meta tags found: {len(csrf_meta)}")
for m in csrf_meta:
    print(f"    {m[:80]}")

# Also check all meta tags
all_metas = re.findall(r'<meta[^>]+name="([^"]+)"[^>]+content="([^"]+)"', html)
print("\n  All meta tags:")
for name, content in all_metas[:20]:
    print(f"    {name}: {content[:80]}")

# Extract CSRF token from cookies
print("\n  Cookies in jar:")
csrf_from_cookie = None
for cookie in cj:
    print(f"    {cookie.name}: {cookie.value[:50] if cookie.value else 'N/A'}")
    if "csrf" in cookie.name.lower():
        csrf_from_cookie = cookie.value

# CSRF token could be in header or meta or JS variable
csrf_in_js = re.findall(r'csrf[_-]?token["\s:=]+["\']([^"\']+)["\']', html, re.IGNORECASE)
print(f"\n  CSRF in JS: {csrf_in_js[:5]}")

csrf_in_headers_meta = re.findall(r'<meta[^>]+name="csrf-token"[^>]+content="([^"]+)"', html)
csrf_in_param_meta = re.findall(r'<meta[^>]+name="csrf-param"[^>]+content="([^"]+)"', html)

print(f"\n  CSRF token meta: {csrf_in_headers_meta}")
print(f"  CSRF param meta: {csrf_in_param_meta}")

# Collect all possible CSRF tokens
csrf_tokens = set()
for t in csrf_in_headers_meta:
    csrf_tokens.add(t)
for t in csrf_in_js:
    csrf_tokens.add(t)
if csrf_from_cookie:
    csrf_tokens.add(csrf_from_cookie)

print(f"\n  Unique CSRF candidates: {len(csrf_tokens)}")

# Also try to find X-CSRF-Token in a script tag
# Rails typically puts it in <meta name="csrf-token">
# But this app might be using a different mechanism

# Let's check the Rails authenticity_token pattern
auth_tokens = re.findall(r'authenticity_token["\s:=]+["\']([^"\']+)["\']', html)
print(f"\n  authenticity_token in HTML: {auth_tokens[:3]}")

# Also look for the token in the application JS
# The JS bundle path from the HTML
app_js_match = re.findall(r"application-[A-Za-z0-9]+\.js", html)
if app_js_match:
    js_url = f"{BASE}/vite/assets/{app_js_match[0]}"
    print("\n  Fetching JS bundle to find CSRF token handling...")
    js_code, _, js_text, _ = fetch_with_cookies(js_url)
    csrf_in_bundle = set(
        re.findall(r'csrf[_-]?token["\s:=]+["\']([^"\']+)["\']', js_text, re.IGNORECASE)
    )
    # Actually, look for how the CSRF is fetched — commonly from a meta tag
    csrf_meta_read = re.findall(r"csrf-token[^}]+content", js_text[:50000])
    print(f"  CSRF references in JS bundle: {len(csrf_in_bundle)}")
    for c in csrf_in_bundle:
        print(f"    {c[:80]}")
    if csrf_meta_read:
        print(f"  CSRF meta read patterns: {csrf_meta_read[:5]}")

    # Also check for header names
    csrf_headers_in_js = set(re.findall(r'["\'](X-[Cc][Ss][Rr][Ff][^"\']+)["\']', js_text))
    print(f"  CSRF header names in JS: {csrf_headers_in_js}")

# ── STEP 2: Try POST with CSRF token ──────────────────────────────────
print(f"\n{'='*70}")
print("STEP 2: Try GraphQL POST with CSRF tokens")
print("=" * 70)

# Try each CSRF candidate
for csrf_token in csrf_tokens:
    if not csrf_token:
        continue
    print(f"\n  Trying CSRF token: {csrf_token[:30]}...")

    query = "{ __typename }"
    payload = json.dumps({"query": query}).encode("utf-8")

    extra_headers = {
        "X-CSRF-Token": csrf_token,
        "Content-Type": "application/json",
    }

    code, resp, text, _ = fetch_with_cookies(
        GRAPHQL_URL, method="POST", data=payload, extra_headers=extra_headers
    )

    print(f"  Status: {code}")
    print(f"  Response: {text[:300]}")

    if "data" in text or "errors" in text:
        print("  *** SUCCESS! GraphQL responded! ***")
        try:
            data = json.loads(text)
            print(json.dumps(data, indent=2)[:1000])
        except Exception:
            pass
        break

    time.sleep(0.3)

# Also try with the cookies from the HTML page (session-based auth)
print("\n  Trying without explicit CSRF header (session cookie only)...")
payload = json.dumps({"query": "{ __typename }"}).encode("utf-8")
code, resp, text, _ = fetch_with_cookies(
    GRAPHQL_URL, method="POST", data=payload, extra_headers={"Content-Type": "application/json"}
)
print(f"  Status: {code}")
print(f"  Response: {text[:300]}")

print(f"\n{'='*70}")
print("CSRF probing complete.")
print("=" * 70)
