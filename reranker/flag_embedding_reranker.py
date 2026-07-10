from FlagEmbedding import FlagReranker

from reranker.base_reranker import BaseReranker
from schema.search_result import SearchResult


class FlagEmbeddingReranker(BaseReranker):
    """
    Reranker implementation based on FlagEmbedding.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3",
        use_fp16: bool = False
    ):
        self.reranker = FlagReranker(
            r"D:\models\bge-reranker-v2-m3",
            use_fp16=use_fp16
        )

    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int | None = None
    ) -> list[SearchResult]:
        """
        Rerank retrieved search results.
        """
        if top_k is not None and top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        if not results:
            return []

        pairs = [
            [
                query,
                result.chunk.text
            ]
            for result in results
        ]

        reranker = self.reranker
        scores = reranker.compute_score(
            pairs,
            normalize=True
        )

        for result, score in zip(
            results,
            scores
        ):
            result.score = score

        reranked_results = sorted(
            results,
            key=lambda result: result.score,
            reverse=True
        )

        if top_k is not None:
            reranked_results = reranked_results[:top_k]

        return reranked_results