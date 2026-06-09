"""Tests for scrython.tags module."""

import json
from pathlib import Path

import scrython

FIXTURES = Path(__file__).parent / "fixtures" / "tags"


def load_fixture(name: str) -> dict:
    with open(FIXTURES / name) as f:
        return json.load(f)


class TestTagObject:
    """Test the Tag Object wrapper."""

    def test_shallow_import(self):
        """scrython.tags.Object is reachable without a deep import."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))
        assert tag.object == "tag"

    def test_scalar_accessors(self):
        """Tag accessors return expected scalar values for a bulk tag dict."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))

        assert tag.id == "5bf7154a-2814-4329-a310-4a1343ee3850"
        assert tag.slug == "bottom-deck-manipulation"
        assert tag.label == "bottom deck manipulation"
        assert tag.uri == "https://tagger.scryfall.com/tags/card/bottom-deck-manipulation"
        assert tag.type == "oracle"

    def test_hierarchy_accessors(self):
        """parent_ids, child_ids, and aliases return their values."""
        tag = scrython.tags.Object(load_fixture("art_tag.json"))

        assert tag.parent_ids == [
            "504aea75-b144-4530-b014-3e3c7a1fd283",
            "7b155ecc-bd5e-4757-bde2-c029b6978bad",
            "b8ad94e6-a042-49ff-bf9e-b963ade6e176",
            "b88f1b22-c601-4e52-ae99-1fc602c65534",
        ]
        assert tag.child_ids == []
        assert tag.aliases == ["mirri (cat)"]
        assert tag.description == "Sami's cat."

    def test_null_description_returns_none(self):
        """A tag whose description is null returns None rather than the literal null."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))

        assert tag.description is None

    def test_absent_nullable_fields_return_none(self):
        """Nullable fields return None when the key is absent rather than raising."""
        tag = scrython.tags.Object({"taggings": []})

        assert tag.description is None
        assert tag.parent_ids is None
        assert tag.child_ids is None
        assert tag.aliases is None


class TestTaggings:
    """Test the nested Tagging wrapper."""

    def test_taggings_returns_tagging_list(self):
        """tag.taggings resolves into a list of Tagging objects."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))

        assert isinstance(tag.taggings, list)
        assert all(isinstance(t, scrython.tags.Tagging) for t in tag.taggings)
        assert len(tag.taggings) == 4

    def test_taggings_always_a_list_when_absent(self):
        """taggings is a required field; it returns [] when missing, never None."""
        tag = scrython.tags.Object({})

        assert tag.taggings == []

    def test_oracle_tagging_shape(self):
        """Oracle taggings expose oracle_id; illustration_id is None."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))
        tagging = tag.taggings[0]

        assert tagging.oracle_id == "97024e8e-dfde-4769-bc27-c3d6fad19e7c"
        assert tagging.illustration_id is None
        assert tagging.weight == "median"
        assert tagging.annotation.startswith("If you play this with a deck")

    def test_art_tagging_shape(self):
        """Art taggings expose illustration_id; oracle_id is None."""
        tag = scrython.tags.Object(load_fixture("art_tag.json"))
        tagging = tag.taggings[0]

        assert tagging.illustration_id == "d7a21c80-7157-4965-b6d0-d1f6ba0aec33"
        assert tagging.oracle_id is None
        assert tagging.weight == "median"

    def test_absent_tagging_annotation_returns_none(self):
        """A tagging without an annotation returns None rather than raising."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))
        tagging = tag.taggings[1]

        assert tagging.weight == "median"
        assert tagging.annotation is None
