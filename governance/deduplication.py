
from schema.corpus_snapshot import CorpusSnapshot
from schema.deduplication_result import DeduplicationResult
from schema.knowledge_base import KnowledgeBase

class Deduplication:
    """
    Remove duplicate documents before ingestion into the knowledge base.

    Deduplication consists of two stages:

    1. Remove duplicate documents inside the corpus package.
    2. Remove documents already existing in the knowledge base.
    """

    def deduplicate(
        self,
        snapshot: CorpusSnapshot,
        knowledge_base: KnowledgeBase,
    ) -> DeduplicationResult:
        """
        Remove duplicate documents before ingestion.
        """

        # Create working copies.
        documents = snapshot.documents.copy()
        chunks = snapshot.chunks.copy()

        # Collector.
        skipped_documents = []

        # Stage 1: Remove duplicates inside the corpus package.
        documents, chunks = self._remove_package_duplicates(
            documents,
            chunks,
            snapshot.governance,
            skipped_documents,
        )

        # Stage 2: Remove documents already existing in the knowledge base.
        documents, chunks = self._remove_knowledge_base_duplicates(
            documents,
            chunks,
            knowledge_base,
            skipped_documents,
        )

        return DeduplicationResult(
            documents=documents,
            chunks=chunks,
            skipped_documents=skipped_documents,
        )

    def _remove_package_duplicates(
        self,
        documents,
        chunks,
        governance,
        skipped_documents,
    ):
        """
        Remove duplicate documents within the corpus package.
        """
        pass
        return documents, chunks

    def _remove_knowledge_base_duplicates(
        self,
        documents,
        chunks,
        knowledge_base,
        skipped_documents,
    ):
        """
        Remove documents that already exist in the knowledge base.
        """
        pass
        return documents, chunks