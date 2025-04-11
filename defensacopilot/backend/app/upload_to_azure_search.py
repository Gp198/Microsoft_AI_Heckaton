import os
import uuid
import pandas as pd
from PyPDF2 import PdfReader
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

# Configurações do Azure Search
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"

# Cliente do Azure Search
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# Funções de leitura
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_csv(path):
    df = pd.read_csv(path)
    return "\n".join(df.astype(str).apply(lambda row: " | ".join(row), axis=1))

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

# Caminho para os ficheiros
DOCS_FOLDER = "docs"
files = os.listdir(DOCS_FOLDER)

# Documentos a indexar
batch = []
for file in files:
    path = os.path.join(DOCS_FOLDER, file)
    ext = os.path.splitext(file)[1].lower()
    if ext == ".txt":
        content = read_txt(path)
    elif ext == ".csv":
        content = read_csv(path)
    elif ext == ".pdf":
        content = read_pdf(path)
    else:
        print(f"❌ Ignorado: {file} (formato não suportado)")
        continue

    if content:
        batch.append({
            "id": str(uuid.uuid4()),
            "content": content
        })
        print(f"✅ Documento '{file}' preparado.")

# Upload
if batch:
    result = search_client.upload_documents(documents=batch)
    if all(r.succeeded for r in result):
        print(f"\n🚀 {len(result)} documentos indexados com sucesso!")
    else:
        print("⚠️ Alguns documentos falharam:")
        for r in result:
            if not r.succeeded:
                print(f" - {r.key}: {r.error_message}")
else:
    print("⚠️ Nenhum documento para indexar.")
