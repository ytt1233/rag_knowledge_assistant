from dataclasses import dataclass, field

@dataclass
class Metadata:
    """
    Metadata describing the knowledge base itself.

    This metadata belongs to the knowledge base rather than
    individual documents.
    """

    collection_name: str
    schema_version: str = "1.2.0"
    created_at: str = ""
    updated_at: str = ""

@dataclass
class DocumentRecord:
    """
    Metadata of a document managed by the knowledge base.

    status:
        active
        deleted
        archived
    """
    doc_id: str
    document_hash: str
    status: str = "active"

@dataclass
class KnowledgeBaseStatus:
    """
    Current statistics of the knowledge base.
    """

    document_count: int = 0
    chunk_count: int = 0
    embedding_count: int = 0

    last_ingestion_time: str = ""
    last_updated_time: str = ""

@dataclass
class KnowledgeBaseGovernance:
    """
    Governance results of the knowledge base.
    """

    duplicate_skipped: int = 0
    incremental_added: int = 0
    incremental_updated: int = 0

@dataclass
class KnowledgeBase:
    """
    A governed business knowledge base.
    """

    metadata: Metadata

    status: KnowledgeBaseStatus = field(default_factory=KnowledgeBaseStatus)

    governance: KnowledgeBaseGovernance = field(default_factory=KnowledgeBaseGovernance)

    documents: list[DocumentRecord] = field(default_factory=list)