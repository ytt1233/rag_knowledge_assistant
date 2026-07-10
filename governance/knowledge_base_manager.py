from datetime import datetime
from pathlib import Path
from dataclasses import asdict
import json

from schema.knowledge_base import (
    KnowledgeBase,
    KnowledgeBaseStatus,
    Metadata,
    DocumentRecord
)


class KnowledgeBaseManager:
    """
    Lifecycle manager for KnowledgeBase.

    Responsibilities:
    - Create a knowledge base.
    - Load a knowledge base.
    - Save a knowledge base.

    Not responsible for:
    - Milvus operations
    - Batch ingestion
    - Deduplication
    - Retrieval
    """

    def __init__(self, root_dir: str | Path = "data/knowledge_base"):
        """
        Initialize the knowledge base manager.

        Args:
            root_dir: Root directory for all knowledge bases.
        """
        self.root_dir = Path(root_dir)
        
    def _get_kb_dir(self, collection_name: str) -> Path:
        """
        Get the directory of a knowledge base.

        Args:
            collection_name: Collection name.   

        Returns:
            Path to the knowledge base directory.
        """
        return self.root_dir / collection_name
    def _get_kb_file(self, collection_name: str) -> Path:
        """
        Get the knowledge base JSON file path.

        Args:
            collection_name: Collection name.

        Returns:
            Path to the knowledge base JSON file.
        """
        return self._get_kb_dir(collection_name) / "knowledge_base.json"
    
    def save(
        self,
        knowledge_base: KnowledgeBase,
    ) -> None:
        
        # 1、获取文件路径
        collection_name = knowledge_base.metadata.collection_name

        kb_file = self._get_kb_file(collection_name)

        # 2、确保文件目录存在
        kb_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # 3、对象转为dict
        data = self._to_dict(knowledge_base)

        # 4、写json
        with kb_file.open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )
    def create(
        self,
        collection_name: str,
        schema_version: str = "1.0.0",
    ) -> KnowledgeBase:
        
        # 1、检查是否存在
        if self.exists(collection_name):
            raise FileExistsError(
                f"Knowledge base '{collection_name}' already exists."
            )
        kb_dir = self._get_kb_dir(collection_name)

        # 2、创建目录
        kb_dir.mkdir(
            parents=True,
            exist_ok=False,
        )

        # 3、创建reports文件夹
        report_dir = kb_dir / "reports"

        report_dir.mkdir()

        # 4、创建 KnowledgeBase
        kb = KnowledgeBase(
            metadata=Metadata(
                collection_name=collection_name,
                schema_version=schema_version,
                created_at=datetime.now().isoformat(),
            ),
            status=KnowledgeBaseStatus(),
            documents=[],
        )

        # 5、保存
        self.save(kb)

        return kb
    def exists(self, collection_name: str) -> bool:
        """
        Check whether a knowledge base exists.

        Args:
            collection_name: Collection name.

        Returns:
            True if the knowledge base exists, otherwise False.
        """
        return self._get_kb_file(collection_name).exists()
    
    def _to_dict(self, knowledge_base: KnowledgeBase) -> dict:
        """
        Convert a KnowledgeBase object to a dictionary.

        Args:
            knowledge_base: KnowledgeBase instance.

        Returns:
            Dictionary representation of the KnowledgeBase.
        """   
        return asdict(knowledge_base)
    
    def _from_dict(self, data: dict) -> KnowledgeBase:
        """
        Convert a dictionary to a KnowledgeBase object.
        """

        metadata = Metadata(
            **data["metadata"]
        )

        status = KnowledgeBaseStatus(
            **data["status"]
        )

        documents = [
            DocumentRecord(**doc)
            for doc in data["documents"]
        ]

        return KnowledgeBase(
            metadata=metadata,
            status=status,
            documents=documents,
        )
    
    def load(
        self,
        collection_name: str,
    ) -> KnowledgeBase:
        """
        Load a knowledge base from disk.

        Args:
            collection_name: Knowledge base collection name.

        Returns:
            KnowledgeBase instance.

        Raises:
            FileNotFoundError:
                If the knowledge base does not exist.
        """

        kb_file = self._get_kb_file(collection_name)

        if not kb_file.exists():
            raise FileNotFoundError(
                f"Knowledge base '{collection_name}' does not exist."
            )

        with kb_file.open(
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

        return self._from_dict(data)