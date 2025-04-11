# rag_agent.py
# ------------------------------------------------------------------------------------
# Retrieval-Augmented Generation (RAG) Agent
# This module performs semantic search using Azure Cognitive Search,
# and returns a structured response with document-based intelligence.
# ------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# === Load environment variables ===
load_dotenv()
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/"

# === Initialize Azure Search Client ===
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AZURE_SEARCH_KEY
)

# === Prompt template ===
RAG_PROMPT_TEMPLATE = """
You are an AI intelligence analyst.

Your task is to answer the user's question using ONLY the information contained in the documents provided as context.

Do not guess or invent data. If the answer is not found in the context, respond clearly:
"No reliable information is available to answer this question."

---
Context:
{context}

---
Question:
{query}

---
Provide a concise, well-structured answer using neutral and informative language.
"""

# === Initialize Semantic Kernel ===
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("OPENAI_DEPLOYMENT"),
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# === RAG agent ===
async def rag_agent(query: str) -> str:
    try:
        # Search relevant documents from Azure Search
        results = search_client.search(search_text=query, top=5)
        context_docs = [doc["content"] for doc in results]

        if not context_docs:
            return "⚠️ No documents found that match the question."

        # Build the prompt using top documents
        context = "\n\n".join(context_docs[:3])
        prompt = RAG_PROMPT_TEMPLATE.format(query=query, context=context)

        # Get completion from Azure OpenAI
        completion = await kernel.services.get(AzureChatCompletion).complete(prompt)
        response = completion.get_final_result()

        # Guardrail validation
        if "no reliable information" in response.lower():
            return "📭 No verifiable information available to answer this question."

        return response
    except Exception as e:
        return f"❌ Error retrieving intelligence: {e}"
