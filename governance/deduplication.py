
from schema.corpus_snapshot import CorpusSnapshot
from schema.corpus_governance import DuplicateGroup 
from schema.deduplication_result import DeduplicationResult
from schema.knowledge_base import KnowledgeBase, DocumentRecord
from schema.chunk import Chunk

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
        self._remove_package_duplicates(
            documents,
            chunks,
            snapshot.governance,
            skipped_documents,
        )

        # Stage 2: Remove documents already existing in the knowledge base.
        self._remove_knowledge_base_duplicates(
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
    ) -> None:
        """
        Remove duplicate documents within the corpus package.
        """
        self._process_duplicate_groups(
            governance.exact_duplicates,
            documents,
            chunks,
            skipped_documents,
        )

        self._process_duplicate_groups(
            governance.cross_format_duplicates,
            documents,
            chunks,
            skipped_documents,
        )
 

    def _remove_knowledge_base_duplicates(
        self,
        documents: list[DocumentRecord],
        chunks: list[Chunk],
        knowledge_base: KnowledgeBase,
        skipped_documents: list[str],
    ) -> None:
        """
        Remove documents that already exist in the knowledge base.
        """

        for document in documents.copy():

            for kb_document in knowledge_base.documents:

                if document.document_hash == kb_document.document_hash:

                    self._remove_document(
                        document.doc_id,
                        documents,
                        chunks,
                        skipped_documents,
                    )

                    break
    

    def _process_duplicate_groups(
        self,
        duplicate_groups: list[DuplicateGroup],
        documents: list[DocumentRecord],
        chunks: list[Chunk],
        skipped_documents: list[str],
    ):
        """
        Remove duplicate documents defined by duplicate groups.
        """

        for group in duplicate_groups:
            for duplicate in group.duplicates:
                self._remove_document(
                    duplicate,
                    documents,
                    chunks,
                    skipped_documents,
                )

    def _remove_document(
        self,
        doc_id: str,
        documents: list[DocumentRecord],
        chunks: list[Chunk],
        skipped_documents: list[str],
    ):
        """
        Remove a document and all its associated chunks.
        """

        before_count = len(documents)

        # Remove the document.
        documents[:] = [
            document
            for document in documents
            if document.doc_id != doc_id
        ]

        # Remove all associated chunks.
        chunks[:] = [
            chunk
            for chunk in chunks
            if chunk.doc_id != doc_id
        ]

        # Record only if a document was actually removed.
        if len(documents) < before_count:
            skipped_documents.append(doc_id)