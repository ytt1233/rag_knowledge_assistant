from abc import ABC, abstractmethod

from schema.chunk_embedding import ChunkEmbedding
from schema.search_result import SearchResult


class BaseVectorStore(ABC):

    @abstractmethod
    def insert(
        self,
        chunk_embeddings: list[ChunkEmbedding]
    ) -> None:
        """
        Insert chunk embeddings into the vector store.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int
    ) -> list[SearchResult]:
        """
        Search for the most similar chunks.
        """
        pass