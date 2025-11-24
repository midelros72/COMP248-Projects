"""Simple script to preload a few health-related dummy documents into Chromadb.

Run:
    python kb/load_data.py
"""
import os
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "kb", "chroma_store")

def main():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection("health_docs")

    if collection.count() > 0:
        print("Collection already has data, skipping insert.")
        return

    docs = [
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

    ef = embedding_functions.DefaultEmbeddingFunction()

    for d in docs:
        emb = ef([d["text"]])
        collection.add(
            ids=[d["id"]],
            documents=[d["text"]],
            embeddings=emb,
        )
        print(f"Inserted {d['id']} into health_docs collection.")

    print("Done populating Chromadb health_docs collection.")

if __name__ == "__main__":
    main()
