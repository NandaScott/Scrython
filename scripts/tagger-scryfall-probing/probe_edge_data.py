#!/usr/bin/env python3
"""Probe Edge data to find where tag names live."""

import sys

sys.path.insert(0, ".")

from scrython.tagger.tagger_graphql import TaggerSession

TaggerSession.reset()

# Query with __typename to see what concrete types edges return
query1 = """
query($set: String!, $number: String!) {
  cardBySet(set: $set, number: $number) {
    name
    edges {
      __typename
      classifier
      type
      name
      namespace
      relatedName
      ... on Tagging {
        tagId: relatedId
        preferredPrintingId
      }
    }
  }
}
"""
print("=== Query 1: __typename + Tagging fragment ===")
result = TaggerSession.execute_graphql(query1, {"set": "sos", "number": "170"})
card = result.get("cardBySet", {})
for edge in card.get("edges", []):
    print(edge)
    print()

# Query 2: Try including tag as a nested object
query2 = """
query($set: String!, $number: String!) {
  cardBySet(set: $set, number: $number) {
    name
    edges {
      __typename
      classifier
      type
      name
      namespace
      relatedName
      ... on Tagging {
        tag {
          name
          description
        }
      }
    }
  }
}
"""
print("=== Query 2: Tagging { tag { name } } ===")
try:
    result2 = TaggerSession.execute_graphql(query2, {"set": "sos", "number": "170"})
    card2 = result2.get("cardBySet", {})
    for edge in card2.get("edges", [])[:3]:
        print(edge)
        print()
except Exception as e:
    print(f"Error: {e}")

# Query 3: Try getting tag by ID separately
# First get a relatedId, then query tag
edge_ids = card.get("edges", [])
if edge_ids:
    first_id = edge_ids[0].get("tagId")
    print(f"\n=== Query 3: tag(id: {first_id}) ===")
    if first_id:
        query3 = """
        query($id: ID!) {
          tag(id: $id) {
            name
            namespace
            description
          }
        }
        """
        result3 = TaggerSession.execute_graphql(query3, {"id": first_id})
        print(result3)

# Query 4: Try the 'card' or 'revisable' query to get taggings
# The Tagging type has 'name' which might be the tag name
query4 = """
query($oracleId: ID!) {
  revisable(id: $oracleId, type: ORACLE_CARD_TAG) {
    __typename
    name
    ... on Tagging {
      id
      name
      namespace
      metadata
    }
  }
}
"""
card_oracle = card.get("oracleId")
print("\n=== Query 4: revisable ===")
# Don't know the oracleId from edges query, get from card data

print(f"\nCard data keys: {list(card.keys())}")
