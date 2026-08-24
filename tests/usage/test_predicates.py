"""Usage tests for card classification convenience methods: legality, color, and type predicates."""

import scrython.cards

# ---------- is_legal_in ----------


def test_named__is_legal_in__returns_true_for_legal_format(cards_named__lightning_bolt):
    card = scrython.cards.Named(exact="Lightning Bolt")
    assert card.is_legal_in("commander") is True


def test_named__is_legal_in__returns_false_when_banned(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.is_legal_in("commander") is False


def test_named__is_legal_in__case_insensitive(cards_named__lightning_bolt):
    card = scrython.cards.Named(exact="Lightning Bolt")
    assert card.is_legal_in("COMMANDER") is True
    assert card.is_legal_in("Commander") is True
    assert card.is_legal_in("commander") is True


# ---------- has_color ----------


def test_named__has_color__mono_color_matches_its_color(cards_named__lightning_bolt):
    card = scrython.cards.Named(exact="Lightning Bolt")
    assert card.has_color("R") is True


def test_named__has_color__mono_color_does_not_match_other_colors(cards_named__lightning_bolt):
    card = scrython.cards.Named(exact="Lightning Bolt")
    assert card.has_color("U") is False


def test_named__has_color__multi_color_matches_all_its_colors(cards_named__niv_mizzet_parun):
    card = scrython.cards.Named(exact="Niv-Mizzet, Parun")
    assert card.has_color("U") is True
    assert card.has_color("R") is True


def test_named__has_color__multi_color_does_not_match_absent_color(cards_named__niv_mizzet_parun):
    card = scrython.cards.Named(exact="Niv-Mizzet, Parun")
    assert card.has_color("G") is False


def test_named__has_color__colorless_card_has_no_colors(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.has_color("W") is False
    assert card.has_color("U") is False
    assert card.has_color("B") is False
    assert card.has_color("R") is False
    assert card.has_color("G") is False


# ---------- type predicates ----------
#
# These six own the sweep's coverage of the is_* accessors: they are computed
# from type_line, so no fixture key exists for the property sweep to assert
# against, and CARD_COVERED_ELSEWHERE in tests/sweep/test_property_sweep.py
# names each of them by node id. Renaming one, or moving its accessor read into
# a helper, reddens tests/sweep/test_sweep_engine_self.py. See CONVENTIONS.md #7.


def test_named__is_creature__returns_true(cards_named__serra_angel):
    card = scrython.cards.Named(exact="Serra Angel")
    assert card.is_creature is True


def test_named__is_instant__returns_true(cards_named__lightning_bolt):
    card = scrython.cards.Named(exact="Lightning Bolt")
    assert card.is_instant is True


def test_named__is_sorcery__returns_true(cards_named__wrath_of_god):
    card = scrython.cards.Named(exact="Wrath of God")
    assert card.is_sorcery is True


def test_named__is_enchantment__returns_true(cards_named__oblivion_ring):
    card = scrython.cards.Named(exact="Oblivion Ring")
    assert card.is_enchantment is True


def test_named__is_artifact__returns_true(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.is_artifact is True


def test_named__is_planeswalker__returns_true(cards_named__jace_beleren):
    card = scrython.cards.Named(exact="Jace Beleren")
    assert card.is_planeswalker is True


def test_named__is_creature__returns_false_for_pure_artifact(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.is_creature is False


def test_named__artifact_creature__is_both_artifact_and_creature(cards_named__ornithopter):
    card = scrython.cards.Named(exact="Ornithopter")
    assert card.is_artifact is True
    assert card.is_creature is True
