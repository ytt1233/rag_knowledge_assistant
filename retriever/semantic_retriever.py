from embeddings.embedding_model import EmbeddingModel
from embeddings.vector_store import VectorStore


class SemanticRetriever:

    def __init__(
        self,
        embedder: EmbeddingModel,
        vector_store: VectorStore
    ):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):
        """
        语义检索
        """

        query_embedding = self.embedder.encode_query(
            query
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )