from schema.search_result import SearchResult


class PromptBuilder:
    """
    Build prompts for the language model.
    """

    @staticmethod
    def build(
        query: str,
        results: list[SearchResult]
    ) -> str:

        contexts = []

        for index, result in enumerate(results, start=1):
            contexts.append(
                f"[{index}]\n{result.chunk.text}"
            )

        context = "\n\n".join(contexts)

        prompt = f"""You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

Do NOT use your own knowledge.

If the answer cannot be found completely in the context, reply exactly:

"I don't know based on the provided context."

Context
-------
{context}

Question
--------
{query}

Answer
------
"""

        return prompt