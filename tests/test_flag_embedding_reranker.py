import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from embedding.ollama_embedding import OllamaEmbedding
from reranker.flag_embedding_reranker import FlagEmbeddingReranker
from retriever.vector_retriever import VectorRetriever
from schema.chunk import Chunk
from schema.metadata import Metadata
from vector_store.milvus_vector_store import MilvusVectorStore


def _create_chunk(
    doc_id: str,
    chunk_id: str,
    text: str
) -> Chunk:
    """
    Create a test chunk.
    """
    return Chunk(
        doc_id=doc_id,
        chunk_id=chunk_id,
        text=text,
        page_num=1,
        metadata=Metadata()
    )


def test_rerank():
    """
    Test the complete retrieval and reranking pipeline.
    """

    # =====================================================
    # Arrange
    # =====================================================

    embedding = OllamaEmbedding()

    chunks = [
        _create_chunk(
            "doc_1",
            "chunk_1",
            "Artificial intelligence is changing the world."
        ),
        _create_chunk(
            "doc_1",
            "chunk_2",
            "Large language models enable powerful applications."
        ),
        _create_chunk(
            "doc_2",
            "chunk_3",
            "Artificial Intelligence (AI) refers to computer systems that learn from data."
        ),
        _create_chunk(
            "doc_2",
            "chunk_4",
            "Python is a popular programming language."
        ),
    ]

    chunk_embeddings = embedding.embed(chunks)

    vector_store = MilvusVectorStore()

    vector_store.create_collection(
        embedding.embedding_dim
    )

    vector_store.insert(
        chunk_embeddings
    )

    retriever = VectorRetriever(
        embedding_model=embedding,
        vector_store=vector_store
    )

    reranker = FlagEmbeddingReranker(
        model_name=r"D:\models\bge-reranker-v2-m3"
    )

    # =====================================================
    # Act
    # =====================================================

    retrieved_results = retriever.retrieve(
        query="What is artificial intelligence?",
        top_k=4
    )

    print("\nVector Retrieval Results")
    print("=" * 60)

    for result in retrieved_results:
        print(f"Score   : {result.score:.4f}")
        print(f"Chunk ID: {result.chunk.chunk_id}")
        print(f"Text    : {result.chunk.text}")
        print("-" * 60)

    reranked_results = reranker.rerank(
        query="What is artificial intelligence?",
        results=retrieved_results,
        top_k=2
    )

    # =====================================================
    # Assert
    # =====================================================

    assert len(reranked_results) == 2

    assert isinstance(
        reranked_results[0].score,
        float
    )

    assert (
        reranked_results[0].score
        >=
        reranked_results[1].score
    )

    print("\nReranked Results")
    print("=" * 60)

    for result in reranked_results:
        print(f"Score   : {result.score:.4f}")
        print(f"Chunk ID: {result.chunk.chunk_id}")
        print(f"Doc ID  : {result.chunk.doc_id}")
        print(f"Text    : {result.chunk.text}")
        print("-" * 60)


def main():

    print("=" * 60)
    print("FlagEmbedding Reranker Test")
    print("=" * 60)

    test_rerank()

    print("✓ test_rerank")

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()