import sys 
sys.path.append(r'F:\mycode\rag_knowledge_assistant')
from embedding.ollama_embedding import OllamaEmbedding
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


def test_create_collection():
    """
    Test collection creation.
    """

    embedding = OllamaEmbedding()

    vector_store = MilvusVectorStore()

    vector_store.create_collection(
        embedding.embedding_dim
    )

    assert vector_store.has_collection()


def test_insert():
    """
    Test inserting chunk embeddings.
    """

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
    ]

    chunk_embeddings = embedding.embed(chunks)

    vector_store = MilvusVectorStore()

    vector_store.create_collection(
        embedding.embedding_dim
    )

    vector_store.insert(
        chunk_embeddings
    )



def test_search():
    """
    Test searching for similar chunks.
    """

    # Arrange
    embedding = OllamaEmbedding()

    chunks = [
        _create_chunk(
            "doc_3",
            "chunk_31",
            "Artificial intelligence is changing the world."
        ),
        _create_chunk(
            "doc_3",
            "chunk_32",
            "Large language models enable powerful applications."
        ),
        _create_chunk(
            "doc_4",
            "chunk_41",
            "Artificial Intelligence (AI) refers to computer systems designed to learn from data, make decisions, generate content or predict outcomes based on the information they process."
        ),
        _create_chunk(
            "doc_4",
            "chunk_42",
            "Use a notebook or digital calendar to track assignment deadlines."
        ),
        _create_chunk(
            "doc_4",
            "chunk_43",
            "Ask yourself questions about the content you just learned."
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

    query_embedding = embedding.embed_query(
        "What is artificial intelligence?"
    )

    # Act
    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=2
    )

    # Assert
    assert len(results) == 2

    assert results[0].chunk is not None
    assert results[0].chunk.text != ""

    assert isinstance(results[0].score, float)

    print("\nTop 2 Search Results:")

    for result in results:
        print("-" * 60)
        print(f"Score   : {result.score:.4f}")
        print(f"Chunk ID: {result.chunk.chunk_id}")
        print(f"Text    : {result.chunk.text}")

def main():

    print("=" * 60)
    print("Milvus Vector Store Test")
    print("=" * 60)

    test_create_collection()
    print("✓ test_create_collection")

    test_insert()
    print("✓ test_insert")

    test_search()
    print("✓ test_search")

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()