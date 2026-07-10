import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from pathlib import Path
import shutil

from pipeline.batch_ingestion_pipeline import BatchIngestionPipeline
from ingestion.corpus_loader import CorpusLoader
from governance.deduplication import Deduplication, DeduplicationResult
from governance.knowledge_base_manager import KnowledgeBaseManager
from embedding.base_embedding import BaseEmbedding
from vector_store.base_vector_store import BaseVectorStore

from schema.chunk import Chunk
from schema.corpus_snapshot import CorpusSnapshot
from schema.knowledge_base import KnowledgeBase,DocumentRecord
from schema.chunk_embedding import ChunkEmbedding



class FakeLoader(CorpusLoader):

    def load(self, package_dir):

        chunk = Chunk(
            chunk_id="chunk_1",
            doc_id="doc_1",
            page_num=1,
            text="Hello RAG",
            metadata={}
        )

        document = DocumentRecord(
            doc_id="doc_1",
            document_hash="hash_1"
        )

        return CorpusSnapshot(
            documents=[document],
            chunks=[chunk],
            governance=None,
        )
    
class FakeDeduplication(Deduplication):

    def deduplicate(
        self,
        snapshot,
        knowledge_base,
    ):

        return DeduplicationResult(
            documents=snapshot.documents,
            chunks=snapshot.chunks,
            skipped_documents=[],
        )
    
class FakeEmbedding(BaseEmbedding):

    def embed(
        self,
        chunks,
    ):

        embeddings = []

        for chunk in chunks:

            embeddings.append(
                ChunkEmbedding(
                    chunk=chunk,
                    embedding=[0.1, 0.2, 0.3],
                )
            )

        return embeddings

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        return [0.1, 0.2, 0.3]
    
class FakeVectorStore(BaseVectorStore):

    def __init__(self):
        self.data = []

    def insert(
        self,
        chunk_embeddings,
    ) -> None:
        self.data.extend(chunk_embeddings)

    def search(
        self,
        query_embedding,
        top_k,
        filters=None,
    ):
        return []

def test_run():

    kb_root = Path("data/test_knowledge_base")

    if kb_root.exists():
        shutil.rmtree(kb_root)

    pipeline = BatchIngestionPipeline(
        loader=FakeLoader(),
        deduplication=FakeDeduplication(),
        embedding_model=FakeEmbedding(),
        vector_store=FakeVectorStore(),
        kb_manager=KnowledgeBaseManager(kb_root),
    )

    result = pipeline.run(
        package_dir="dummy_package",
        collection_name="finance",
    )

    print(result)

    assert result["collection"] == "finance"
    assert result["documents"] == 1
    assert result["chunks"] == 1
    assert result["skipped_documents"] == 0

    print("✓ test_run passed")

def main():

    print("=" * 60)
    print("Batch Ingestion Pipeline Test")
    print("=" * 60)

    test_run()

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()