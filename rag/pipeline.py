from embeddings.embedding_model import EmbeddingModel
from embeddings.vector_store import VectorStore
from retriever.semantic_retriever import SemanticRetriever
from retriever.reranker import Reranker
from llm.prompt import PromptBuilder
from llm.generator import Generator
from llm.citation import CitationFormatter


class RAGPipeline:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.vector_store = VectorStore()

        self.retriever = SemanticRetriever(
            self.embedder,
            self.vector_store
        )

        self.reranker = Reranker()

        self.generator = Generator()

    def chat(self, query: str):

        semantic_results = self.retriever.retrieve(
            query=query,
            top_k=5
        )

        rerank_results = self.reranker.rerank(
            query=query,
            retrieved_chunks=semantic_results,
            top_k=3
        )

        prompt = PromptBuilder.build(
            query=query,
            contexts=rerank_results
        )

        answer = self.generator.generate(
            prompt
        )

        citations = CitationFormatter.format(
            rerank_results
        )

        return {
            "query": query,
            "answer": answer,
            "citations": citations
        }