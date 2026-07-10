from embedding.base_embedding import BaseEmbedding
from vector_store.base_vector_store import BaseVectorStore

from retriever.vector_retriever import VectorRetriever

from reranker.base_reranker import BaseReranker

from generator.base_generator import BaseGenerator
from generator.prompt_builder import PromptBuilder
from generator.citation_formatter import CitationFormatter


class RAGPipeline:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore,
        reranker: BaseReranker,
        generator: BaseGenerator,
    ):
        self.retriever = VectorRetriever(
            embedding_model=embedding_model,
            vector_store=vector_store,
        )

        self.reranker = reranker

        self.generator = generator

    def chat(
        self,
        query: str,
        top_k: int = 5,
        rerank_top_k: int = 3,
        filters: dict[str, str] | None = None,
    ) -> dict:

        # 1. Retrieval
        retrieved_results = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters,
        )

        # 2. Rerank
        reranked_results = self.reranker.rerank(
            query=query,
            results=retrieved_results,
            top_k=rerank_top_k,
        )

        # 3. Prompt
        prompt = PromptBuilder.build(
            query=query,
            results=reranked_results,
        )

        # 4. Generation
        answer = self.generator.generate(
            prompt
        )

        # 5. Citation
        citations = CitationFormatter.format(
            results=reranked_results,
        )

        return {
            "query": query,
            "answer": answer,
            "citations": citations,
        }
    