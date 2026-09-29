from pydantic import BaseModel
from schema.response import SearchResultResponse


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    rerank_top_k: int = 5
    filters: dict[str, str] | str | None = None

class SearchRequest(BaseModel):

    query: str

    top_k: int = 5

    rerank_top_k: int = 5

    filters: dict[str, str] | str | None = None


class AnswerRequest(BaseModel):

    query: str

    exclusion_results: list[SearchResultResponse]
    
    definition_results: list[SearchResultResponse]