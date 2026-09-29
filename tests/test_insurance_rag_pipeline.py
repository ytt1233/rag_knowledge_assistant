import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from rag.pipeline import RAGPipeline

from embedding.ollama_embedding import OllamaEmbedding
from vector_store.milvus_vector_store import MilvusVectorStore
from reranker.flag_embedding_reranker import FlagEmbeddingReranker
from generator.ollama_generator import OllamaGenerator
from generator.deepseek_generator import DeepSeekGenerator
from generator.prompt_builder import PromptBuilder

from schema.response import SearchResultResponse

DEFAULT_COLLECTION = "insurance"

embedding_model = OllamaEmbedding()

vector_store = MilvusVectorStore(
    collection_name = DEFAULT_COLLECTION
)

reranker = FlagEmbeddingReranker()

# generator = OllamaGenerator()
generator = DeepSeekGenerator()

pipeline = RAGPipeline(
    embedding_model=embedding_model,
    vector_store=vector_store,
    reranker=reranker,
    generator=generator,
)


def main():
    QUERY = "去巴厘岛潜水出现意外受伤"

    filters = 'structure_path LIKE "责任免除%"'
    result1 = pipeline.search(
        query=QUERY,
        filters=filters,
    )

    filters = 'structure_path LIKE "释义%"'
    result2 = pipeline.search(
        query=QUERY,
        filters=filters,
    )

    exclusion_results = [
        SearchResultResponse(
            text=result.chunk.text,
            structure_path=result.chunk.structure_context.get("structure_path"),
            page_num=result.chunk.page_num,
            title=result.chunk.metadata.get_domain("title"),
            score=result.score,
        )
        for result in result1
    ]

    definition_results = [
        SearchResultResponse(
            text=result.chunk.text,
            structure_path=result.chunk.structure_context.get("structure_path"),
            page_num=result.chunk.page_num,
            title=result.chunk.metadata.get_domain("title"),
            score=result.score,
        )
        for result in result2
    ]

    prompt = PromptBuilder.build_from_evidence(
        query=QUERY,
        exclusion_results=exclusion_results,
        definition_results=definition_results,
    )

    answer = generator.generate(prompt)

    print(f"answer:{answer}")


if __name__ == "__main__":
    main()