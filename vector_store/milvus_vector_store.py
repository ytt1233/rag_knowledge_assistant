from pymilvus import MilvusClient, DataType
from vector_store.base_vector_store import BaseVectorStore
from schema.chunk_embedding import ChunkEmbedding
from schema.search_result import SearchResult
from schema.metadata import Metadata
from schema.chunk import Chunk


class MilvusVectorStore(BaseVectorStore):

    def __init__(
        self,
        uri: str = "http://localhost:19530",
        collection_name: str = "rag_chunks"
    ):
        self.collection_name = collection_name
        self.client = MilvusClient(uri=uri)

    def has_collection(self) -> bool:
        """Check if the collection exists."""
        return self.client.has_collection(self.collection_name)

    def drop_collection(self) -> None:
        """
        删除 Collection
        """
        if self.has_collection():
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
    def create_collection(
        self,
        embedding_dim: int
    ) -> None:
        """Create a collection in Milvus."""

        if self.has_collection():
            return
        dim = embedding_dim

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
        chunk_embeddings: list[ChunkEmbedding]
    ) -> None:
        """
        Insert chunk embeddings into Milvus.
        """

        if not chunk_embeddings:
            return

        data = []

        for chunk_embedding in chunk_embeddings:

            chunk = chunk_embedding.chunk

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
                    "embedding": chunk_embedding.embedding,
                }
            )

        self.client.insert(
            collection_name=self.collection_name,
            data=data
        )

        print(
            f"Milvus: inserted {len(data)} chunks."
        )
        
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filters: dict[str, str] | None = None
    ) -> list[SearchResult]:
        """
        Search similar chunks from Milvus.

        Args:
            query_embedding: Query embedding vector.
            top_k: Number of results to return.
            filters: Optional metadata filters.

        Returns:
            A list of SearchResult objects.
        """

        filter_expr = None
        if filters:
            expressions = [f'{field} == "{value}"' for field, value in filters.items()]
            filter_expr = " AND ".join(expressions)
        print(f'filter_expr: {filter_expr}')
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_embedding],
            limit=top_k,
            filter=filter_expr,
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

        search_results = []
        print(f'results[0]: {len(results[0])}')
        for hit in results[0]:

            entity = hit["entity"]

            metadata = Metadata(
                domain={
                    "title": entity["title"],
                    "category": entity["category"]
                }
            )

            chunk = Chunk(
                doc_id=entity["doc_id"],
                chunk_id=entity["chunk_id"],
                text=entity["text"],
                page_num=entity["page_num"],
                metadata=metadata
            )

            search_results.append(
                SearchResult(
                    chunk=chunk,
                    score=hit["distance"]
                )
            )

        return search_results
