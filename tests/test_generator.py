import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from embedding.ollama_embedding import OllamaEmbedding
from generator.citation_formatter import CitationFormatter
from generator.ollama_generator import OllamaGenerator
from generator.prompt_builder import PromptBuilder
from reranker.flag_embedding_reranker import FlagEmbeddingReranker
from retriever.vector_retriever import VectorRetriever
from schema.chunk import Chunk
from schema.generation_result import GenerationResult
from schema.metadata import Metadata
from vector_store.milvus_vector_store import MilvusVectorStore


def _create_chunk(
    doc_id: str,
    chunk_id: str,
    text: str,
    title: str
) -> Chunk:
    """
    Create a test chunk.
    """

    metadata = Metadata()

    metadata.domain["title"] = title

    return Chunk(
        doc_id=doc_id,
        chunk_id=chunk_id,
        text=text,
        page_num=1,
        metadata=metadata
    )


def test_generator():
    """
    Test the complete RAG generation pipeline.
    """

    # =====================================================
    # Arrange
    # =====================================================

    embedding = OllamaEmbedding()

    chunks = [
        _create_chunk(
            "doc_1",
            "chunk_1",
            "Artificial intelligence is changing the world.",
            "AI Handbook"
        ),
        _create_chunk(
            "doc_1",
            "chunk_2",
            "Large language models enable powerful applications.",
            "AI Handbook"
        ),
        _create_chunk(
            "doc_2",
            "chunk_3",
            "Artificial Intelligence (AI) refers to computer systems that learn from data.",
            "Introduction to AI"
        ),
        _create_chunk(
            "doc_2",
            "chunk_4",
            "Python is a popular programming language.",
            "Python Guide"
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

    retriever = VectorRetriever(
        embedding_model=embedding,
        vector_store=vector_store
    )

    reranker = FlagEmbeddingReranker()

    prompt_builder = PromptBuilder()

    generator = OllamaGenerator()

    citation_formatter = CitationFormatter()

    # =====================================================
    # Retrieve
    # =====================================================

    results = retriever.retrieve(
        query="What is artificial intelligence?",
        top_k=3
    )

    # =====================================================
    # Rerank
    # =====================================================

    results = reranker.rerank(
        query="What is artificial intelligence?",
        results=results,
        top_k=2
    )

    # =====================================================
    # Prompt
    # =====================================================

    prompt = prompt_builder.build(
        query="What is artificial intelligence?",
        results=results
    )

    # =====================================================
    # Generate
    # =====================================================

    answer = generator.generate(prompt)

    # =====================================================
    # Citation
    # =====================================================

    citations = citation_formatter.format(results)

    generation_result = GenerationResult(
        answer=answer,
        citations=citations
    )

    # =====================================================
    # Assert
    # =====================================================

    assert isinstance(generation_result.answer, str)
    assert len(generation_result.answer.strip()) > 0

    assert isinstance(generation_result.citations, list)

    print("\nAnswer")
    print("=" * 60)
    print(generation_result.answer)

    print("\nCitations")
    print("=" * 60)

    for citation in generation_result.citations:
        print(citation)


def main():

    print("=" * 60)
    print("Generator Pipeline Test")
    print("=" * 60)

    test_generator()

    print("✓ test_generator")

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()