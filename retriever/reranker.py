# retriever/reranker.py

from FlagEmbedding import FlagReranker


class Reranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3"
    ):
        """
        BGE Reranker
        """
        # self.reranker = FlagReranker(
        #     model_name,
        #     use_fp16=False
        # )
        self.reranker = FlagReranker(
            r"D:\models\bge-reranker-v2-m3",
            use_fp16=False
)
    def rerank(
        self,
        query: str,
        retrieved_chunks: list[dict],
        top_k: int = 3
    ):
        """
        对 Milvus 检索结果重新排序
        """

        if not retrieved_chunks:
            return []

        pairs = [
            [query, chunk["text"]]
            for chunk in retrieved_chunks
        ]

        scores = self.reranker.compute_score(
            pairs,
            normalize=True
        )

        for chunk, score in zip(
            retrieved_chunks,
            scores
        ):
            chunk["rerank_score"] = score

        reranked_results = sorted(
            retrieved_chunks,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k]