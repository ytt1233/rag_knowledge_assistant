import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")
from pathlib import Path
import shutil

from ingestion.corpus_loader import CorpusLoader
from governance.deduplication import Deduplication
from governance.knowledge_base_manager import KnowledgeBaseManager
from embedding.ollama_embedding import OllamaEmbedding
from vector_store.milvus_vector_store import MilvusVectorStore
from pipeline.batch_ingestion_pipeline import BatchIngestionPipeline


def test_batch_ingestion():

    collection_name = "test_finance"

    kb_manager = KnowledgeBaseManager()

    #Step1 清理测试环境
    if kb_manager.exists(collection_name):
        shutil.rmtree(
            kb_manager._get_kb_dir(collection_name)
        )

    print("Preparing test environment...")

    #Step2 创建真实对象
    loader = CorpusLoader()

    deduplication = Deduplication()

    embedding_model = OllamaEmbedding()

    vector_store = MilvusVectorStore(collection_name=collection_name)

    pipeline = BatchIngestionPipeline(
        loader=loader,
        deduplication=deduplication,
        embedding_model=embedding_model,
        vector_store=vector_store,
        kb_manager=kb_manager,
    )
    
    package_dir = "data/corpus_packages/package_20260702_143520"

    #Step3 第一次导入
    result = pipeline.run(
        package_dir=package_dir,
        collection_name=collection_name,
    )

    #Step4 验证 KnowledgeBase
    assert kb_manager.exists(collection_name)

    kb = kb_manager.load(collection_name)

    assert kb.status.document_count == 2
    assert kb.status.chunk_count == 23
    assert kb.status.embedding_count == 23

    assert len(kb.documents) == 2

    print("KnowledgeBase verification passed.")

    #Step5 第二次导入
    result2 = pipeline.run(
        package_dir=package_dir,
        collection_name=collection_name,
    )

    #Step6 验证 Deduplication
    assert result2["documents"] == 0
    assert result2["chunks"] == 0
    assert result2["skipped_documents"] == 2

    print("Deduplication verification passed.")


def main():

    print("=" * 60)
    print("Batch Ingestion Integration Test")
    print("=" * 60)

    test_batch_ingestion()

    print("\n✓ Integration Test Passed")
    print("\nAll tests completed.")


if __name__ == "__main__":
    main()