import sys
sys.path.append(r'F:\mycode\rag_knowledge_assistant')
from embedding.ollama_embedding import OllamaEmbedding
from schema.chunk import Chunk
from schema.metadata import Metadata


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


def test_embed_success():
    """
    Test embedding generation for multiple chunks.
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
    ]

    # Act
    results = embedding.embed(chunks)

    # Assert
    assert len(results) == len(chunks)

    for result, chunk in zip(results, chunks):
        assert result.chunk == chunk
        assert isinstance(result.embedding, list)
        assert len(result.embedding) > 0

    print("✓ test_embed_success")


def test_empty_chunks():
    """
    Test embedding with an empty chunk list.
    """

    # Arrange
    embedding = OllamaEmbedding()

    # Act
    results = embedding.embed([])

    # Assert
    assert results == []

    print("✓ test_empty_chunks")
def test_embedding_dimension():
    """
    Test embedding dimension.
    """

    # Arrange
    embedding = OllamaEmbedding()

    # Act
    dimension = embedding.embedding_dim

    # Assert
    assert isinstance(dimension, int)
    assert dimension > 0

    print("✓ test_embedding_dimension")



def main():

    print("=" * 60)
    print("Embedding Test")
    print("=" * 60)

    test_empty_chunks()
    test_embedding_dimension()
    test_embed_success()

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()