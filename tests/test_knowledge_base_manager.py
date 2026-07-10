import sys
import json

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from pathlib import Path

import shutil

from governance.knowledge_base_manager import KnowledgeBaseManager

from schema.knowledge_base import (
    KnowledgeBase,
    Metadata,
    KnowledgeBaseStatus,
    DocumentRecord,
)


def test_init():
    """Test KnowledgeBaseManager initialization."""

    manager = KnowledgeBaseManager()

    print(f"manager.root_dir: {manager.root_dir}")

    assert manager.root_dir == Path("data/knowledge_base")

    print("✓ test_init")

def test_get_kb_dir():
    manager = KnowledgeBaseManager()

    kb_dir = manager._get_kb_dir("finance")

    print(f"Knowledge base directory: {kb_dir}")

    assert kb_dir == Path("data/knowledge_base/finance")

    print("✓ test_get_kb_dir")

def test_get_kb_dir_with_custom_root():
    manager = KnowledgeBaseManager(root_dir="test_data")

    kb_dir = manager._get_kb_dir("finance")

    assert kb_dir == Path("test_data/finance")

    print("✓ test_get_kb_dir_with_custom_root")

def test_get_kb_file():
    """
    Test getting the knowledge base JSON file path.
    """

    manager = KnowledgeBaseManager()

    kb_file = manager._get_kb_file("finance")

    print(f"Knowledge base file: {kb_file}")

    assert kb_file == Path(
        "data/knowledge_base/finance/knowledge_base.json"
    )

def test_exists():
    """
    Test checking whether a knowledge base exists.
    """

    manager = KnowledgeBaseManager(root_dir="test_data/knowledge_base")

    # 清理旧测试数据
    if manager.root_dir.exists():
        shutil.rmtree(manager.root_dir)

    # 不存在
    assert manager.exists("finance") is False

    # 创建 knowledge_base.json
    kb_dir = manager._get_kb_dir("finance")
    kb_dir.mkdir(parents=True)

    kb_file = manager._get_kb_file("finance")
    kb_file.write_text("{}")

    # 存在
    assert manager.exists("finance") is True

    # 清理
    shutil.rmtree(manager.root_dir)

def test_to_dict():
    """
    Test converting a KnowledgeBase object to a dictionary.
    """

    manager = KnowledgeBaseManager()

    kb = KnowledgeBase(
        metadata=Metadata(
            collection_name="finance",
            schema_version="1.0.0",
            created_at="2026-07-08T10:00:00"
        ),
        status=KnowledgeBaseStatus(),
        documents=[
            DocumentRecord(
                doc_id="doc_001",
                document_hash="abc123"
            )
        ]
    )

    data = manager._to_dict(kb)

    print(data)

    assert isinstance(data, dict)

    assert data["metadata"]["collection_name"] == "finance"
    assert data["metadata"]["schema_version"] == "1.0.0"

    assert data["status"]["document_count"] == 0

    assert len(data["documents"]) == 1
    assert data["documents"][0]["doc_id"] == "doc_001"
    print("✓ test_to_dict")

def test_save():
    """
    Test saving a knowledge base to disk.
    """

    manager = KnowledgeBaseManager(root_dir="test_output/knowledge_base")

    # Clean test directory
    if manager.root_dir.exists():
        shutil.rmtree(manager.root_dir)

    kb = KnowledgeBase(
        metadata=Metadata(
            collection_name="finance",
            schema_version="1.0.0",
            created_at="2026-07-08T10:00:00",
        ),
        status=KnowledgeBaseStatus(),
        documents=[
            DocumentRecord(
                doc_id="doc_001",
                document_hash="abc123",
            )
        ],
    )

    # Save
    manager.save(kb)

    kb_file = manager._get_kb_file("finance")

    print(f"Knowledge base file: {kb_file}")

    assert kb_file.exists()

    with kb_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["metadata"]["collection_name"] == "finance"
    assert data["metadata"]["schema_version"] == "1.0.0"

    assert len(data["documents"]) == 1
    assert data["documents"][0]["doc_id"] == "doc_001"

    assert data["status"]["document_count"] == 0

    # Clean
    shutil.rmtree(manager.root_dir)  

    print("✓ test_save")

