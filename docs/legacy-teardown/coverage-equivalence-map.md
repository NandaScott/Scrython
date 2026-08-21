# Coverage equivalence map — legacy test teardown gate

Issue: #211 (gate for #182, blocked by #180/#181, both closed). Per-case
list of which legacy tests are safe to delete now vs. which must be kept.
Writes no production change and deletes nothing itself.

## Resolution (2026-08-21)

Reviewed with @NandaScott: proceed with the deletion slices on the
mechanism-level replacements below. Gaps are real but none are silently
dropped — tracked in [#244](https://github.com/NandaScott/Scrython/issues/244)
(`ready-for-human`, blocked by #214 so it can't start until teardown itself
is done).

## How to read the tables

Each row is one legacy test case. **Covered** rows are safe to delete now.
**GAP** rows are not — keep them until #244 closes that gap.

- **Covered** — a named test (usage or sweep suite) exercises the same
  observable behavior through the public API. Verified by reading both
  tests, not by name-matching.
- **Covered (generic mechanism)** — not covered by an equivalent
  *endpoint-specific* test, but by a retained component test in
  `test_base.py` (`TestRequestHandlerPathBuilding` /
  `TestRequestHandlerParamBuilding`) that exercises the same underlying code
  with a synthetic handler. These retained tests use path templates
  structurally identical to the ones being deleted (`cards/:id`,
  `cards/:code/:number/:lang?`, etc.), so the deletion is sound *only
  because* those retained tests stay.
- **GAP** — no test anywhere (legacy suite excluded) exercises this.

---

## `tests/test_cards.py`

| Legacy case | Status |
|---|---|
| `TestNamed::test_fuzzy_search` | Covered — `usage/test_cards_named.py::test_named__exact__returns_correct_name` (fuzzy vs exact is the same kwarg-passthrough code path; param mechanism below) |
| `TestNamed::test_exact_search` | Covered — same |
| `TestNamed::test_endpoint_path` | Covered (generic mechanism) — `test_base.py::TestRequestHandlerPathBuilding` |
| `TestSearch::test_search_query` (`.object`, `.total_cards`, url param) | `.object`/`.total_cards` covered — `sweep/test_property_sweep.py` LIST_CORPUS (`cards_search__lea_red`); url param covered (generic mechanism) |
| `TestSearch::test_list_mixin_data_method` | Covered, more thoroughly — `usage/test_list_helpers.py` (4-card multiset vs 1 card) |
| `TestSearch::test_list_mixin_has_more` | Covered — `usage/test_list_envelope.py::test_by_id__rulings__has_more_is_bool` (shared mixin, different endpoint) |
| `TestSearch::test_endpoint_path` | Covered (generic mechanism) |
| `TestAutocomplete::test_autocomplete_query` (object/total_values) | Covered — `usage/test_catalog_envelope.py` + sweep CATALOG_CORPUS |
| `TestAutocomplete::test_catalog_mixin_data_method` | Covered — same |
| `TestAutocomplete::test_endpoint_path` | Covered (generic mechanism) |
| `TestRandom::test_random_card` | **GAP** — `Random` never constructed outside legacy suite |
| `TestRandom::test_endpoint_path` | **GAP** (same) |
| `TestCollection::test_collection_with_identifiers` | **GAP** — `Collection` never constructed outside legacy suite |
| `TestCollection::test_endpoint_path` | **GAP** (same) |
| `TestByCodeNumber::test_get_card_by_code_and_number` | **GAP** — not constructed anywhere else |
| `TestByCodeNumber::test_with_language_param` | **GAP** |
| `TestByCodeNumber::test_missing_required_params` | Covered (generic mechanism) — `test_base.py::test_missing_required_param_raises_error` |
| `TestByMultiverseId::test_get_card_by_multiverse_id` | **GAP** |
| `TestByMTGOId::test_get_card_by_mtgo_id` | **GAP** |
| `TestByArenaId::test_get_card_by_arena_id` | **GAP** |
| `TestByTCGPlayerId::test_get_card_by_tcgplayer_id` | **GAP** |
| `TestByCardMarketId::test_get_card_by_cardmarket_id` | **GAP** |
| `TestById::test_get_card_by_id` | Covered — `usage/test_layout_corpus.py` (11 fixtures via `ById`) |
| `TestCardsMixins::test_core_fields_mixin` | Covered, more rigorously — `sweep/test_property_sweep.py` (introspects every `CoreFieldsMixin` `@property` against 26 fixtures, value-level not just type-level) |
| `TestCardsMixins::test_gameplay_fields_mixin` | Covered, more rigorously — same |
| `TestCardsMixins::test_print_fields_mixin` | Covered, more rigorously — same |

## `tests/test_sets.py`

| Legacy case | Status |
|---|---|
| `TestAll::test_get_all_sets` | **GAP** — `sets.All` never constructed outside legacy suite |
| `TestAll::test_list_mixin_data_method` | **GAP** (same) |
| `TestAll::test_endpoint_path` | **GAP** (same) |
| `TestByCode::test_get_set_by_code` | Covered — `usage/test_sets_by_code.py` |
| `TestByCode::test_missing_code_param` | Covered (generic mechanism) |
| `TestByTCGPlayerId::*` (2 cases) | **GAP** — `sets.ByTCGPlayerId` never constructed elsewhere |
| `TestById::test_get_set_by_id` | **GAP** — `sets.ById` never constructed elsewhere (only `ByCode` is used) |
| `TestById::test_missing_id_param` | Covered (generic mechanism) |
| `TestSetsMixins::test_sets_object_mixin_properties` | Covered, more rigorously — sweep `SET_CORPUS` |
| `TestSetsMixins::test_sets_object_from_list` | **GAP** — depends on `All()`, which is unconstructed anywhere else |

## `tests/test_bulk_data.py`

| Legacy case | Status |
|---|---|
| `TestAll::*` (3 cases) | **GAP** — `bulk_data.All` never constructed elsewhere |
| `TestById::test_get_bulk_data_by_id` | Covered — `usage/test_bulk_data_by_id.py`, `usage/test_bulk_data_download.py` |
| `TestById::test_missing_id_param` | Covered (generic mechanism) |
| `TestByType::test_get_bulk_data_by_type` | **GAP** — `ByType` never constructed elsewhere |
| `TestByType::test_missing_type_param` | Covered (generic mechanism) |
| `TestBulkDataMixins::test_bulk_data_object_mixin_properties` | Covered, more rigorously — sweep `BULK_DATA_CORPUS` |
| `TestBulkDataMixins::test_bulk_data_object_from_list` | **GAP** — depends on `All()` |
| `TestBulkDataDownload::test_download_returns_parsed_data` | Covered — `usage/test_bulk_data_download.py` |
| `TestBulkDataDownload::test_download_saves_to_file` | **GAP** — no usage test exercises `filepath=` |
| `TestBulkDataDownload::test_download_without_return_data` | **GAP** |
| `TestBulkDataDownload::test_download_with_invalid_gzip` | **GAP** |
| `TestBulkDataDownload::test_download_with_invalid_json` | **GAP** |
| `TestBulkDataDownload::test_download_progress_without_tqdm_raises_import_error` | **GAP** |
| `TestBulkDataDownload::test_download_decompresses_gzip_body_no_progress` | Covered — same code path as the basic download test |
| `TestBulkDataDownload::test_download_decompresses_gzip_body_with_progress` | **GAP** — `progress=True` path never exercised |
| `TestBulkDataDownload::test_download_sets_user_agent` | **GAP** |

## `tests/test_catalogs.py`

| Legacy case | Status |
|---|---|
| `TestCardNames`, `TestPlaneswalkerTypes`, `TestCardTypes`, `TestKeywordAbilities`, `TestKeywordActions`, `TestArtifactTypes`, `TestEnchantmentTypes`, `TestLandTypes`, `TestSpellTypes` (14 cases total) | **GAP** — only `CreatureTypes` is constructed anywhere outside the legacy suite |
| `TestCreatureTypes::*` (2 cases) | Covered — `usage/test_catalogs_creature_types.py` |
| `TestCatalogsMixin::test_catalog_properties` (via `CardNames`) | **GAP** (depends on untested class) |
| `TestCatalogsMixin::test_data_content` (via `CreatureTypes`) | Covered — same fixture as above |
| `TestCatalogsFactory::*` (19 cases: 18 routing + 1 invalid-type) | **GAP, entire class** — `Catalogs(catalog_type=...)` is never called anywhere outside the legacy suite |

## `tests/test_migrations.py`

| Legacy case | Status |
|---|---|
| `TestAll::*` (4 cases) | **GAP** — `migrations.All` never constructed elsewhere |
| `TestById::test_get_migration_by_id` | Partially covered — `usage/test_migrations_by_id.py` asserts `migration_strategy`/`old_scryfall_id`; `.object`/`.id` not asserted there but proven generically by construction succeeding |
| `TestById::test_endpoint_path` | Covered (generic mechanism) |
| `TestById::test_missing_id_param` | Covered (generic mechanism) |
| `TestMigrationsMixins::test_migrations_object_mixin_properties` (uri, performed_at, new_scryfall_id, note, metadata) | **Partial GAP** — no sweep spec exists for the migrations object type (unlike Card/Sets/BulkData), so `uri`, `performed_at`, `new_scryfall_id`, `note`, `metadata` are asserted only in the legacy file |
| `TestMigrationsMixins::test_merge_migration_properties` | **GAP** — depends on `All()` |
| `TestMigrationsMixins::test_delete_migration_properties` | **GAP** — depends on `All()`; also the only place `new_scryfall_id is None` (delete strategy) is exercised |
| `TestMigrationsMixins::test_filter_by_strategy` | **GAP** — depends on `All()` |
| `TestMigrationsFactory::*` (3 cases) | **GAP, entire class** — `Migrations(...)` never called elsewhere |

## `tests/test_rulings.py`

| Legacy case | Status |
|---|---|
| `TestById::test_get_rulings_by_id` | Covered — `usage/test_list_envelope.py`, `usage/test_rulings_by_id.py` |
| `TestById::test_list_mixin_data_method` | Covered — same |
| `TestById::test_endpoint_path` | Covered (generic mechanism) |
| `TestById::test_missing_id_param` | Covered (generic mechanism) |
| `TestByMultiverseId::*`, `TestByMTGOId::*`, `TestByArenaId::*`, `TestByCodeNumber::*` (8 cases) | **GAP** — none of these classes constructed outside legacy suite (only `ById` is used) |
| `TestRulingsMixins::test_rulings_object_mixin_properties` (object, oracle_id, source, published_at, comment) | Partially covered — `source`/`published_at`/`comment` via usage tests; `object == "ruling"` and `oracle_id` not asserted elsewhere |
| `TestRulingsMixins::test_rulings_object_from_list` | Covered — `usage/test_rulings_by_id.py` |
| `TestRulingsMixins::test_filter_by_source` | **GAP** — no usage test filters rulings by source |
| `TestRulingsFactory::*` (6 cases) | **GAP, entire class** — `Rulings(...)` never called elsewhere |

## `tests/test_symbology.py`

| Legacy case | Status |
|---|---|
| `TestAll::*` (3 cases) | Partially covered — `usage/test_symbology_all.py` only asserts `symbol`/`english` for one entry; `.object`, `.has_more`, url/endpoint path not asserted there |
| `TestParseMana::*` (3 cases) | **GAP, entire class** — `ParseMana` never constructed outside legacy suite |
| `TestSymbologyMixins::test_symbology_object_mixin_properties` (represents_mana, mana_value, appears_in_mana_costs, funny, colors, hybrid, phyrexian) | **GAP** — usage suite only checks `symbol`/`english` |
| `TestSymbologyMixins::test_hybrid_symbol_properties` | **GAP** |
| `TestSymbologyMixins::test_non_mana_symbol_properties` | **GAP** |
| `TestSymbologyMixins::test_mana_cost_mixin_properties` | **GAP** — depends on `ParseMana` |
| `TestSymbologyMixins::test_filter_symbols_by_property` | **GAP** |
| `TestSymbologyFactory::*` (2 cases) | **GAP, entire class** — `Symbology(...)` never called elsewhere |

## `tests/test_property_types.py`

**Fully replaced, more rigorously.** `sweep/test_property_sweep.py::test_passthrough_sweep`
introspects every `@property` on `CoreFieldsMixin`/`GameplayFieldsMixin`/
`PrintFieldsMixin`/sets/bulk-data mixins via `inspect.getmembers` and asserts
actual *value* passthrough (not just type) against 26 card fixtures spanning
every layout, plus dedicated set/bulk-data fixtures. The sweep engine's own
self-tests (`test_sweep_engine_self.py::test_every_accessor_is_asserted`,
`test_every_exception_declares_coverage`) enforce that no accessor can
silently fall out of the sweep. This is a strict superset of what
`test_property_types.py`'s type-only parametrized checks did. No gap.

## `tests/test_magic_methods.py`

| Legacy case | Status |
|---|---|
| `TestMagicMethodsBase::test_repr_with_card` | Covered — `usage/test_stringification.py::test_card__repr__class_id_name_format` |
| `TestMagicMethodsBase::test_repr_with_set` | Covered — `test_set__repr__class_id_name_format` |
| `TestMagicMethodsBase::test_repr_without_id_or_name` | **GAP** — no usage fixture for a handler with no id/name |
| `TestMagicMethodsBase::test_str_with_card` | Covered — `test_card__str__name_set_format` |
| `TestMagicMethodsBase::test_str_with_card_no_set` | **GAP** — no usage fixture for a card lacking `set` |
| `TestMagicMethodsBase::test_str_with_set` | Covered — `test_set__str__name_code_format` |
| `TestMagicMethodsBase::test_str_with_list` | Covered — `test_list__str__list_count_format` |
| `TestMagicMethodsBase::test_str_with_catalog` | Covered — `test_catalog__str__catalog_count_format` |
| `TestMagicMethodsBase::test_eq_same_card_same_id` | Covered — `usage/test_equality_hash.py::test_card__same_id__is_equal` |
| `TestMagicMethodsBase::test_eq_different_cards` | Covered — `test_card__different_id__is_not_equal` |
| `TestMagicMethodsBase::test_eq_with_non_handler_object` | Covered (str/int/dict); `is not None` branch specifically not asserted |
| `TestMagicMethodsBase::test_eq_without_ids` (identity fallback) | Covered, differently — `usage/test_equality_hash.py::test_catalog__id_less__*` proves the same identity-fallback branch via a real id-less object (`CreatureTypes`) instead of a synthetic handler |
| `TestMagicMethodsBase::test_hash_same_card` | Covered indirectly — proven by set/dict dedup tests below, not a direct `hash() ==` assertion |
| `TestMagicMethodsBase::test_hash_different_cards` | Covered indirectly — same |
| `TestMagicMethodsBase::test_hash_enables_set_usage` | Covered — `test_card__usable_as_set_member` |
| `TestMagicMethodsBase::test_hash_enables_dict_usage` | Covered — `test_card__usable_as_dict_key` |
| `TestMagicMethodsObject::*` (10 cases) | **GAP, entire class** — `cards.Object` defines its own `__repr__`/`__str__`/`__eq__`/`__hash__` (`scrython/cards/cards.py:20-83`), separate from `ScrythonRequestHandler`'s. The usage suite never constructs `Object` directly from a dict, so none of this is exercised elsewhere. |

## `tests/test_serialization.py`

| Legacy case | Status |
|---|---|
| `TestSerializationBase::test_to_dict_returns_copy` | Covered — `usage/test_serialization.py::test_named__to_dict__mutation_does_not_leak` |
| `TestSerializationBase::test_to_dict_modification_doesnt_affect_original` | Covered — same |
| `TestSerializationBase::test_to_json_returns_valid_json` | Covered — `test_named__to_json__round_trips` |
| `TestSerializationBase::test_to_json_with_indent` | **GAP** — no usage test passes `indent=` |
| `TestSerializationBase::test_to_json_with_sort_keys` | **GAP** — no usage test passes `sort_keys=` |
| `TestSerializationBase::test_from_dict_creates_instance` | Covered — `test_named__from_dict__constructs_without_network` |
| `TestSerializationBase::test_from_dict_doesnt_modify_source` | **GAP** — not explicitly asserted |
| `TestSerializationBase::test_round_trip_to_dict_from_dict` | Covered — `test_named__from_dict__exposes_same_surface` |
| `TestSerializationBase::test_round_trip_to_json_from_dict` | Covered — `test_named__to_json__round_trips` |
| `TestSerializationObject::*` (5 cases) | **GAP, entire class** — `cards.Object` has its own `to_dict`/`to_json`/`from_dict` (`scrython/cards/cards.py:85-134`), never exercised outside the legacy suite |
| `TestSerializationList::test_to_list_with_objects` | Covered — `sweep/test_property_sweep.py::test_wrapped_list_data_preserves_items` |
| `TestSerializationList::test_to_list_empty` | **GAP** |
| `TestSerializationList::test_to_list_doesnt_affect_original` | **GAP** — mutation-isolation of the returned list not asserted elsewhere |
| `TestSerializationList::test_to_list_multiple_calls` | **GAP** |

## `tests/test_iteration.py`

| Legacy case | Status |
|---|---|
| `TestIterationBasics::test_iter_allows_direct_iteration` | Covered — `usage/test_list_envelope.py::test_by_id__rulings__is_directly_iterable` |
| `TestIterationBasics::test_len_returns_current_page_size` | **GAP** — `__len__` never asserted in usage suite |
| `TestIterationBasics::test_iter_with_empty_results` | **GAP** |
| `TestIterationBasics::test_iter_multiple_times` | **GAP** |
| `TestIterationBasics::test_iter_works_with_list_comprehension` | Covered, loosely — subsumed by the iterability proof above |
| `TestIterationBasics::test_iter_works_with_filter` | Covered, loosely — same |
| `TestIterAllPagination::test_iter_all_single_page` | **GAP** — the only `iter_all()` usage test uses a 2-page fixture; the "already exhausted on page 1" branch is never hit as the *first* page |
| `TestIterAllPagination::test_iter_all_multiple_pages` | Covered — `test_by_id__rulings__iter_all_yields_items_across_pages` |
| `TestIterAllPagination::test_iter_all_empty_results` | **GAP** |
| `TestIterAllPagination::test_iter_all_is_generator` | **GAP** |
| `TestIterAllPagination::test_iter_all_can_be_consumed_once` | **GAP** — generator-exhaustion guarantee not asserted elsewhere |
| `TestIterAllPagination::test_iter_vs_iter_all_single_page` | **GAP** |

## `tests/test_convenience.py`

| Legacy case | Status |
|---|---|
| `test_is_legal_in_*` (3 cases) | Covered — `usage/test_predicates.py` |
| `test_has_color_single_color/multicolor/colorless` | Covered — `usage/test_predicates.py` |
| `test_has_color_case_insensitive` | **GAP** — usage suite tests case-insensitivity for `is_legal_in` but not `has_color` (same implementation pattern, low risk) |
| `test_is_creature/instant/sorcery/enchantment/artifact/planeswalker` | Covered — `usage/test_predicates.py` |
| `test_type_checks_artifact_creature` | Covered — `test_named__artifact_creature__is_both_artifact_and_creature` |
| `test_lowest_price_*` / `test_highest_price_*` (5 cases) | Covered — `usage/test_cards_price_and_image.py` |
| `test_get_image_url_normal` (incl. `size="large"`) | Partially covered — usage test only checks "is not None"; the `size="large"` branch and exact URL are not asserted |
| `test_get_image_url_double_faced` (incl. `size="large"`) | Partially covered — front-face URL covered; `size="large"` for DFC not asserted |
| `test_get_image_url_no_images` | Covered |
| `TestListConvenienceMethods::*` (7 cases) | Covered — `usage/test_list_helpers.py`, using richer real-card fixtures than the legacy synthetic dicts |

## Embedded `mock_urlopen` classes (mixed-file split)

Per PRD #182, only these classes are retained in each file; everything else
in the file is deleted. Retained classes are pure/synthetic (no HTTP mock)
and cover the generic mechanism; deleted classes are the ones actually
integrating with a live-ish request flow.

| File | Deleted class | Status |
|---|---|---|
| `test_base.py` | `TestRequestHandlerFetch::test_successful_fetch` | Covered — implicitly by every usage test (a successful fetch is the precondition for all of them) |
| `test_base.py` | `TestRequestHandlerFetch::test_fetch_with_error_response_raises_scryfall_error` | **GAP** — no usage/sweep test ever arms an error response; `ScryfallError` being raised by a real `_fetch()` is untested once this goes |
| `test_base.py` | `TestRequestHandlerFetch::test_request_headers` | **GAP** — User-Agent on the regular fetch path (distinct from the download path) not asserted elsewhere |
| `test_base.py` | `TestRequestHandlerFetch::test_endpoint_property` | **GAP**, low severity |
| `test_base.py` | `TestScryfallDataReadOnly` (6 cases) | **GAP, entire class, structurally** — `tests/usage/CONVENTIONS.md` rule 2 forbids asserting on `.scryfall_data` in usage tests. Nothing currently proves the SimpleNamespace wrapper is read-only, dot-accessible, non-leaking on mutation, cached, or correctly nests dicts/lists. |
| `test_caching.py` | `TestRequestHandlerCaching` (9 cases) | **GAP, entire class, structurally** — the `stub_response` seam never sets `cache=True`/inspects cache state, so handler↔cache integration (as opposed to `MemoryCache` in isolation, which is retained) has no coverage |
| `test_rate_limiting.py` | `TestRequestHandlerRateLimiting` (12 cases) | **GAP, entire class, structurally** — `stub_response` patches `RateLimiter.wait` to a no-op for every usage test by design, so handler↔rate-limiter integration (as opposed to `RateLimiter` in isolation, which is retained) has no coverage |

Retained classes confirmed to genuinely subsume the mechanism they claim to
(spot-checked, not assumed): `TestRequestHandlerPathBuilding` and
`TestRequestHandlerParamBuilding` in `test_base.py` use synthetic
`_endpoint` templates (`"cards/:id"`, `"cards/:code/:number/:lang?"`) that
are structurally identical to the real templates in `scrython/cards/cards.py`
(`/cards/multiverse/:id`, `/cards/:code/:number/:lang?`, etc.), and assert
the same missing-required-param `KeyError` message format the deleted
endpoint-specific tests checked. `TestMemoryCache`/`TestCacheKeyGeneration`/
`TestGlobalCache` and `TestRateLimiter`/`TestSlowRateLimiter`/
`TestEndpointRateLimiterAssignment` are pure unit tests of the underlying
classes with no HTTP involved — they stay correct regardless of this
deletion, but they don't prove the *integration* points above.

---

## Full suite run (standing evidence)

```
./venv/bin/python -m pytest -q
```

```
1 failed, 4793 passed, 1 skipped in 7.54s
FAILED tests/test_packaging.py::test_py_typed_in_wheel - subprocess.CalledProcessError: ... python -m build ...
```

The one failure is pre-existing and out of scope: `test_py_typed_in_wheel`
shells out to `python -m build`, and the `build` package simply isn't
installed in this checkout's `venv` (`ModuleNotFoundError: No module named
'build'`) — an environment gap, not a regression, and unrelated to any file
in the teardown list (`git log -1 -- tests/test_packaging.py` → PR #198,
unrelated PEP 561 work). Every other test — including all files slated for
deletion, all retained component tests, the full usage suite, and the full
sweep suite — passes.
