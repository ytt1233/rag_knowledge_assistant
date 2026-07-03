from dataclasses import dataclass, field


@dataclass
class CorpusGovernance:
    """
    Governance information produced by Project1.

    This object is read-only in Project2 and represents
    governance results for a Governed Corpus Package.
    记录文档之间的重复关系
    """

    schema_version: str = "1.0.0"

    # Each inner list represents one exact duplicate group.
    exact_duplicates: list[list[str]] = field(default_factory=list)

    # Each inner list represents one cross-format duplicate group.
    cross_format_duplicates: list[list[str]] = field(default_factory=list)