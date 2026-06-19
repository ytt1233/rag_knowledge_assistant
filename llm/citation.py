# llm/citation.py

class CitationFormatter:

    @staticmethod
    def format(chunks):
        """
        根据检索结果生成引用信息
        """

        citations = []
        seen = set()
        for chunk in chunks:
            title = chunk.get("title", "Unknown")
            page = chunk.get("page_num", "Unknown")

            key = (title, page)
            if key in seen:
                continue

            seen.add(key)
            citations.append(
                f"{title}（第{page}页）"
            )

        return citations