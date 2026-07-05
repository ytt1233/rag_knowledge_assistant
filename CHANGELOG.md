# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog**.

---

## [v1.2.0] - 2026-07-05

### Added

* Implemented `CorpusLoader` to load governed corpus packages.
* Added `CorpusSnapshot` as the unified ingestion data model.
* Implemented two-stage deduplication:

  * Package-level duplicate removal
  * Knowledge base duplicate removal
* Added `DeduplicationResult` for standardized deduplication output.
* Added reusable test environment for deduplication tests.

### Tests

* Added `test_no_duplicates()`
* Added `test_package_duplicates()`
* Added `test_knowledge_base_duplicates()`

### Refactored

* Unified duplicate removal workflow using in-place collection updates.
* Improved duplicate group representation with `DuplicateGroup`.
