from dataclasses import dataclass

from schema.corpus_governance import CorpusGovernance
from schema.knowledge_base import DocumentRecord


@dataclass
class CorpusSnapshot:
    """
    Runtime representation of a Governed Corpus Package.

    This object is constructed by CorpusLoader and serves
    as the input to Knowledge Base Governance.
    """

    documents: list[DocumentRecord]
    governance: CorpusGovernance