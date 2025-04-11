# rag_agent.py
# ------------------------------------------------------------------------------------
# Retrieval-Augmented Generation (RAG) Agent
# This module performs semantic search using Azure Cognitive Search,
# and returns a structured response with document-based intelligence.
# ------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from pathlib import Path

# === Load environment variables from .env ===
load_dotenv(dotenv_path=Path("C:/Users/Utilizador/Documents/GitHub/Microsoft_AI_Heckaton/defensacopilot/backend/app/.env"))

AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")

AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"

# === Initialize Azure Cognitive Search Client ===
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# === RAG Agent logic ===
async def rag_agent(query: str, top_k: int = 3) -> str:
    """
    Performs a semantic search over Azure Cognitive Search index,
    retrieving the most relevant document snippets for the user query.

    Parameters:
        query (str): The user's input question.
        top_k (int): Number of top documents to retrieve (default: 3)

    Returns:
        str: Formatted response with sources and content excerpts.
    """
    try:
        results = search_client.search(search_text=query, top=top_k)
        hits = [doc["content"] for doc in results if "content" in doc]

        if not hits:
            return "⚠️ No relevant documents were found in the knowledge base."

        response = f"""
📚 Document Intelligence Report

🧭 Question:
\"{query}\"

📄 Top {len(hits)} Retrieved Snippets:
"""
        for i, content in enumerate(hits, 1):
            snippet = content[:500].replace("\n", " ")  # Trim & format
            response += f"\n🔹 Snippet {i}:\n{snippet}\n"

        return response.strip()

    except Exception as e:
        return f"❌ Error while performing RAG search: {e}"
