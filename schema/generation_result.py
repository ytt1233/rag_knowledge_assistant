from dataclasses import dataclass


@dataclass
class GenerationResult:
    """
    Final output of the RAG generation pipeline.
    """

    answer: str

    citations: list[str]