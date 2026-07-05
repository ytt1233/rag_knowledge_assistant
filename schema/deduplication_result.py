from dataclasses import dataclass, field
from schema.chunk import Chunk
from schema.knowledge_base import DocumentRecord




@dataclass
class DeduplicationResult:
    """
    Result of the deduplication process.
    """

    documents: list[DocumentRecord] = field(default_factory=list)

    chunks: list[Chunk] = field(default_factory=list)

    skipped_documents: list[str] = field(default_factory=list)