# pipeline/batch_ingestion_pipeline.py

import os


class BatchIngestionPipeline:

    def __init__(
        self,
        loader,
        embedding_model,
        vector_store
    ):
        self.loader = loader
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def run(
        self,
        data_dir: str
    ):
        """
        批量导入目录下所有 JSONL 文件
        """

        total_files = 0
        total_chunks = 0

        for file_name in os.listdir(data_dir):

            if not file_name.endswith(".jsonl"):
                continue

            file_path = os.path.join(
                data_dir,
                file_name
            )

            print(
                f"\nProcessing: {file_name}"
            )

            chunks = self.loader.load(
                file_path
            )

            texts = [
                chunk.text
                for chunk in chunks
            ]

            embeddings = (
                self.embedding_model.encode(
                    texts
                )
            )

            self.vector_store.insert(
                chunks,
                embeddings
            )

            total_files += 1
            total_chunks += len(chunks)

            print(
                f"Loaded {len(chunks)} chunks."
            )

        print("\nBatch Ingestion Completed")

        print(
            f"Total Files : {total_files}"
        )

        print(
            f"Total Chunks: {total_chunks}"
        )
        return {
            "files": total_files,
            "chunks": total_chunks
        }