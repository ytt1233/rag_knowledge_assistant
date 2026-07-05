import sys
sys.path.append(r'F:\mycode\rag_knowledge_assistant')

from ingestion.corpus_loader import CorpusLoader
from governance.deduplication import Deduplication

from schema.knowledge_base import (
    KnowledgeBase,
    Metadata,
)


def main():

    package_path = "data/corpus_packages/package_20260702_143520"

    # Load corpus package.
    loader = CorpusLoader()
    snapshot = loader.load(package_path)

    # Create an empty knowledge base.
    knowledge_base = KnowledgeBase(
        metadata=Metadata(
            collection_name="demo_knowledge_base"
        )
    )

    # Run deduplication.
    deduplication = Deduplication()

    result = deduplication.deduplicate(
        snapshot,
        knowledge_base,
    )

    print("=" * 60)
    print("Deduplication Result")
    print("=" * 60)

    print(f"Documents: {len(result.documents)}")
    print(f"Chunks: {len(result.chunks)}")
    print(f"Skipped Documents: {len(result.skipped_documents)}")

    print()

    print("Document IDs:")

    for document in result.documents:
        print(f"  - {document.doc_id}")


if __name__ == "__main__":
    main()