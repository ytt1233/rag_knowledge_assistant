from pydantic import BaseModel


class ChatResponse(BaseModel):
    query: str
    answer: str
    citations: list[str]

class SearchResultResponse(BaseModel):

    text: str

    structure_path: str | None = None

    page_num: int | None = None

    title: str | None = None

    score: float

class SearchResponse(BaseModel):

    query: str

    results: list[SearchResultResponse]

class AnswerResponse(BaseModel):
    query: str
    answer: str