def test_create():
    """
    Test creating a knowledge base.
    """

    manager = KnowledgeBaseManager(root_dir="test_output/knowledge_base")

    # Clean test directory
    if manager.root_dir.exists():
        shutil.rmtree(manager.root_dir)

    # Create knowledge base
    kb = manager.create("finance")

    print(kb)

    # Verify returned object
    assert isinstance(kb, KnowledgeBase)
    assert kb.metadata.collection_name == "finance"
    assert kb.metadata.schema_version == "1.0.0"
    assert kb.documents == []

    # Verify knowledge base directory
    kb_dir = manager._get_kb_dir("finance")
    assert kb_dir.exists()

    # Verify reports directory
    report_dir = kb_dir / "reports"
    assert report_dir.exists()

    # Verify knowledge_base.json
    kb_file = manager._get_kb_file("finance")
    assert kb_file.exists()

    # Verify exists()
    assert manager.exists("finance")

    # Clean test directory
    shutil.rmtree(manager.root_dir)

    print("✓ test_create")

def test_create_exists():
    """
    Test creating an existing knowledge base.
    """

    manager = KnowledgeBaseManager(root_dir="test_output/knowledge_base")

    if manager.root_dir.exists():
        shutil.rmtree(manager.root_dir)

    manager.create("finance")

    try:
        manager.create("finance")
        assert False, "Expected FileExistsError"

    except FileExistsError:
        print("FileExistsError raised as expected.")

    shutil.rmtree(manager.root_dir)

    print("✓ test_create_exists")

def test_from_dict():
    """
    Test converting a dictionary to a KnowledgeBase object.
    """

    manager = KnowledgeBaseManager()

    data = {
        "metadata": {
            "collection_name": "finance",
            "schema_version": "1.0.0",
            "created_at": "2026-07-08T10:00:00",
        },
        "status": {
            "document_count": 1,
            "chunk_count": 10,
            "embedding_count": 10,
            "last_ingestion_time": "",
            "last_updated_time": "",
        },
        "documents": [
            {
                "doc_id": "doc_001",
                "document_hash": "abc123",
                "status": "active",
            }
        ],
    }

    kb = manager._from_dict(data)

    print(kb)

    assert isinstance(kb, KnowledgeBase)

    assert kb.metadata.collection_name == "finance"
    assert kb.metadata.schema_version == "1.0.0"

    assert kb.status.document_count == 1

    assert len(kb.documents) == 1
    assert kb.documents[0].doc_id == "doc_001"

    print("✓ test_from_dict")

def test_load():
    """
    Test loading a knowledge base from disk.
    """

    manager = KnowledgeBaseManager(root_dir="test_output/knowledge_base")

    # Clean test directory
    if manager.root_dir.exists():
        shutil.rmtree(manager.root_dir)

    # Create a KnowledgeBase object
    kb = KnowledgeBase(
        metadata=Metadata(
            collection_name="finance",
            schema_version="1.0.0",
            created_at="2026-07-08T10:00:00",
        ),
        status=KnowledgeBaseStatus(),
        documents=[
            DocumentRecord(
                doc_id="doc_001",
                document_hash="abc123",
            )
        ],
    )

    # Save the knowledge base
    manager.save(kb)

    # Load the knowledge base
    loaded_kb = manager.load("finance")

    print(loaded_kb)

    # Verify
    assert loaded_kb == kb

    # Clean test directory
    shutil.rmtree(manager.root_dir)

    print("✓ test_load")

def test_load_not_exists():
    """
    Test loading a non-existent knowledge base.
    """

    manager = KnowledgeBaseManager(root_dir="test_output/knowledge_base")

    if manager.root_dir.exists():
        shutil.rmtree(manager.root_dir)

    try:
        manager.load("finance")
        assert False, "Expected FileNotFoundError"

    except FileNotFoundError:
        pass

    print("FileNotFoundError raised as expected.")
    
    print("✓ test_load_not_exists")
    
def main():

    print("=" * 60)
    print("KnowledgeBaseManager Test")
    print("=" * 60)

    #用于Initialization
    # test_init()

    #用于Path Utilities
    # test_get_kb_dir()
    # test_get_kb_dir_with_custom_root()
    # test_get_kb_file()

    #用于格式转换
    # test_to_dict()
    # test_from_dict()

    #用于持久化
    # test_save()
    # test_load()
    # test_load_not_exists()

    #用于生命周期管理
    # test_exists()
    # test_create()
    # test_create_exists()
    

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()