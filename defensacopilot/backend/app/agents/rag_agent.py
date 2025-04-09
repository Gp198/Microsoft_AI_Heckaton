# rag_agent.py - RAG com FAISS local

import os
import faiss
import pickle
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

# Carrega o modelo de embedding local (compatível com FAISS)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Caminho para os documentos indexados localmente
FAISS_INDEX_PATH = "faiss_index/index.faiss"
DOCS_PATH = "faiss_index/docs.pkl"

# Carrega FAISS index e os documentos
index = faiss.read_index(FAISS_INDEX_PATH)
with open(DOCS_PATH, "rb") as f:
    documents = pickle.load(f)

# Função de busca RAG
async def rag_agent(query: str) -> str:
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), k=3)

    results: List[str] = []
    for idx in I[0]:
        results.append(f"• {documents[idx][:300]}...")

    return "\n📖 RAG Intel Report:\n" + "\n".join(results)
