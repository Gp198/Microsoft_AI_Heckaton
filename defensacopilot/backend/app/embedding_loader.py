# embedding_loader.py - carrega documentos e cria embeddings no Azure AI Search

import os
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField, VectorSearch, HnswAlgorithmConfiguration, VectorSearchAlgorithmKind, VectorSearchProfile
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential as OpenAICredential
import openai

# CONFIG
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = "defensacopilot-index"
AZURE_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# Mock documentos a indexar (simulados para demo)
docs = [
    {
        "id": "nato-2024",
        "title": "NATO Watch Report 2024",
        "content": "NATO reports increased troop presence in the Baltic region as part of readiness exercises."
    },
    {
        "id": "eda-budget",
        "title": "EDA Defense Budget Overview",
        "content": "EU member states increased defense spending by 12%, with a focus on cybersecurity and mobility."
    },
    {
        "id": "csis-check",
        "title": "Disinformation Alert",
        "content": "No credible evidence supports the claim that Country X has initiated conflict with Country Y."
    }
]

def create_index():
    index_client = SearchIndexClient(
        endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )

    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="title", type="Edm.String", sortable=True),
        SearchableField(name="content", type="Edm.String")
    ]

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX,
        fields=fields
    )

    if AZURE_SEARCH_INDEX not in [i.name for i in index_client.list_indexes()]:
        index_client.create_index(index)
        print("✅ Índice criado com sucesso!")
    else:
        print("ℹ️ Índice já existe.")

def upload_documents():
    search_client = SearchClient(
        endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        index_name=AZURE_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )
    search_client.upload_documents(docs)
    print("📄 Documentos carregados para Azure Search.")

if __name__ == "__main__":
    create_index()
    upload_documents()

