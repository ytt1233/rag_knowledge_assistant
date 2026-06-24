from embeddings.embedding_model import EmbeddingModel
from embeddings.vector_store import VectorStore

embedding_model = EmbeddingModel()
vector_store = VectorStore()

query_embedding = embedding_model.encode_query(
    "重点行业大客户满意度评分是多少"
)

# results = vector_store.search(
#     query_embedding=query_embedding,
#     category="规划",
#     top_k=3
# )

results = vector_store.search(
    query_embedding=query_embedding,
    title="宏达智能科技公司",
    top_k=3
)

for r in results:
    print(r["category"])
    print(r["title"])
    print(r["score"])
    print(r["text"])