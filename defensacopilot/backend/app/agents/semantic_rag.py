# semantic_rag.py — Retrieve semantically relevant document chunks using FAISS or Chroma

import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model and index on module load
model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "../data/index.faiss"
DOCS_PATH = "../data/docs.pkl"

# Load FAISS index
try:
    index = faiss.read_index(INDEX_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load FAISS index: {e}")

# Load original documents
try:
    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load document store: {e}")

def fetch_semantic_context(query: str, top_k: int = 3) -> str:
    """
    Search the FAISS index for semantically similar documents.
    Returns a formatted string with top document chunks.
    """
    query_vector = model.encode([query])
    D, I = index.search(query_vector, top_k)

    results = []
    for idx in I[0]:
        if idx < len(documents):
            chunk = documents[idx]
            results.append(f"• {chunk.strip()}")

    return "\n".join(results) if results else "[No relevant context found.]"

# Optional CLI test
if __name__ == "__main__":
    q = input("Query: ")
    print("\nContext:\n")
    print(fetch_semantic_context(q))

