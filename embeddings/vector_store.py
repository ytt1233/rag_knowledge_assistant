# embeddings/vector_store.py

from pymilvus import MilvusClient, DataType
from schema.chunk import Chunk


class VectorStore:

    def __init__(
        self,
        uri: str = "http://localhost:19530",
        collection_name: str = "rag_chunks"
    ):
        self.collection_name = collection_name
        self.client = MilvusClient(uri=uri)

    def create_collection(self, dim: int = 1024):
        """
        创建 Collection。
        """

        if self.client.has_collection(
            collection_name=self.collection_name
        ):
            print(
                f"Collection '{self.collection_name}' already exists."
            )
            return

        schema = self.client.create_schema( 
            auto_id=False,
            enable_dynamic_field=False
        )

        schema.add_field(
            field_name="chunk_id",
            datatype=DataType.VARCHAR,
            is_primary=True,
            max_length=100
        )

        schema.add_field(
            field_name="doc_id",
            datatype=DataType.VARCHAR,
            max_length=255
        )

        schema.add_field(
            field_name="text",
            datatype=DataType.VARCHAR,
            max_length=65535
        )

        schema.add_field(
            field_name="page_num",
            datatype=DataType.INT64
        )

        schema.add_field(
            field_name="title",
            datatype=DataType.VARCHAR,
            max_length=512
        )

        schema.add_field(
            field_name="category",
            datatype=DataType.VARCHAR,
            max_length=128
        )

        schema.add_field(
            field_name="embedding",
            datatype=DataType.FLOAT_VECTOR,
            dim=dim
        )

        index_params = self.client.prepare_index_params()

        index_params.add_index(
            field_name="embedding",
            metric_type="COSINE",
            index_type="HNSW",
            index_name="embedding_index",
            params={
                "M": 16,
                "efConstruction": 200
            }
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params
        )

        print(
            f"Collection '{self.collection_name}' created successfully."
        )

    def insert(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]]
    ):
        """
        插入数据
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                "chunks 与 embeddings 数量不一致"
            )

        data = []

        for chunk, embedding in zip(chunks, embeddings):
            data.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "doc_id": chunk.doc_id,
                    "text": chunk.text,
                    "page_num": chunk.page_num,
                    "title": chunk.metadata.get_domain(
                        "title", ""
                    ),
                    "category": chunk.metadata.get_domain(
                        "category", ""
                    ),
                    "embedding": embedding,
                }
            )

        self.client.insert(
            collection_name=self.collection_name,
            data=data
        )

        print(
            f"Inserted {len(data)} records."
        )

    def drop_collection(self):
        """
        删除 Collection
        """

        if self.client.has_collection(
                collection_name=self.collection_name):

            self.client.drop_collection(
                collection_name=self.collection_name
            )

            print(
                f"Collection '{self.collection_name}' dropped."
            )
        else:
            print(
                f"Collection '{self.collection_name}' does not exist."
            )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ):
        """
        Milvus语义检索
        """

        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_embedding],
            limit=top_k,
            search_params={
                "metric_type": "COSINE"
            },
            output_fields=[
                "chunk_id",
                "doc_id",
                "text",
                "page_num",
                "title",
                "category"
            ]
        )

        retrieved_chunks = []

        for hit in results[0]:
            entity = hit["entity"]

            retrieved_chunks.append(
                {
                    "chunk_id": entity["chunk_id"],
                    "doc_id": entity["doc_id"],
                    "text": entity["text"],
                    "page_num": entity["page_num"],
                    "title": entity["title"],
                    "category": entity["category"],
                    "score": hit["distance"]
                }
            )

        return retrieved_chunks