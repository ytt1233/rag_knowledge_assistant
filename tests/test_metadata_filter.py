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
    text: str,
    title: str,
    category: str
) -> Chunk:
    """
    Create a test chunk.
    """

    metadata = Metadata()

    metadata.domain["title"] = title
    metadata.domain["category"] = category

    return Chunk(
        doc_id=doc_id,
        chunk_id=chunk_id,
        text=text,
        page_num=1,
        metadata=metadata
    )

def _prepare_retriever() -> VectorRetriever:
    """
    Prepare a retriever with test data.
    """

    embedding = OllamaEmbedding()

    chunks = [

        _create_chunk(
            "doc_ai",
            "chunk_ai_1",
            "Artificial intelligence is changing the world.",
            "AI Handbook",
            "AI"
        ),

        _create_chunk(
            "doc_ai",
            "chunk_ai_2",
            "Machine learning is a subset of AI.",
            "AI Handbook",
            "AI"
        ),

        _create_chunk(
            "doc_python",
            "chunk_py_1",
            "Python is a programming language.",
            "Python Guide",
            "Programming"
        ),

        _create_chunk(
            "doc_python",
            "chunk_py_2",
            "Functions organize reusable code.",
            "Python Guide",
            "Programming"
        ),

    ]

    chunk_embeddings = embedding.embed(chunks)

    vector_store = MilvusVectorStore()

    if vector_store.has_collection():
        vector_store.drop_collection()

    vector_store.create_collection(
        embedding.embedding_dim
    )

    vector_store.insert(
        chunk_embeddings
    )

    return VectorRetriever(
        embedding_model=embedding,
        vector_store=vector_store
    )

def test_filter_by_title():
    """
    Test filtering by title.
    """

    retriever = _prepare_retriever()

    results = retriever.retrieve(
        query="What is artificial intelligence?",
        top_k=5,
        filters={
            "title": "AI Handbook"
        }
    )

    assert len(results) > 0

    for result in results:

        assert (
            result.chunk.metadata.get_domain("title")
            == "AI Handbook"
        )

    print("✓ test_filter_by_title")

def test_filter_by_category():
    """
    Test filtering by category.
    """

    retriever = _prepare_retriever()

    results = retriever.retrieve(
        query="What is artificial intelligence?",
        top_k=5,
        filters={
            "category": "AI"
        }
    )

    assert len(results) > 0

    for result in results:

        assert (
            result.chunk.metadata.get_domain("category")
            == "AI"
        )

    print("✓ test_filter_by_category")

def test_filter_by_title_and_category():
    """
    Test filtering by title and category.
    """

    retriever = _prepare_retriever()

    results = retriever.retrieve(
        query="What is artificial intelligence?",
        top_k=5,
        filters={
            "title": "AI Handbook",
            "category": "AI"
        }
    )

    assert len(results) > 0

    for result in results:

        assert (
            result.chunk.metadata.get_domain("title")
            == "AI Handbook"
        )

        assert (
            result.chunk.metadata.get_domain("category")
            == "AI"
        )

    print("✓ test_filter_by_title_and_category")

def main():

    print("=" * 60)
    print("Metadata Filter Test")
    print("=" * 60)

    # test_filter_by_title()

    # test_filter_by_category()

    test_filter_by_title_and_category()

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()  