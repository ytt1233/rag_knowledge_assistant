# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog**.

---

## [v1.2.0] - 2026-07-10

### Added

#### Knowledge Base 

* Added `KnowledgeBaseManager` for knowledge base lifecycle management.
* Added knowledge base metadata persistence.
* Added knowledge base metadata update mechanism.

#### Batch Ingestion

* Implemented `CorpusLoader` to load governed corpus packages.
* Added `CorpusSnapshot` as the unified ingestion data model.
* Added governed corpus package support.
* Added end-to-end batch ingestion pipeline.

#### Deduplication

* Implemented two-stage deduplication:
  * Package-level duplicate removal
  * Knowledge base duplicate removal
* Added `DeduplicationResult` for standardized deduplication output.

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

#### Retriever

* Added `BaseRetriever` as the abstract retrieval interface.
* Implemented `VectorRetriever`.
* Connected embedding and vector search into a unified retrieval pipeline.

#### Reranker

* Added `BaseReranker` as the abstract reranking interface.
* Implemented `FlagEmbeddingReranker` for cross-encoder reranking.

#### API

* Updated FastAPI service to the new dependency injection architecture.
* Integrated the refactored RAG pipeline.

### Tests

#### Batch Ingestion

* Added `test_batch_ingestion()`
* Added `test_batch_ingestion_pipeline()`

#### Corpus Loader

* Added `test_corpus_loader()`

#### Knowledge Base

* Added `test_knowledge_base_manager()`

#### Metadata Filtering

* Added `test_metadata_filter()`

#### Deduplication

* Added `test_deduplication()`
  * `test_no_duplicates()`
  * `test_package_duplicates()`
  * `test_knowledge_base_duplicates()`

#### Embedding

* Added `test_ollama_embedding()`
  * `test_embed_success()`
  * `test_empty_chunks()`
  * `test_embedding_dimension()`

#### Vector Store

* Added `test_milvus_vector_store()`
  * `test_create_collection()`
  * `test_insert()`
  * `test_search()`

#### Retriever

* Added `test_vector_retriever()`
  * `test_retrieve()`

#### Reranker

* Added `test_flag_embedding_reranker()`
  * `test_rerank()`


### Refactored

* Unified duplicate removal workflow using in-place collection updates.
* Improved duplicate group representation with `DuplicateGroup`.
* Refactored the embedding module with interface-based architecture.
* Refactored the vector store module with interface-based architecture.
* Refactored the retrieval module with interface-based architecture.
* Refactored the reranker module with interface-based architecture.
* Refactored RAGPipeline with dependency injection.

### Documentation

* Updated README.
* Updated system architecture.
* Updated workflow.
* Updated Quick Start.
* Updated Roadmap.