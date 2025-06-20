# app/rag.py

from app.translator import translate_to_english
from app.utils import clean_text, generate_uuid, log_info, log_error

from langchain_chroma import Chroma  # ✅ Updated Chroma import
from langchain_core.documents import Document  # ✅ Updated Document import
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ Updated Embeddings

from typing import List, Dict
import os

# Chroma persistent storage path
CHROMA_PATH = "chroma_index"

# Embedding model using HuggingFace sentence transformers
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Global vector store instance
vector_store: Chroma = None

def init_chroma():
    """Initialize or load Chroma vector store from disk."""
    global vector_store

    try:
        vector_store = Chroma(
            collection_name="real_estate_docs",
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_model
        )

        if os.path.exists(CHROMA_PATH):
            log_info("Chroma index loaded from disk.")
        else:
            log_info("Initialized new Chroma index.")

    except Exception as e:
        log_error(f"Failed to initialize Chroma: {e}")

# Initialize at module load
init_chroma()

def save_chroma_index():
    """Persist Chroma index to disk."""
    try:
        vector_store.persist()
        log_info("Chroma index persisted to disk.")
    except Exception as e:
        log_error(f"Failed to persist Chroma index: {e}")

def add_document(text: str) -> str:
    """Add a cleaned and translated real estate document to Chroma."""
    global vector_store

    try:
        english_text = translate_to_english(text)
        cleaned = clean_text(english_text)
        doc_id = generate_uuid()

        doc = Document(
            page_content=cleaned,
            metadata={"id": doc_id}
        )

        vector_store.add_documents([doc])
        save_chroma_index()

        log_info(f"Document added with ID: {doc_id}")
        return doc_id

    except Exception as e:
        log_error(f"Failed to add document: {e}")
        return None

def search(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    """Search Chroma index and return top-k matching documents."""
    try:
        english_query = translate_to_english(query)
        cleaned_query = clean_text(english_query)

        results = vector_store.similarity_search(cleaned_query, k=top_k)

        return [
            {
                "text": doc.page_content,
                "id": doc.metadata.get("id", "N/A")
            }
            for doc in results
        ]

    except Exception as e:
        log_error(f"Search failed: {e}")
        return []
