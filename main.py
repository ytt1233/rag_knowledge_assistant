from ingestion.jsonl_loader import JSONLLoader
from embeddings.embedding_model import EmbeddingModel


loader = JSONLLoader()

chunks = loader.load(
    "data/governed_docs/华锦股份：2025年年度报告摘要.jsonl"
)

texts = [chunk.text for chunk in chunks]

embedder = EmbeddingModel()

embeddings = embedder.encode(texts)

print("Chunk数量:", len(chunks))
print("Embedding数量:", len(embeddings))
print("Embedding维度:", len(embeddings[0]))