#!/usr/bin/env python3
"""
Probe the tagger.scryfall.com GraphQL endpoint.
Found via: JS bundle references /graphql

Tests:
1. Introspection query (to discover schema)
2. Common tag queries derived from edgeDefs structure
3. Card tag lookup by oracleId and printingId
"""

import gzip
import json
import time
import urllib.error
import urllib.request

BASE = "https://tagger.scryfall.com"
GRAPHQL_URL = f"{BASE}/graphql"

# Card data from Scryfall API (sos/170 = Abigale, Poet Laureate)
ORACLE_ID = "2f5f46ed-b8aa-4864-bd20-17281d4632bf"
PRINTING_ID = "77285d12-e658-4eb3-ba13-ff202afab9c8"
ILLUSTRATION_ID = "c1f8e669-60d0-4e66-b85a-07dafb9782a9"


def graphql_query(query: str, variables: dict | None = None, label: str = ""):
    """Execute a GraphQL query against the tagger endpoint."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")

    headers = {
        "User-Agent": "Scrython/2.0 TaggerDiscovery (https://github.com/NandaScott/Scrython)",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    req = urllib.request.Request(GRAPHQL_URL, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass
            text = raw.decode("utf-8", errors="replace")
            code = resp.getcode()
            ct = resp.headers.get("Content-Type", "")

            print(f"\n{'='*60}")
            print(f"QUERY: {label}")
            print(f"  Status: {code} | Content-Type: {ct}")

            try:
                data = json.loads(text)
                if "errors" in data:
                    print("  [ERRORS]:")
                    for err in data.get("errors", [])[:3]:
                        print(f"    {err.get('message', str(err))[:200]}")
                if "data" in data and data["data"] is not None:
                    print("  [DATA]:")
                    print(json.dumps(data["data"], indent=2)[:2000])
                return data
            except json.JSONDecodeError:
                print(f"  [RAW] (not JSON): {text[:500]}")
                return None

    except urllib.error.HTTPError as e:
        print(f"\n{'='*60}")
        print(f"QUERY: {label}")
        print(f"  [HTTP {e.code}]")
        try:
            err_body = e.read()
            print(f"  Body: {err_body.decode('utf-8', errors='replace')[:500]}")
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"\n  [ERR] {label}: {e}")
        return None


# ── Introspection ─────────────────────────────────────────────────────

print("=" * 70)
print("PROBING GRAPHQL ENDPOINT")
print("=" * 70)

# 1. Basic introspection
introspection_query = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    types {
      name
      kind
    }
  }
}
"""
graphql_query(introspection_query, label="Full Introspection")

# 2. Just query type fields (less data)
query_type_query = """
{
  __type(name: "Query") {
    name
    fields {
      name
      args { name type { name kind } }
      type { name kind ofType { name kind } }
    }
  }
}
"""
graphql_query(query_type_query, label="Query type fields")

# 3. Try simpler queries first - just see if endpoint responds
simple_query = """
{ __typename }
"""
graphql_query(simple_query, label="Simple __typename")

# ── Domain queries based on edgeDefs ───────────────────────────────────

# Try queries matching the edgeDefs structure we found in the HTML
# edgeDefs had: ORACLE_CARD_TAG, PRINTING_TAG, ILLUSTRATION_TAG, various RELATIONSHIP types

# 4. Try: oracleCardTag query
queries_to_try = [
    (
        "oracleCardTag by oracleId",
        """
        query($oracleId: ID!) {
          oracleCardTag(oracleId: $oracleId) {
            name
            count
          }
        }
        """,
        {"oracleId": ORACLE_ID},
    ),
    (
        "oracleCardTags by oracleId",
        """
        query($oracleId: ID!) {
          oracleCardTags(oracleId: $oracleId) {
            name
            count
          }
        }
        """,
        {"oracleId": ORACLE_ID},
    ),
    (
        "printingTag by printingId",
        """
        query($printingId: ID!) {
          printingTag(printingId: $printingId) {
            name
            count
          }
        }
        """,
        {"printingId": PRINTING_ID},
    ),
    (
        "printingTags by printingId",
        """
        query($printingId: ID!) {
          printingTags(printingId: $printingId) {
            name
            count
          }
        }
        """,
        {"printingId": PRINTING_ID},
    ),
    (
        "card by set+number",
        """
        query($set: String!, $number: String!) {
          card(set: $set, number: $number) {
            name
            oracleId
            printingId
            tags { name category count }
            edges { classifier target { name } }
          }
        }
        """,
        {"set": "sos", "number": "170"},
    ),
    (
        "cardTags",
        """
        query($oracleId: ID!) {
          cardTags(oracleId: $oracleId) {
            name
            category
            tagType
            count
          }
        }
        """,
        {"oracleId": ORACLE_ID},
    ),
    (
        "tags",
        """
        {
          tags {
            name
            category
          }
        }
        """,
        None,
    ),
    (
        "tagCategories",
        """
        {
          tagCategories {
            name
            label
          }
        }
        """,
        None,
    ),
    (
        "oracleCard edges",
        """
        query($oracleId: ID!) {
          oracleCard(oracleId: $oracleId) {
            name
            tags { name category }
            edges { classifier label }
          }
        }
        """,
        {"oracleId": ORACLE_ID},
    ),
    (
        "oracleCard",
        """
        query($oracleId: ID!) {
          oracleCard(oracleId: $oracleId) {
            name
          }
        }
        """,
        {"oracleId": ORACLE_ID},
    ),
    (
        "printing",
        """
        query($printingId: ID!) {
          printing(printingId: $printingId) {
            name set collectorNumber
          }
        }
        """,
        {"printingId": PRINTING_ID},
    ),
    (
        "allOracleCards (paginated)",
        """
        query($first: Int) {
          allOracleCards(first: $first) {
            edges {
              node {
                name
              }
            }
          }
        }
        """,
        {"first": 3},
    ),
    (
        "search by tag",
        """
        query($category: String!, $tag: String!) {
          taggedCards(category: $category, tag: $tag) {
            name
            set
            collectorNumber
          }
        }
        """,
        {"category": "function", "tag": "removal"},
    ),
]

for label, query, variables in queries_to_try:
    graphql_query(query, variables, label)
    time.sleep(0.3)

# ── Also try non-POST variations ──────────────────────────────────────
print(f"\n{'='*70}")
print("TRYING GET REQUESTS TO /graphql")
print("=" * 70)

get_url = f"{GRAPHQL_URL}?query={{__typename}}"
headers = {
    "User-Agent": "Scrython/2.0 TaggerDiscovery",
    "Accept": "application/json",
}
req = urllib.request.Request(get_url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(f"  Status: {resp.getcode()}")
        print(f"  Content-Type: {resp.headers.get('Content-Type')}")
        data = resp.read().decode("utf-8", errors="replace")
        print(f"  Body: {data[:500]}")
except urllib.error.HTTPError as e:
    print(f"  Status: {e.code}")
    print(f"  Body: {e.read().decode('utf-8', errors='replace')[:500]}")
except Exception as e:
    print(f"  ERR: {e}")

print(f"\n{'='*70}")
print("GraphQL probing complete.")
print("=" * 70)
