import os

from ingestion.corpus_loader import CorpusLoader
from embedding.base_embedding import BaseEmbedding
from vector_store.base_vector_store import BaseVectorStore
from governance.deduplication import Deduplication
from governance.knowledge_base_manager import KnowledgeBaseManager
from datetime import datetime


class BatchIngestionPipeline:

    def __init__(
        self,
        loader: CorpusLoader,
        deduplication: Deduplication,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore,
        kb_manager: KnowledgeBaseManager,
    ):
        self.loader = loader
        self.deduplication = deduplication
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.kb_manager = kb_manager

    def run(
        self,
        package_dir: str,
        collection_name: str,
    ) -> dict[str, int]:
        """
        Batch ingest a corpus package into a knowledge base.
        """
        # 1、确保collection存在
        if not self.vector_store.has_collection():

            self.vector_store.create_collection(

                self.embedding_model.embedding_dim
            )
        # 2. 确保knowledge base存在
        if self.kb_manager.exists(collection_name):
            kb = self.kb_manager.load(collection_name)
        else:
            kb = self.kb_manager.create(collection_name)

        # 3. Load corpus package
        snapshot = self.loader.load(package_dir)

        # 4. Deduplicate
        result = self.deduplication.deduplicate(
            snapshot,
            kb,
        )

        # 5. Generate embeddings
        chunk_embeddings = self.embedding_model.embed(
            result.chunks
        )

        # 6. Insert into vector store
        self.vector_store.insert(
            chunk_embeddings
        )

        # 7. Update KnowledgeBase
        kb.documents.extend(
            result.documents
        )

        kb.status.document_count = len(kb.documents)
        kb.status.chunk_count += len(result.chunks)
        kb.status.embedding_count += len(chunk_embeddings)

        now = datetime.now().isoformat()

        kb.status.last_ingestion_time = now
        kb.status.last_updated_time = now

        # 8. Save KnowledgeBase
        self.kb_manager.save(kb)

        print("\nBatch ingestion completed.")
        print(f"Collection          : {collection_name}")
        print(f"Inserted documents  : {len(result.documents)}")
        print(f"Inserted chunks     : {len(result.chunks)}")
        print(f"Skipped documents   : {len(result.skipped_documents)}")

        return {
            "collection": collection_name,
            "documents": len(result.documents),
            "chunks": len(result.chunks),
            "skipped_documents": len(result.skipped_documents),
        }
