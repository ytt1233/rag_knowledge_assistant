from abc import ABC, abstractmethod

from schema.chunk import Chunk
from schema.chunk_embedding import ChunkEmbedding


class BaseEmbedding(ABC):
    """
    Base interface for embedding models.
    """

    @abstractmethod
    def embed(
        self,
        chunks: list[Chunk]
    ) -> list[ChunkEmbedding]:
        """
        Generate embeddings for chunks.

        Args:
            chunks: List of chunks to embed.

        Returns:
            List of chunk embeddings.
        """
        pass