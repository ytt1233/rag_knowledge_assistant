import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from rag.pipeline import RAGPipeline

from embedding.ollama_embedding import OllamaEmbedding
from vector_store.milvus_vector_store import MilvusVectorStore
from reranker.flag_embedding_reranker import FlagEmbeddingReranker
from generator.ollama_generator import OllamaGenerator
from rag.pipeline import RAGPipeline

DEFAULT_COLLECTION = "insurance"

embedding_model = OllamaEmbedding()

vector_store = MilvusVectorStore(
    collection_name = DEFAULT_COLLECTION
)

reranker = FlagEmbeddingReranker()

generator = OllamaGenerator()

pipeline = RAGPipeline(
    embedding_model=embedding_model,
    vector_store=vector_store,
    reranker=reranker,
    generator=generator,
)

QUERY = "什么是高风险运动"
def main():
    result = pipeline.chat(
        query= QUERY,
    )

    print(f'回答:{result["answer"]}')
    print(f'引用:{result["citations"]}')




if __name__ == "__main__":
    main()