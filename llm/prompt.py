# llm/prompt.py

class PromptBuilder:

    @staticmethod
    def build(query: str, contexts: list[dict]) -> str:
        """
        构造 RAG Prompt
        """

        references = []

        for i, chunk in enumerate(contexts, 1):
            title = chunk["title"]
            page = chunk["page_num"]
            text = chunk["text"]

            references.append(
                f"""
                标题：{title}
                页码：{page}
                内容：
                {text}
                """
            )

        context = "\n\n".join(references)

        prompt = f"""你是一名专业的企业知识助手。

        请严格依据提供的参考资料回答问题。

        要求：
        1. 不允许编造答案；
        2. 如果参考资料中无法找到答案，请明确说明“未找到相关信息”；
        3. 回答要准确、简洁。
        4. 请不要在回答中使用“参考资料1”“参考资料2”等字样
        5. 直接给出答案

        参考资料：
        {context}

        用户问题：
        {query}

        请开始回答：
        """

        return prompt