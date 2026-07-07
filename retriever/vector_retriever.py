from embedding.base_embedding import BaseEmbedding
from retriever.base_retriever import BaseRetriever
from schema.search_result import SearchResult
from vector_store.base_vector_store import BaseVectorStore


class VectorRetriever(BaseRetriever):
    """
    Retriever based on vector similarity search.
    """

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, str] | None = None
    ) -> list[SearchResult]:
        """
        Retrieve the most relevant chunks for a query.
        """

        query_embedding = self.embedding_model.embed_query(
            query
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters
        )