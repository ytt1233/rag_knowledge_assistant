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
        rerank_top_k: int = 5,
        filters: dict[str, str] | str | None = None,
    ) -> dict:
        # print("------------------------------")
        # print(f'query:{query}')
        # print(f'filters:{filters}')

        # 1. Retrieval
        retrieved_results = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters,
        )
        # for result in retrieved_results:
        #         print(f'\n 召回内容:{result.chunk.text} 分数:{result.score}  来源：第{result.chunk.page_num}页 {result.chunk.structure_context.get("structure_path",None)}')

        # 2. Rerank
        reranked_results = self.reranker.rerank(
            query=query,
            results=retrieved_results,
            top_k=rerank_top_k,
        )
        # for result in reranked_results:
        #         print(f'\n 重排内容:{result.chunk.text} 分数:{result.score} 来源：第{result.chunk.page_num}页 {result.chunk.structure_context.get("structure_path",None)}')
        
        # 3. Prompt
        prompt = PromptBuilder.build(
            query=query,
            results=reranked_results,
        )

        # 4. Generation
        answer = self.generator.generate(
            prompt
        )
        # print(f'answer:{answer}')

        # 5. Citation
        citations = CitationFormatter.format(
            results=reranked_results,
        )
        
        return {
            "query": query,
            "answer": answer,
            "citations": citations,
        }
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        rerank_top_k: int = 5,
        filters: dict[str, str] | str | None = None,
    ) -> list:

        # print("************************************")
        # print(f'query:{query}')

        # 1. Retrieval
        retrieved_results = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters,
        )

        # for result in retrieved_results:
        #     print(f'召回内容:{result.chunk.text}')

        # print(f'rerank_top_k:{rerank_top_k}')

        # 2. Rerank
        reranked_results = self.reranker.rerank(
            query=query,
            results=retrieved_results,
            top_k=rerank_top_k,
        )

        # for result in reranked_results:
        #     print(f'重排内容:{result.chunk.text} 分数:{result.score}')

        # print(f'reranked_results:{len(reranked_results)}')

        return reranked_results