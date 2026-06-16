import json
from schema.chunk import Chunk
from schema.metadata import Metadata


class JSONLLoader:

    def load(self, file_path: str):
        chunks = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)

                metadata_dict = data.get("metadata", {})

                metadata = Metadata(
                    common=metadata_dict.get("common", {}),
                    domain=metadata_dict.get("domain", {})
                )

                chunk = Chunk(
                    chunk_id=data["chunk_id"],
                    doc_id=data["doc_id"],
                    text=data["text"],
                    page_num=data["page_num"],
                    metadata=metadata
                )

                chunks.append(chunk)

        return chunks