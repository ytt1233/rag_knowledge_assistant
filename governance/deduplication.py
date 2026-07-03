from schema.corpus_snapshot import CorpusSnapshot
from schema.knowledge_base import DocumentRecord, KnowledgeBase


class Deduplication:
    """
    Filter duplicate documents before ingestion.

    Responsibilities:
        - Skip documents marked as duplicates by Project 1 governance.
        - Skip documents already existing in the KnowledgeBase.
        - Update governance statistics.

    This class does NOT:
        - Detect duplicates
        - Import documents
        - Generate embeddings
    """

    def filter(
        self,
        kb: KnowledgeBase,
        snapshot: CorpusSnapshot,
    ) -> list[DocumentRecord]:
        """
        Filter duplicate documents.

        Args:
            kb: Current knowledge base.
            snapshot: Governed corpus snapshot.

        Returns:
            Documents ready for incremental ingestion.
        """

        documents = self._filter_governance_duplicates(snapshot)

        documents = self._filter_kb_duplicates(
            kb,
            documents,
        )

        return documents

    def _filter_governance_duplicates(
        self,
        snapshot: CorpusSnapshot,
    ) -> list[DocumentRecord]:
        """
        Remove documents already identified as duplicates by Project 1.
        """

        skip_documents = (
            set(snapshot.governance.exact_duplicates)
            | set(snapshot.governance.cross_format_duplicates)
        )

        filtered = []

        skipped = 0

        for document in snapshot.documents:

            if document.doc_id in skip_documents:
                skipped += 1
                continue

            filtered.append(document)

        snapshot.governance.duplicate_skipped = skipped

        return filtered

    def _filter_kb_duplicates(
        self,
        kb: KnowledgeBase,
        documents: list[DocumentRecord],
    ) -> list[DocumentRecord]:
        """
        Remove documents already existing in the KnowledgeBase.
        """

        existing_hashes = self._build_hash_set(kb)

        filtered = []

        skipped = 0

        for document in documents:

            if document.document_hash in existing_hashes:
                skipped += 1
                continue

            filtered.append(document)

        kb.governance.duplicate_skipped += skipped

        return filtered

    @staticmethod
    def _build_hash_set(
        kb: KnowledgeBase,
    ) -> set[str]:
        """
        Build a hash set from existing documents.
        """

        return {
            document.document_hash
            for document in kb.documents
        }