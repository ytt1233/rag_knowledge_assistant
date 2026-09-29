from schema.search_result import SearchResult
from schema.response import SearchResultResponse


class PromptBuilder:
    """
    Build prompts for the language model.
    """
    #通用rag问答
    @staticmethod
    def build(
        query: str,
        results: list[SearchResult]
    ) -> str:

        contexts = []

        for index, result in enumerate(results, start=1):
            contexts.append(
                f"[{index}]\n"
                f"结构路径：{result.chunk.structure_context.get('structure_path', '')}\n"
                f"内容：{result.chunk.text}"
            )

        context = "\n\n".join(contexts)

        prompt = f"""
            你是一个基于知识库进行问答的 AI 助手。

            请根据提供的知识库内容回答用户问题。

            知识库内容：
            -------
            {context}

            问题：
            -------
            {query}

            回答要求：
            -------
            1. 仅根据提供的知识库内容回答，不要使用知识库之外的信息进行推测。
            2. 如果知识库内容不足以回答问题，请明确说明“知识库中没有足够的信息”。
            3. 回答时优先使用与问题最相关的知识内容。
            4. 如果引用知识库内容，请注明对应的结构路径。
            5. 不要虚构知识库中不存在的事实。

            请按照以下格式回答：

            答案：
            <根据知识库内容给出的回答>

            依据：
            <引用相关知识库内容，并注明结构路径>
            """

        return prompt
    
    #用于保险条款中判断用户描述的保险事故/事实是否属于责任免除
    @staticmethod
    def build_from_evidence(
        query: str,
        exclusion_results: list[SearchResultResponse],
        definition_results: list[SearchResultResponse],
    ):

        exclusion_contexts = []

        for index, result in enumerate(exclusion_results, start=1):
            exclusion_contexts.append(
                f"[{index}]\n"
                f"结构路径：{result.structure_path or ''}\n"
                f"条款内容：{result.text}"
            )

        exclusion_context = "\n\n".join(exclusion_contexts)

        definition_contexts = []

        for index, result in enumerate(definition_results, start=1):
            definition_contexts.append(
                f"[{index}]\n"
                f"结构路径：{result.structure_path or ''}\n"
                f"条款内容：{result.text}"
            )

        definition_context = "\n\n".join(definition_contexts)

        return PromptBuilder._build_prompt(
            query=query,
            exclusion_context=exclusion_context,
            definition_context=definition_context,
        )

    @staticmethod
    def _build_prompt(
        query: str,
        exclusion_context: str,
        definition_context: str,
    ) -> str:

        prompt = f"""
        保险条款：
        -------

        【责任免除条款】
        {exclusion_context}

        【释义条款】
        {definition_context}

        问题：
        --------
        {query}

        任务：
        --------
        请判断用户描述的事实是否属于保险条款明确规定的责任免除情形。

        你的判断对象是“用户描述的保险事故/事实”，
        而不是用户提问的句式。

        无论用户使用“赔吗”“能赔吗”“是否赔偿”“属于免责吗”
        还是其他问法，都应根据保险条款判断该事实是否属于责任免除。

        判断依据：

        1. 责任免除条款
        是判断 EXCLUSION 的直接依据。
        只有当用户描述的事实与责任免除条款形成明确匹配时，
        才能判断为 EXCLUSION。

        2. 保险责任条款
        是判断 NOT_EXCLUSION 的直接依据。
        只有当保险责任条款能够直接支持用户描述的事实时，
        才能判断为 NOT_EXCLUSION。

        3. 释义条款
        只能用于解释保险条款中的专业术语，
        或判断用户描述的事实是否符合相关专业术语的定义。

        释义条款本身不能单独证明 EXCLUSION，
        也不能单独证明 NOT_EXCLUSION。
        不能因为现有【责任免除条款】中没有找到匹配，
        就直接判断为 NOT_EXCLUSION

        证据使用规则：

        - 如果结论为 EXCLUSION，
          “依据”必须引用能够直接构成责任免除的【责任免除条款】。
          【释义条款】只能作为辅助证据，
          用于说明用户描述的事实与责任免除条款中的专业术语之间的对应关系。

        - 如果结论为 NOT_EXCLUSION，
          “依据”必须引用能够直接支持该结论的【保险责任条款】。
          仅有【释义条款】不能得出 NOT_EXCLUSION。
          当前提供的证据中没有保险责任条款时，
          不得仅根据释义条款判断 NOT_EXCLUSION。

        - 如果结论为 INSUFFICIENT_EVIDENCE：
          “依据”必须说明当前没有找到能够直接支持
          EXCLUSION 或 NOT_EXCLUSION 的条款。

          如果存在能够帮助解释用户事实的【释义条款】，
          必须单独标记为“辅助释义”，
          不得将其列为“依据”。

          如果【释义条款】能够帮助解释用户描述中的专业术语，
          可以作为“辅助释义”引用，
          但不能将释义条款本身作为 INSUFFICIENT_EVIDENCE 的直接依据。

        特别注意：

        1、如果用户事实与责任免除条款不完全匹配，
        不得因为释义条款中出现相似概念，
        就将用户事实扩展为责任免除事实。

        例如：

        用户：“喝酒后死亡”

        条款：
        “被保险人酒后驾车……期间属于责任免除”
        以及：
        “酒后驾车指……”

        不能将“喝酒后死亡”推断为“酒后驾车”。

        必须判断：
        喝酒 ≠ 酒后驾车。

        因此应返回：
        INSUFFICIENT_EVIDENCE。

        而：

        用户：“酒后驾车发生意外死亡”

        与：
        “被保险人酒后驾车……期间”
        明确匹配，

        应返回：
        EXCLUSION。

        2、另一个重要情况：

        如果用户描述的事实可以通过【释义条款】
        与某个专业术语建立对应关系，
        但该专业术语在【责任免除条款】中没有对应的免责规定，
        不能仅因为存在这种对应关系就判断为 EXCLUSION。

        例如：

        用户：“乘坐公交车发生意外受伤”

        【释义条款】说明公交车属于相关客运交通工具，
        但如果现有【责任免除条款】中没有明确规定
        “乘坐该类交通工具”属于责任免除，

        则不能根据该释义条款判断 EXCLUSION。

        当前没有保险责任条款能够直接支持 NOT_EXCLUSION 时，
        应返回：
        INSUFFICIENT_EVIDENCE。


        你的判断结论为：

        1. EXCLUSION
        2. NOT_EXCLUSION
        3. INSUFFICIENT_EVIDENCE

        请严格按照以下格式回答，不要增加其他内容：

        结论：<EXCLUSION / NOT_EXCLUSION / INSUFFICIENT_EVIDENCE>

        依据：
        <直接依据；如果没有直接依据，明确说明“未找到直接支持结论的条款”>

        辅助释义：
        <如果存在相关释义条款则引用；没有则省略>

        理由：
        <1-3句话说明判断关系，不重复依据>

        依据：
        - 如果是 EXCLUSION,引用直接支持免责的【责任免除条款】；
        - 如果使用【释义条款】进行语义桥接，将其标记为“辅助释义”；
        - 如果是 NOT_EXCLUSION,必须引用直接支持非免责的【保险责任条款】；
        - 如果是 INSUFFICIENT_EVIDENCE,说明没有找到能够直接支持
          EXCLUSION 或 NOT_EXCLUSION 的条款；
        - 不得把仅用于解释术语的【释义条款】写成直接判断依据。

        理由：
        请用 1-3 句话说明：
        1. 用户事实与相关条款是否形成明确匹配；
        2. 释义条款在判断中的作用。

        不要重复用户事实，不要重复相同理由。
        """

        print("============================== PROMPT =============================")
        print(prompt)

        return prompt