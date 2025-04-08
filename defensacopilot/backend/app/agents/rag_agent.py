# rag_agent.py - Agente que usa Azure Cognitive Search para grounding

import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "defensacopilot-index")

async def rag_agent(query: str) -> str:
    """
    Consulta o índice do Azure Search e retorna um sumário com os documentos mais relevantes.
    """
    search_client = SearchClient(
        endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        index_name=AZURE_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )

    results = search_client.search(query, top=3)
    hits = [f"• {doc['title']}: {doc['content']}" for doc in results]

    if not hits:
        return "No relevant documents found in the knowledge base."

    return (
        f"\U0001F4D6 Intel Report from Search:\n" +
        "\n\n".join(hits)
    )
