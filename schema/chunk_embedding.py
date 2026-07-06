from dataclasses import dataclass
from schema.chunk import Chunk

@dataclass
class ChunkEmbedding:
    """
    Embedding representation of a chunk.
    """

    chunk: Chunk

    embedding: list[float]