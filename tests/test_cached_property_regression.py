"""Regression tests for issue #230: functools.cache replaced with cached_property."""

import gc
import weakref

from scrython.base_mixins import ScryfallListMixin
from scrython.cards.cards import Object


class _ConcreteList(ScryfallListMixin):
    list_data_type = None

    def __init__(self, data):
        self._scryfall_data = data


def _make_object(uid, card_faces=None, all_parts=None):
    data = {
        "object": "card",
        "id": uid,
        "name": "Test Card",
        "layout": "normal",
        "lang": "en",
    }
    if card_faces is not None:
        data["card_faces"] = card_faces
    if all_parts is not None:
        data["all_parts"] = all_parts
    return Object(data)


class TestWeakrefGC:
    def test_list_mixin_data_instance_is_collected(self):
        obj = _ConcreteList({"data": [1, 2], "has_more": False})
        ref = weakref.ref(obj)
        _ = obj.data
        del obj
        gc.collect()
        assert ref() is None

    def test_list_mixin_unread_instance_is_collected(self):
        obj = _ConcreteList({"data": [1], "has_more": False})
        ref = weakref.ref(obj)
        del obj
        gc.collect()
        assert ref() is None

    def test_card_faces_instance_is_collected(self):
        obj = _make_object(
            "gc-test", card_faces=[{"name": "A", "object": "card_face", "mana_cost": ""}]
        )
        ref = weakref.ref(obj)
        _ = obj.card_faces
        del obj
        gc.collect()
        assert ref() is None

    def test_all_parts_instance_is_collected(self):
        obj = _make_object(
            "gc-test-2",
            all_parts=[
                {
                    "id": "x",
                    "object": "related_card",
                    "component": "token",
                    "name": "T",
                    "type_line": "Token",
                    "uri": "u",
                }
            ],
        )
        ref = weakref.ref(obj)
        _ = obj.all_parts
        del obj
        gc.collect()
        assert ref() is None


class TestNoIDCrossContamination:
    """Two distinct objects with the same Scryfall ID must not share cached values."""

    def test_card_faces_same_id_different_data(self):
        first = _make_object(
            "shared-id",
            card_faces=[
                {"name": "Front", "object": "card_face", "mana_cost": "{1}"},
                {"name": "Back", "object": "card_face", "mana_cost": ""},
            ],
        )
        second = _make_object("shared-id")  # same id, genuinely has no card_faces

        assert first.card_faces is not None
        assert [f._scryfall_data["name"] for f in first.card_faces] == ["Front", "Back"]

        assert second.card_faces is None

    def test_card_faces_faceless_first(self):
        first = _make_object("shared-id-2")  # no card_faces
        second = _make_object(
            "shared-id-2",
            card_faces=[{"name": "Alpha", "object": "card_face", "mana_cost": ""}],
        )

        assert first.card_faces is None
        assert second.card_faces is not None
        assert second.card_faces[0]._scryfall_data["name"] == "Alpha"

    def test_all_parts_same_id_different_data(self):
        related = [
            {
                "id": "r1",
                "object": "related_card",
                "component": "token",
                "name": "T",
                "type_line": "Token",
                "uri": "u",
            }
        ]
        first = _make_object("all-parts-id", all_parts=related)
        second = _make_object("all-parts-id")  # same id, no all_parts

        assert first.all_parts is not None
        assert first.all_parts[0]._scryfall_data["name"] == "T"
        assert second.all_parts is None

    def test_list_data_same_hash_objects(self):
        obj1 = _ConcreteList({"data": [10, 20], "has_more": False})
        obj2 = _ConcreteList({"data": [30], "has_more": False})
        assert obj1.data == [10, 20]
        assert obj2.data == [30]


class TestRepeatedAccessIdentity:
    """Repeated access on one instance returns the identical object."""

    def test_card_faces_repeated_access_same_object(self):
        obj = _make_object(
            "repeat-id",
            card_faces=[{"name": "X", "object": "card_face", "mana_cost": ""}],
        )
        first_access = obj.card_faces
        second_access = obj.card_faces
        assert first_access is second_access

    def test_all_parts_repeated_access_same_object(self):
        related = [
            {
                "id": "rr",
                "object": "related_card",
                "component": "token",
                "name": "N",
                "type_line": "Token",
                "uri": "u",
            }
        ]
        obj = _make_object("repeat-all-parts", all_parts=related)
        assert obj.all_parts is obj.all_parts

    def test_list_data_repeated_access_same_object(self):
        obj = _ConcreteList({"data": [1, 2, 3], "has_more": False})
        first_access = obj.data
        second_access = obj.data
        assert first_access is second_access
