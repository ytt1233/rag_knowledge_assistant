from fastapi import FastAPI

from schema.request import ChatRequest
from schema.response import ChatResponse

from rag.pipeline import RAGPipeline

app = FastAPI(
    title="RAG Knowledge Assistant"
)

pipeline = RAGPipeline()


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    result = pipeline.chat(
        request.query
    )

    return ChatResponse(
        query=result["query"],
        answer=result["answer"],
        citations=result["citations"]
    )