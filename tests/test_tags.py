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

        assert tag.id == "b7c19924-b4bf-492b-9c98-1e9b0f6e4d3a"
        assert tag.slug == "removal"
        assert tag.label == "Removal"
        assert tag.uri == "https://api.scryfall.com/cards/oracle-tag/removal"
        assert tag.type == "oracle"
        assert tag.description.startswith("Cards that destroy")

    def test_nullable_list_accessors(self):
        """Nullable list accessors return their values when present."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))

        assert tag.parent_ids == ["a1111111-1111-1111-1111-111111111111"]
        assert tag.child_ids == [
            "c2222222-2222-2222-2222-222222222222",
            "d3333333-3333-3333-3333-333333333333",
        ]
        assert tag.aliases == ["interaction", "answers"]

    def test_absent_nullable_fields_return_none(self):
        """Nullable fields return None when absent rather than raising."""
        tag = scrython.tags.Object(load_fixture("art_tag.json"))

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
        assert len(tag.taggings) == 2

    def test_oracle_tagging_shape(self):
        """Oracle taggings expose oracle_id; illustration_id is None."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))
        tagging = tag.taggings[0]

        assert tagging.object == "tagging"
        assert tagging.oracle_id == "f2b9983e-20d4-4d12-9e2c-ec6d9a345787"
        assert tagging.illustration_id is None
        assert tagging.weight == "strong"
        assert tagging.annotation == "Doom Blade destroys a nonblack creature."

    def test_art_tagging_shape(self):
        """Art taggings expose illustration_id; oracle_id is None."""
        tag = scrython.tags.Object(load_fixture("art_tag.json"))
        tagging = tag.taggings[0]

        assert tagging.illustration_id == "9c1f0a2b-5678-4d12-9e2c-ec6d9a345789"
        assert tagging.oracle_id is None
        assert tagging.weight == "median"

    def test_absent_tagging_annotation_returns_none(self):
        """A tagging without an annotation returns None rather than raising."""
        tag = scrython.tags.Object(load_fixture("oracle_tag.json"))
        tagging = tag.taggings[1]

        assert tagging.weight == "very_strong"
        assert tagging.annotation is None
