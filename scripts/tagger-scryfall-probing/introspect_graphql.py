#!/usr/bin/env python3
"""
Full GraphQL introspection of the tagger.scryfall.com API.
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

# ── Session + CSRF setup ─────────────────────────────────────────────

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
AGENT = "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)"

def get_session_and_csrf():
    headers = {
        "User-Agent": AGENT,
        "Accept": "text/html,application/json,*/*",
        "Accept-Encoding": "gzip, deflate",
    }
    req = urllib.request.Request(CARD_URL, headers=headers)
    resp = opener.open(req, timeout=15)
    raw = resp.read()
    try:
        raw = gzip.decompress(raw)
    except Exception:
        pass
    html = raw.decode("utf-8", errors="replace")
    csrf = re.findall(r'<meta[^>]+name="csrf-token"[^>]+content="([^"]+)"', html)
    return html, csrf[0] if csrf else None

def graphql(query: str, variables: dict | None = None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    headers = {
        "User-Agent": AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "X-CSRF-Token": csrf_token,
    }
    req = urllib.request.Request(GRAPHQL_URL, data=payload, headers=headers, method="POST")
    try:
        resp = opener.open(req, timeout=15)
        raw = resp.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        return json.loads(raw.decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        print(f"  HTTP {e.code}: {raw.decode('utf-8', errors='replace')[:300]}")
        return None

print("=" * 70)
print("Establishing session...")
html, csrf_token = get_session_and_csrf()
print(f"CSRF token: {csrf_token[:40] if csrf_token else 'NONE'}...")

# ── Full introspection ───────────────────────────────────────────────

print("\nFULL INTROSPECTION")
print("=" * 70)

introspection = """
fragment FullType on __Type {
  kind
  name
  fields(includeDeprecated: true) {
    name
    args { name type { name kind ofType { name kind } } }
    type { name kind ofType { name kind } }
    isDeprecated
    deprecationReason
  }
  inputFields { name type { name kind } }
  enumValues { name }
}

query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    types {
      ...FullType
    }
  }
}
"""

result = graphql(introspection)
if result and "data" in result:
    schema = result["data"]["__schema"]
    print(f"Query type: {schema['queryType']['name']}")
    print(f"Mutation type: {schema.get('mutationType', {}).get('name', 'NONE')}")
    
    types = schema.get("types", [])
    print(f"\nTotal types: {len(types)}")
    
    # Filter to interesting types (not __TypeKind, __InputValue, etc.)
    interesting = [t for t in types if not t["name"].startswith("__") and t.get("fields")]
    print(f"Types with fields: {len(interesting)}")
    
    for t in interesting:
        name = t["name"]
        kind = t["kind"]
        fields = t.get("fields") or []
        field_names = [f["name"] for f in fields]
        field_str = ", ".join(field_names[:15])
        if len(field_names) > 15:
            field_str += f", ... (+{len(field_names) - 15})"
        print(f"\n  {name} ({kind}): {field_str}")
        for f in fields[:20]:
            args = [f"{a['name']}: {a['type'].get('name', '?')}" for a in f.get("args", [])]
            type_str = f["type"].get("name") or f["type"].get("ofType", {}).get("name", "?")
            arg_str = f"({', '.join(args)})" if args else ""
            print(f"    {f['name']}{arg_str}: {type_str}")

    # Also show enum types
    enums = [t for t in types if t["kind"] == "ENUM" and not t["name"].startswith("__")]
    print(f"\n\nEnum types:")
    for e in enums:
        print(f"  {e['name']}: {e.get('enumValues', [])}")
else:
    print(f"Introspection failed: {result}")

# ── Primary query: card tags ─────────────────────────────────────────

print(f"\n{'='*70}")
print("PRIMARY ENDPOINT: oracleCard (card tags)")
print("=" * 70)

card_query = """
query($oracleId: ID!) {
  oracleCard(oracleId: $oracleId) {
    name
    tags {
      tag { name category tagType }
      count
    }
    edges {
      edge { classifier label type }
      target { name }
    }
  }
}
"""
result = graphql(card_query, {"oracleId": ORACLE_ID})
if result and "data" in result:
    print(json.dumps(result["data"], indent=2))
else:
    print(f"Failed: {result}")

# Try the 'tag' query field (from schema)
print(f"\n{'='*70}")
print("Try: tag field query")
print("=" * 70)

tag_query = """
{
  tag(name: "removal", category: "function") {
    name
    category
    tagType
    count
    cards(first: 3) {
      edges {
        node { name set collectorNumber }
      }
    }
  }
}
"""
result = graphql(tag_query)
if result:
    if "errors" in result:
        for err in result.get("errors", []):
            print(f"  Error: {err.get('message', '')[:200]}")
    if "data" in result:
        print(json.dumps(result["data"], indent=2)[:2000])

# Try tagCategory query
print(f"\n{'='*70}")
print("Try: tagCategories query")
print("=" * 70)

cat_query = """
{
  tagCategories {
    name
    label
    tags(first: 3) {
      edges {
        node { name count }
      }
    }
  }
}
"""
result = graphql(cat_query)
if result:
    if "errors" in result:
        for err in result.get("errors", []):
            print(f"  Error: {err.get('message', '')[:200]}")
    if "data" in result:
        print(json.dumps(result["data"], indent=2)[:2000])

print(f"\n{'='*70}")
print("Discovery complete!")
print("=" * 70)