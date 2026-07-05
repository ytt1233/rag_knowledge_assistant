from ingestion.jsonl_loader import JSONLLoader
from pathlib import Path
import json

from schema.corpus_snapshot import CorpusSnapshot
from schema.corpus_governance import CorpusGovernance
from schema.knowledge_base import DocumentRecord
from schema.chunk import Chunk
from schema.corpus_governance import CorpusGovernance,DuplicateGroup


class CorpusLoader:
    """
    Load a Governed Corpus Package into a runtime CorpusSnapshot.

    Responsibilities:
        - Load governed documents.
        - Load governance information.
        - Build a CorpusSnapshot.

    This loader does NOT perform:
        - Deduplication
        - Incremental ingestion
        - Embedding generation
        - Knowledge base updates
        - Milvus operations
    """
    def __init__(self):
        self.jsonl_loader = JSONLLoader()

    def load(self, package_path: str) -> CorpusSnapshot:
        """
        Load a Governed Corpus Package.

        Args:
            package_path: Path to the Governed Corpus Package.

        Returns:
            A runtime CorpusSnapshot.
        """
        documents, chunks = self._load_documents(package_path)

        governance = self._load_governance(package_path)

        return CorpusSnapshot(
            documents=documents,
            chunks=chunks,
            governance=governance,
        )

    def _load_documents(
        self,
        package_path: str,
    ) -> list[DocumentRecord]:
        """
        Load all governed documents from a Governed Corpus Package.

        Args:
            package_path: Path to the package.

        Returns:
            A list of DocumentRecord objects.
        """
        documents: list[DocumentRecord] = []
        all_chunks = []

        governed_docs_dir = Path(package_path) / "governed_docs"
        print(f'package_path:{Path(package_path) }')

        if not governed_docs_dir.exists():
            raise FileNotFoundError(
                f"Governed documents directory not found: {governed_docs_dir}"
            )

        for jsonl_file in governed_docs_dir.glob("*.jsonl"):

            chunks = self.jsonl_loader.load(str(jsonl_file))

            all_chunks.extend(chunks)

            documents.extend(
                self._build_document_records(chunks)
            )

        return documents, all_chunks

    def _build_document_records(
        self,
        chunks: list[Chunk],
    ) -> list[DocumentRecord]:
        """
        Aggregate chunk-level data into document-level records.

        Args:
            chunks: All chunks loaded from a JSONL file.

        Returns:
            A list of DocumentRecord objects.
        """

        document_map: dict[str, Chunk] = {}

        for chunk in chunks:
            if chunk.doc_id not in document_map:
                document_map[chunk.doc_id] = chunk

        return [
            self._create_document_record(chunk)
            for chunk in document_map.values()
        ]



    def _create_document_record(
        self,
        chunk: Chunk,
    ) -> DocumentRecord:
        """
        Create a DocumentRecord from a chunk.

        Args:
            chunk: A chunk belonging to a governed document.

        Returns:
            A DocumentRecord.

        Raises:
            ValueError:
                If required metadata is missing.
        """

        doc_id = chunk.doc_id

        document_hash = chunk.metadata.common.get("document_hash")

        if not doc_id:
            raise ValueError("Missing required field: doc_id")

        if not document_hash:
            raise ValueError(
                f"Document '{doc_id}' is missing required metadata: document_hash"
            )

        return DocumentRecord(
            doc_id=doc_id,
            document_hash=document_hash,
        )
    
    def _load_governance(
        self,
        package_path: str,
    ) -> CorpusGovernance:
        """
        Load governance information from a Governed Corpus Package.

        Args:
            package_path: Path to the corpus package.

        Returns:
            A CorpusGovernance object.
        """

        governance_file = (
            Path(package_path) / "corpus_governance.json"
        )

        if not governance_file.exists():
            raise FileNotFoundError(
                f"Governance file not found: {governance_file}"
            )

        with open(governance_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        exact_duplicates = [
            DuplicateGroup(
                primary_doc=item["primary_doc"],
                duplicates=item.get("duplicates", []),
            )
            for item in data.get("exact_duplicates", [])
        ]

        cross_format_duplicates = [
            DuplicateGroup(
                primary_doc=item["primary_doc"],
                duplicates=item.get("duplicates", []),
            )
            for item in data.get("cross_format_duplicates", [])
        ]

        return CorpusGovernance(
            schema_version=data.get("schema_version", "1.0.0"),
            exact_duplicates=exact_duplicates,
            cross_format_duplicates=cross_format_duplicates,
        )