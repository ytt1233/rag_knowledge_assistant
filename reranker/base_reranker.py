from abc import ABC, abstractmethod

from schema.search_result import SearchResult


class BaseReranker(ABC):
    """
    Abstract interface for reranking retrieved results.
    """

    @abstractmethod
    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int | None = None
    ) -> list[SearchResult]:
        """
        Rerank retrieved search results.

        Args:
            query:
                User query.

            results:
                Retrieved search results.

            top_k:
                Number of results to keep after reranking.
                If None, return all reranked results.

        Returns:
            A reranked list of SearchResult.
        """
        pass