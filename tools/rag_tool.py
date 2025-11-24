import os
from typing import List

import chromadb

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "kb", "chroma_store")

def _get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection("health_docs")

def rag_search_fallback(query: str, k: int = 4) -> List[str]:
    """Basic direct Python RAG search that does not rely on CrewAI tools system."""
    collection = _get_collection()
    if collection.count() == 0:
        return []
    results = collection.query(query_texts=[query], n_results=k)
    docs_nested = results.get("documents", [[]])
    return docs_nested[0] if docs_nested else []
