import sys
sys.path.append(r'F:\mycode\rag_knowledge_assistant')

from pathlib import Path

from ingestion.corpus_loader import CorpusLoader
from governance.deduplication import Deduplication
from schema.knowledge_base import KnowledgeBase, Metadata, DocumentRecord


from test_config import (
    PACKAGE_NO_DUPLICATES,
    PACKAGE_DUPLICATES,
    PACKAGE_KB_DUPLICATES,
)


def create_test_environment(package_path: Path):
    """
    Create a reusable test environment.
    """

    loader = CorpusLoader()

    snapshot = loader.load(str(package_path))

    knowledge_base = KnowledgeBase(
        metadata=Metadata(
            collection_name="test_collection"
        )
    )

    deduplication = Deduplication()

    return snapshot, knowledge_base, deduplication


def test_no_duplicates():
    """
    Test deduplication when no duplicate documents exist.
    """

    # Arrange
    snapshot, knowledge_base, deduplication = create_test_environment(
        PACKAGE_NO_DUPLICATES
    )

    # Act
    result = deduplication.deduplicate(
        snapshot,
        knowledge_base,
    )

    # Assert
    assert len(result.documents) == len(snapshot.documents)
    assert len(result.chunks) == len(snapshot.chunks)
    assert len(result.skipped_documents) == 0

    print("✓ test_no_duplicates passed")


def test_package_duplicates():
    """
    Test duplicate removal inside a corpus package.
    """

    # Arrange
    snapshot, knowledge_base, deduplication = create_test_environment(
        PACKAGE_DUPLICATES
    )

    # Act
    result = deduplication.deduplicate(
        snapshot,
        knowledge_base,
    )

    # Assert

    # One duplicate document should be removed.
    assert len(result.documents) == len(snapshot.documents) - 1

    # Removed document should also remove its chunks.
    assert len(result.chunks) < len(snapshot.chunks)

    # Exactly one document should be skipped.
    assert len(result.skipped_documents) == 1

    # Verify the skipped document.
    assert (
        "华锦股份：2025年年度报告摘要"
        in result.skipped_documents
    )

    # Verify document count consistency.
    assert (
        len(result.documents)
        + len(result.skipped_documents)
        == len(snapshot.documents)
    )

    print("✓ test_package_duplicates passed")


def test_knowledge_base_duplicates():
    """
    Test duplicate removal against the knowledge base.
    """

    # Arrange
    snapshot, knowledge_base, deduplication = create_test_environment(
        PACKAGE_KB_DUPLICATES
    )

    # Simulate an existing document in the knowledge base.
    knowledge_base.documents.append(
        DocumentRecord(
            doc_id="existing_document",
            document_hash=snapshot.documents[0].document_hash,
        )
    )

    # Act
    result = deduplication.deduplicate(
        snapshot,
        knowledge_base,
    )

    # Assert

    # One document should be removed.
    assert len(result.documents) == len(snapshot.documents) - 1

    # Related chunks should also be removed.
    assert len(result.chunks) < len(snapshot.chunks)

    # One document should be skipped.
    assert len(result.skipped_documents) == 1

    # Verify the skipped document is the one from the package.
    assert result.skipped_documents[0] == snapshot.documents[0].doc_id

    # Verify document count consistency.
    assert (
        len(result.documents)
        + len(result.skipped_documents)
        == len(snapshot.documents)
    )

    print("✓ test_knowledge_base_duplicates passed")


def main():

    print("=" * 60)
    print("Deduplication Test")
    print("=" * 60)

    test_no_duplicates()
    test_package_duplicates()
    test_knowledge_base_duplicates()

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()