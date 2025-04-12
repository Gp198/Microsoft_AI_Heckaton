# semantic_rag.py — Retrieve semantically relevant document chunks using FAISS or Chroma

import os
import pickle
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

DOCUMENTS_FOLDER = "docs"
FAISS_INDEX_PATH = "faiss_index/index.faiss"
DOCS_PATH = "faiss_index/docs.pkl"

os.makedirs("faiss_index", exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")
documents = []
embeddings = []

# --- Funções de leitura ---

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_csv(path):
    df = pd.read_csv(path)
    return "\n".join(df.astype(str).apply(lambda row: " | ".join(row), axis=1))

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

# --- Carregamento dos ficheiros ---

for file in os.listdir(DOCUMENTS_FOLDER):
    file_path = os.path.join(DOCUMENTS_FOLDER, file)
    content = ""
    if file.endswith(".txt"):
        content = read_txt(file_path)
    elif file.endswith(".csv"):
        content = read_csv(file_path)
    elif file.endswith(".pdf"):
        content = read_pdf(file_path)
    else:
        continue

    if content:
        documents.append(content)
        embeddings.append(model.encode(content))

# --- Criar índice FAISS ---
embedding_dim = len(embeddings[0])
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(embeddings).astype("float32"))

# Guardar index e docs
faiss.write_index(index, FAISS_INDEX_PATH)
with open(DOCS_PATH, "wb") as f:
    pickle.dump(documents, f)

print(f"✅ Index criado com {len(documents)} documentos!")

# Optional CLI test
if __name__ == "__main__":
    q = input("Query: ")
    print("\nContext:\n")
    print(fetch_semantic_context(q))
