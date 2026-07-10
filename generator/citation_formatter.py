from schema.search_result import SearchResult


class CitationFormatter:
    """
    Format citations from retrieved search results.
    """

    @staticmethod
    def format(
        results: list[SearchResult]
    ) -> list[str]:
        """
        Generate unique citations from search results.
        """

        citations = []
        seen = set()

        for result in results:

            title = result.chunk.metadata.get_domain(
                "title",
                "Unknown"
            )

            page = result.chunk.page_num

            key = (
                title,
                page
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                f"{title} (Page {page})"
            )

        return citations