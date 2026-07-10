from dataclasses import dataclass

@dataclass
class KnowledgeBaseMetrics:
    """
    Calculated metrics of the knowledge base.
    """

    duplicate_document_count: int = 0

    duplicate_rate: float = 0.0

    average_chunks_per_document: float = 0.0

    average_chunk_length: float = 0.0