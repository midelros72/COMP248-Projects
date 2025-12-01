"""Simple script to preload a few health-related dummy documents into FAISS.

Run:
    python kb/load_data.py
"""
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FAISS_PATH = os.path.join(BASE_DIR, "kb", "faiss_store")

def main():
    print("Initializing FAISS with HuggingFace embeddings...")
    # Using all-MiniLM-L6-v2 which is equivalent to Chroma's default
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    docs_data = [
        {
            "id": "doc1",
            "text": "Influenza (flu) is a contagious respiratory illness caused by influenza viruses. "
                    "Common symptoms include fever, cough, sore throat, runny or stuffy nose, muscle or "
                    "body aches, headaches and fatigue.",
        },
        {
            "id": "doc2",
            "text": "Hand hygiene, such as washing hands with soap and water for at least 20 seconds, is one "
                    "of the most effective ways to prevent many infectious diseases.",
        },
        {
            "id": "doc3",
            "text": "Vaccination is a safe and effective way to prevent many serious diseases. Side effects are "
                    "usually mild and temporary, such as soreness at the injection site or low-grade fever.",
        },
    ]

    documents = [Document(page_content=d["text"], metadata={"id": d["id"]}) for d in docs_data]

    # Create and save the FAISS index
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(FAISS_PATH)
    
    print(f"Done populating FAISS index at {FAISS_PATH}")

if __name__ == "__main__":
    main()
