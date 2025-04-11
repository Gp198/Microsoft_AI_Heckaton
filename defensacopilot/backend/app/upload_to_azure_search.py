import os
import uuid
import pandas as pd
from PyPDF2 import PdfReader
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from pathlib import Path

# === Load environment variables from a specific .env file ===
env_path = Path("C:/Users/Utilizador/Documents/GitHub/Microsoft_AI_Heckaton/defensacopilot/backend/app/.env")
load_dotenv(dotenv_path=env_path)

# === Azure Cognitive Search configuration ===
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"

# === Initialize Azure Search Client ===
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# === File Readers ===
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_csv(path):
    df = pd.read_csv(path)
    return "\n".join(df.astype(str).apply(lambda row: " | ".join(row), axis=1))

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

# === File Directory and Loop ===
DOCUMENTS_FOLDER = "docs"
files = os.listdir(DOCUMENTS_FOLDER)
batch = []
docs_indexed = 0

for file in files:
    path = os.path.join(DOCUMENTS_FOLDER, file)
    ext = os.path.splitext(file)[1].lower()

    if ext == ".txt":
        content = read_txt(path)
    elif ext == ".csv":
        content = read_csv(path)
    elif ext == ".pdf":
        content = read_pdf(path)
    else:
        print(f"❌ Skipped unsupported format: {file}")
        continue

    if content:
        batch.append({
            "id": str(uuid.uuid4()),
            "content": content
        })
        docs_indexed += 1
        print(f"✅ Document indexed: {file}")

# === Upload to Azure Search ===
if batch:
    try:
        result = search_client.upload_documents(documents=batch)
        print(f"\n🚀 Uploaded {len(result)} documents to Azure Search index '{AZURE_SEARCH_INDEX}'.")
    except Exception as e:
        print(f"⚠️ Upload failed: {e}")
else:
    print("⚠️ No documents to upload.")
