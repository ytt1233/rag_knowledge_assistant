from fastapi import FastAPI

from schema.request import ChatRequest
from schema.response import ChatResponse

from rag.pipeline import RAGPipeline

from embedding.ollama_embedding import OllamaEmbedding
from vector_store.milvus_vector_store import MilvusVectorStore
from reranker.flag_embedding_reranker import FlagEmbeddingReranker
from generator.ollama_generator import OllamaGenerator

DEFAULT_COLLECTION = "test_finance"

app = FastAPI(
    title="RAG Knowledge Assistant"
)

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


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    result = pipeline.chat(
        query=request.query
    )

    return ChatResponse(
        query=result["query"],
        answer=result["answer"],
        citations=result["citations"],
    )