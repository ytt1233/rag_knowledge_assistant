from dataclasses import dataclass

from schema.chunk import Chunk


@dataclass
class SearchResult:
    """
    Search result returned by a vector store.
    """

    chunk: Chunk

    score: float