import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from embedding.ollama_embedding import OllamaEmbedding
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


def test_retrieve():
    """
    Test the complete retrieval pipeline.
    """

    # Arrange
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

    # Act
    results = retriever.retrieve(
        query="What is artificial intelligence?",
        top_k=2
    )

    # Assert
    assert len(results) == 2

    assert results[0].chunk is not None
    assert results[0].chunk.text != ""
    assert isinstance(results[0].score, float)

    print("\nTop 2 Retrieval Results:")

    for result in results:
        print("-" * 60)
        print(f"Score   : {result.score:.4f}")
        print(f"Chunk ID: {result.chunk.chunk_id}")
        print(f"Doc ID  : {result.chunk.doc_id}")
        print(f"Text    : {result.chunk.text}")


def main():

    print("=" * 60)
    print("Vector Retriever Test")
    print("=" * 60)

    test_retrieve()
    print("✓ test_retrieve")

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()