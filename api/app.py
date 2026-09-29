from fastapi import FastAPI

from schema.request import ChatRequest, SearchRequest, AnswerRequest
from schema.response import ChatResponse, SearchResponse, SearchResultResponse, AnswerResponse

from rag.pipeline import RAGPipeline

from embedding.ollama_embedding import OllamaEmbedding
from vector_store.milvus_vector_store import MilvusVectorStore
from reranker.flag_embedding_reranker import FlagEmbeddingReranker
from generator.ollama_generator import OllamaGenerator
from generator.prompt_builder import PromptBuilder
from generator.deepseek_generator import DeepSeekGenerator

DEFAULT_COLLECTION = "insurance"

app = FastAPI(
    title="RAG Knowledge Assistant"
)

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


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    result = pipeline.chat(
        query=request.query,
        top_k=request.top_k,
        rerank_top_k=request.rerank_top_k,
        filters=request.filters,
    )

    return ChatResponse(
        query=result["query"],
        answer=result["answer"],
        citations=result["citations"],
    )

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    results = pipeline.search(
        query=request.query,
        top_k=request.top_k,
        rerank_top_k=request.rerank_top_k,
        filters=request.filters,
    )

    return SearchResponse(
        query=request.query,
        results=[
            SearchResultResponse(
                text=result.chunk.text,
                structure_path=result.chunk.structure_context.get("structure_path"),
                page_num=result.chunk.page_num,
                title=result.chunk.metadata.get_domain("title"),
                score=result.score,
            )
            for result in results
        ],
    )

@app.post("/answer", response_model=AnswerResponse)
def answer(request: AnswerRequest):

    prompt = PromptBuilder.build_from_evidence(
        query=request.query,
        exclusion_results=request.exclusion_results,
        definition_results=request.definition_results,
    )

    answer = generator.generate(prompt)

    return AnswerResponse(
        query=request.query,
        answer=answer,
    )

