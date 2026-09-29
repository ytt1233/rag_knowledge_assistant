from dataclasses import dataclass, field
from schema.metadata import Metadata
from typing import Dict, Any, Optional


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    page_num: int
    metadata: Metadata
    structure_context: Dict[str, Any] = field(default_factory=dict)#结构上下文