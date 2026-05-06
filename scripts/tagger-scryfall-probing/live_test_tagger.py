#!/usr/bin/env python3
"""
Live integration test for the Scrython tagger module.
Tests CardTags against the actual tagger.scryfall.com API.
"""

import sys

sys.path.insert(0, ".")

from scrython.tagger import CardTags, TaggerSession

print("=" * 60)
print("Scrython Tagger — Live Integration Test")
print("=" * 60)

# Reset session state for clean test
TaggerSession.reset()

# Test 1: CardTags for Abigale, Poet Laureate (sos/170)
print("\n[Test 1] CardTags(code='sos', number='170')")
try:
    tags = CardTags(code="sos", number="170")
    print(f"  Card: {tags.card_name}")
    print(f"  Oracle ID: {tags.oracle_id}")
    print(f"  Printing ID: {tags.printing_id}")
    print(f"  Total edges: {len(tags.tags) + len(tags.relationships)}")
    print(f"  Tags: {len(tags.tags)}")
    print(f"  Relationships: {len(tags.relationships)}")

    if tags.tags:
        print("\n  All tags:")
        for tag in tags.tags:
            print(f"    [{tag.classifier}] {tag.name} ({tag.namespace or 'no namespace'})")

    if tags.oracle_tags:
        print(f"\n  Oracle card tags: {[t.name for t in tags.oracle_tags]}")
    if tags.printing_tags:
        print(f"  Printing tags: {[t.name for t in tags.printing_tags]}")
    if tags.illustration_tags:
        print(f"  Illustration tags: {[t.name for t in tags.illustration_tags]}")
    if tags.relationships:
        print("\n  Relationships:")
        for rel in tags.relationships:
            print(f"    [{rel.classifier}] {rel.name}")

    print("\n  [PASS] CardTags works correctly")
except Exception as e:
    print(f"\n  [FAIL] {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()

# Test 2: CardTags for Lightning Bolt (lea/??) — using a well-known card
# Lightning Bolt in Alpha (LEA) is collector number 155
print("\n[Test 2] CardTags(code='lea', number='155') — Lightning Bolt (Alpha)")
try:
    bolt_tags = CardTags(code="lea", number="155")
    name = bolt_tags.card_name or "(unknown)"
    tag_count = len(bolt_tags.tags)
    print(f"  Card: {name}")
    print(f"  Tags: {tag_count}")
    print(f"  Tag names: {bolt_tags.tag_names[:10]}")
    if bolt_tags.has_tag("burn"):
        print("  This card has the 'burn' tag!")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {type(e).__name__}: {e}")

# Test 3: Test TagObject
print("\n[Test 3] TagObject functionality")
if tags and tags.tags:
    tag = tags.tags[0]
    print(f"  repr: {repr(tag)}")
    print(f"  str: {str(tag)}")
    print(f"  is_tag: {tag.is_tag}")
    print(f"  is_oracle_tag: {tag.is_oracle_tag}")
    print(f"  is_printing_tag: {tag.is_printing_tag}")
    print(f"  is_illustration_tag: {tag.is_illustration_tag}")
    print(f"  to_dict: {tag.to_dict()}")
    print("  [PASS]")
else:
    print("  [SKIP] No tags available")

# Test 4: has_tag helper
print("\n[Test 4] has_tag helper")
if tags and tags.tags:
    first_tag_name = tags.tags[0].name
    result = tags.has_tag(first_tag_name)
    print(f"  has_tag('{first_tag_name}'): {result}")
    assert result is True, f"has_tag should return True for '{first_tag_name}'"
    print(f"  has_tag('nonexistent_tag_xyz'): {tags.has_tag('nonexistent_tag_xyz')}")
    print("  [PASS]")
else:
    print("  [SKIP] No tags available")

# Test 5: tags_by_namespace
print("\n[Test 5] tags_by_namespace")
if tags and tags.tags:
    namespaces = set(t.namespace for t in tags.tags if t.namespace)
    print(f"  Available namespaces: {namespaces}")
    if namespaces:
        first_ns = next(iter(namespaces))
        ns_tags = tags.tags_by_namespace(first_ns)
        print(f"  Tags in '{first_ns}': {[t.name for t in ns_tags]}")
    print("  [PASS]")
else:
    print("  [SKIP] No tags available")

# Test 6: Rate limiting
print("\n[Test 6] Rate limiting")
try:
    tags2 = CardTags(code="lea", number="155", rate_limit_per_second=2.0)
    print(f"  Card (rate limited): {tags2.card_name}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# Test 7: Rate limiting disabled
print("\n[Test 7] Rate limiting disabled")
try:
    tags3 = CardTags(code="lea", number="155", rate_limit=False)
    print(f"  Card (unlimited): {tags3.card_name}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

print(f"\n{'=' * 60}")
print("Live test complete!")
print("=" * 60)
