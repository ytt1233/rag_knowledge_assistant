# embeddings/embedding_model.py

from typing import List
from ollama import Client


class EmbeddingModel:
    """
    Ollama Embedding Model
    """

    def __init__(
        self,
        model_name: str = "bge-m3",
        host: str = "http://localhost:11434"
    ):
        self.model_name = model_name
        self.client = Client(host=host)
        self._embedding_dim = None

    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        批量生成 embedding。

        Args:
            texts: 文本列表

        Returns:
            List[List[float]]
        """
        response = self.client.embed(
            model=self.model_name,
            input=texts
        )

        return response.embeddings

    def encode_query(self, query: str) -> List[float]:
        """
        对单个查询生成 embedding。
        """
        return self.encode([query])[0]

    @property
    def embedding_dim(self):
        if self._embedding_dim is None:
            self._embedding_dim = len(self.encode(["test"])[0])

        return self._embedding_dim