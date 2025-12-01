import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

FAISS_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "faiss_store")

def rag_search_fallback(query: str, k: int = 4) -> List[str]:
    """Search the FAISS index for relevant documents."""
    if not os.path.exists(FAISS_PATH):
        print(f"⚠️  FAISS index not found at {FAISS_PATH}")
        return []

    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # allow_dangerous_deserialization is set to True because we created the index ourselves
        vectorstore = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        docs = vectorstore.similarity_search(query, k=k)
        return [d.page_content for d in docs]
    except Exception as e:
        print(f"Error searching FAISS index: {e}")
        return []
