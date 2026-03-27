from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import chromadb
from chromadb.api.models.Collection import Collection


class ChromaStore:
    def __init__(self, persist_dir: Path, collection_name: str = "minibot_docs") -> None:
        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection: Collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def index_chunks(self, filename: str, chunks: list[str]) -> int:
        if not chunks:
            return 0

        ids = [f"{filename}-{idx}-{uuid4()}" for idx in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk_index": idx} for idx in range(len(chunks))]
        self.collection.add(ids=ids, documents=chunks, metadatas=metadatas)
        return len(chunks)

    def search(self, query: str, top_k: int = 4) -> list[str]:
        if self.collection.count() == 0:
            return []
        result = self.collection.query(query_texts=[query], n_results=top_k)
        docs = result.get("documents", [[]])
        return docs[0] if docs else []
