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
                    "body aches, headaches and fatigue. Complications can include pneumonia, ear infections, "
                    "and sinus infections.",
        },
        {
            "id": "doc2",
            "text": "Hand hygiene, such as washing hands with soap and water for at least 20 seconds, is one "
                    "of the most effective ways to prevent many infectious diseases. Alcohol-based hand sanitizers "
                    "with at least 60% alcohol can be used if soap and water are not available.",
        },
        {
            "id": "doc3",
            "text": "Vaccination is a safe and effective way to prevent many serious diseases. Side effects are "
                    "usually mild and temporary, such as soreness at the injection site or low-grade fever. "
                    "Vaccines work by training the immune system to recognize and fight pathogens.",
        },
        {
            "id": "doc4",
            "text": "Type 2 Diabetes is a chronic condition that affects the way the body processes blood sugar (glucose). "
                    "Symptoms include increased thirst, frequent urination, hunger, fatigue, and blurred vision. "
                    "Risk factors include obesity, inactivity, and family history.",
        },
        {
            "id": "doc5",
            "text": "Hypertension (High Blood Pressure) is a common condition in which the long-term force of the blood "
                    "against your artery walls is high enough that it may eventually cause health problems, such as heart disease. "
                    "It is often called the 'silent killer' because it may have no warning signs or symptoms.",
        },
        {
            "id": "doc6",
            "text": "Regular physical activity is one of the most important things you can do for your health. "
                    "It can help control weight, reduce risk of cardiovascular disease, type 2 diabetes, and some cancers, "
                    "strengthen bones and muscles, and improve mental health and mood.",
        },
        {
            "id": "doc7",
            "text": "A balanced diet involves consuming a variety of foods in the right proportions. "
                    "Key components include fruits, vegetables, whole grains, lean proteins, and healthy fats. "
                    "Limiting processed foods, added sugars, and excessive sodium is recommended for optimal health.",
        },
        {
            "id": "doc8",
            "text": "Mental health includes our emotional, psychological, and social well-being. It affects how we think, "
                    "feel, and act. It also helps determine how we handle stress, relate to others, and make choices. "
                    "Common conditions include anxiety disorders, depression, and bipolar disorder.",
        },
        {
            "id": "doc9",
            "text": "Sleep is essential for good health. Adults generally need 7 or more hours of good-quality sleep "
                    "on a regular schedule each night. Poor sleep is linked to chronic conditions like diabetes, "
                    "heart disease, obesity, and depression.",
        },
        {
            "id": "doc10",
            "text": "Antibiotic resistance happens when germs like bacteria and fungi develop the ability to defeat "
                    "the drugs designed to kill them. That means the germs are not killed and continue to grow. "
                    "Overuse and misuse of antibiotics are key drivers of this global health threat.",
        }
    ]

    documents = [Document(page_content=d["text"], metadata={"id": d["id"]}) for d in docs_data]

    # Create and save the FAISS index
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(FAISS_PATH)
    
    print(f"Done populating FAISS index at {FAISS_PATH}")

if __name__ == "__main__":
    main()
