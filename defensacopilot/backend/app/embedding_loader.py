# embedding_loader.py — Load and embed documents (txt, pdf, csv) to FAISS index

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# === Config ===
DATA_DIR = "../data"
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
DOCS_PATH = os.path.join(DATA_DIR, "docs.pkl")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".csv"]

# === Load documents ===
def load_documents(directory: str):
    documents = []
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        ext = os.path.splitext(file)[-1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue
        try:
            if ext == ".txt":
                loader = TextLoader(path)
            elif ext == ".pdf":
                loader = PyPDFLoader(path)
            elif ext == ".csv":
                loader = CSVLoader(path)
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"⚠️ Failed to load {file}: {e}")
    return documents

# === Embed and index ===
def build_faiss_index(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(docs)

    texts = [chunk.page_content for chunk in chunks]
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(texts, f)
    faiss.write_index(index, INDEX_PATH)
    print(f"✅ Indexed {len(texts)} text chunks.")

# === Execute ===
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    docs = load_documents("../source_docs")
    build_faiss_index(docs)
