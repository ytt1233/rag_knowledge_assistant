from pipeline.batch_ingestion_pipeline import (
    BatchIngestionPipeline
)

from ingestion.jsonl_loader import JSONLLoader

from embeddings.embedding_model import (
    EmbeddingModel
)

from embeddings.vector_store import (
    VectorStore
)


loader = JSONLLoader()

embedding_model = EmbeddingModel()

vector_store = VectorStore(
    collection_name="rag_chunks"
)

# 测试阶段建议重建知识库
vector_store.list_collections()
vector_store.drop_collection()
vector_store.create_collection(
    dim=embedding_model.embedding_dim
) 

pipeline = BatchIngestionPipeline(
    loader,
    embedding_model,
    vector_store
)

pipeline.run(
    "data/governed_docs"
)