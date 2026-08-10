"""Usage tests for list helper methods: as_dict, filter, and map."""

import scrython.cards

# Four cards pinned across two sets: Counterspell and Lightning Bolt from LEA,
# Fireball and Giant Growth from M10.
_QUERY = (
    '(name:"Counterspell" or name:"Lightning Bolt") s:lea'
    ' or (name:"Fireball" or name:"Giant Growth") s:m10'
)


def test_search__as_dict__keyed_by_name_is_addressable(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    by_name = results.as_dict("name")
    assert by_name["Lightning Bolt"].name == "Lightning Bolt"
    assert by_name["Counterspell"].name == "Counterspell"


def test_search__as_dict__keyed_by_id_round_trips(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    by_id = results.as_dict("card_id")
    assert len(by_id) == len(results.data)
    for card_id, card in by_id.items():
        assert card.card_id == card_id


def test_search__filter__by_set_returns_only_matching_cards(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    lea_cards = results.filter(lambda card: card.set == "lea")
    assert len(lea_cards) > 0
    assert all(card.set == "lea" for card in lea_cards)


def test_search__filter__empty_result_returns_empty_list(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    no_cards = results.filter(lambda card: card.set == "thb")
    assert no_cards == []


def test_search__map__to_names(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    names = results.map(lambda card: card.name)
    assert "Lightning Bolt" in names
    assert "Counterspell" in names
    assert len(names) == len(results.data)


def test_search__map__to_name_set_tuples(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    tuples = results.map(lambda card: (card.name, card.set))
    assert ("Lightning Bolt", "lea") in tuples
    assert ("Fireball", "m10") in tuples


def test_search__chain__filter_by_set_then_map_to_names(cards_search__multiset):
    results = scrython.cards.Search(q=_QUERY, order="name", unique="prints")
    lea_names = list(map(lambda card: card.name, results.filter(lambda card: card.set == "lea")))
    assert "Lightning Bolt" in lea_names
    assert "Counterspell" in lea_names
    assert not any(card.set != "lea" for card in results.filter(lambda card: card.set == "lea"))
