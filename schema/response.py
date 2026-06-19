from pydantic import BaseModel
from typing import List


class ChatResponse(BaseModel):
    query: str
    answer: str
    citations: List[str]