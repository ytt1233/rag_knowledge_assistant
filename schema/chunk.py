from dataclasses import dataclass
from schema.metadata import Metadata


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    page_num: int
    metadata: Metadata