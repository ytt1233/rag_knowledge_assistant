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

#### Embedding

* Introduced the `ChunkEmbedding` data model.
* Added `BaseEmbedding` as the abstract embedding interface.
* Implemented `OllamaEmbedding`.
* Added support for both chunk embedding and query embedding.

#### Vector Store

* Added `BaseVectorStore` as the abstract vector store interface.
* Implemented `MilvusVectorStore`.
* Added collection creation.
* Added vector insertion.
* Added semantic vector search.
* Introduced the `SearchResult` data model for retrieval results.

### Tests

#### Deduplication

* Added `test_no_duplicates()`
* Added `test_package_duplicates()`
* Added `test_knowledge_base_duplicates()`

#### Embedding

* Added `test_embed_success()`
* Added `test_empty_chunks()`
* Added `test_embedding_dimension()`

#### Vector Store

* Added `test_create_collection()`
* Added `test_insert()`
* Added `test_search()`

### Refactored

* Unified duplicate removal workflow using in-place collection updates.
* Improved duplicate group representation with `DuplicateGroup`.
* Refactored the embedding module with interface-based architecture.
* Unified vector store interfaces for future retriever integration.