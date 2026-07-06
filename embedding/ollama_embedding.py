from ollama import Client

from embedding.base_embedding import BaseEmbedding
from schema.chunk import Chunk
from schema.chunk_embedding import ChunkEmbedding


class OllamaEmbedding(BaseEmbedding):
    """
    Embedding implementation based on Ollama.
    """

    def __init__(
        self,
        model_name: str = "bge-m3",
        host: str = "http://localhost:11434"
    ):
        self.model_name = model_name
        self.client = Client(host=host)
        self._embedding_dim = None

    def embed(
        self,
        chunks: list[Chunk]
    ) -> list[ChunkEmbedding]:
        """
        Generate embeddings for chunks.
        """
        if not chunks:
            return []
        
        texts = [
            chunk.text
            for chunk in chunks
        ]

        response = self.client.embed(
            model=self.model_name,
            input=texts
        )

        return [
            ChunkEmbedding(
                chunk=chunk,
                embedding=embedding
            )
            for chunk, embedding in zip(
                chunks,
                response.embeddings
            )
        ]

    @property
    def embedding_dim(self) -> int:
        """
        Return embedding dimension.
        """

        if self._embedding_dim is None:
            self._embedding_dim = len(
                self.client.embed(
                    model=self.model_name,
                    input=["test"]
                ).embeddings[0]
            )

        return self._embedding_dim