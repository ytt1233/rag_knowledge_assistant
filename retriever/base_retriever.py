from abc import ABC, abstractmethod

from schema.search_result import SearchResult


class BaseRetriever(ABC):
    """
    Abstract interface for document retrieval.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, str] | None = None
    ) -> list[SearchResult]:
        """
        Retrieve the most relevant chunks for a query.

        Args:
            query: User query.
            top_k: Number of results to retrieve.
            filters: Optional metadata filters.

        Returns:
            A list of SearchResult objects.
        """
        pass