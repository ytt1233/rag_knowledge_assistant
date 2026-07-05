from dataclasses import dataclass, field

from dataclasses import dataclass, field


@dataclass
class DuplicateGroup:
    """
    A group of duplicate documents.

    The primary document is kept,
    while all duplicate documents are skipped.
    """

    primary_doc: str

    duplicates: list[str] = field(default_factory=list)


@dataclass
class CorpusGovernance:
    """
    Governance information produced by Project1.

    This object is read-only in Project2.
    """

    schema_version: str = "1.0.0"

    exact_duplicates: list[DuplicateGroup] = field(default_factory=list)

    cross_format_duplicates: list[DuplicateGroup] = field(default_factory=list)