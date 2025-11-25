import os
from typing import List

import chromadb

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "kb", "chroma_store")

def _get_collection():
    """DISABLED: ChromaDB corrupted - returning None to bypass RAG."""
    print("⚠️  RAG disabled (ChromaDB corrupted)")
    return None

def rag_search_fallback(query: str, k: int = 4) -> List[str]:
    """RAG disabled to avoid ChromaDB corruption crash."""
    return []
