# disinfo_agent.py
# ---------------------------------------------------------------
# Disinformation Agent - Simulates fact-checking of questionable claims
# This module is part of the DefensaCopilot agent system.
# ---------------------------------------------------------------

# The agent receives a query and returns a structured response
# simulating misinformation analysis based on a predefined template.

from azure.search.documents import SearchClient
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel import Kernel
from dotenv import load_dotenv
import os

# Load environment and Azure Search config
load_dotenv()
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/"

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AZURE_SEARCH_KEY
)

# Professional analyst prompt with strong guardrails
DISINFO_PROMPT_TEMPLATE = """
You are an AI misinformation analyst working for a defense intelligence agency.

Your job is to verify whether the following claim might be false, misleading, or lacking credible evidence. Use only the context provided.

Respond ONLY based on the provided context. If no reliable information exists, respond: "No supporting evidence was found."

---
Context:
{context}

---
Claim to analyze:
{query}

---
Answer clearly and professionally in one paragraph.
"""

# Setup Semantic Kernel with Azure OpenAI
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("OPENAI_DEPLOYMENT"),
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

async def disinfo_agent(query: str) -> str:
    # Step 1: Search documents related to the query
    results = search_client.search(query, top=5)
    context_docs = [doc["content"] for doc in results]

    if not context_docs:
        return "⚠️ No relevant documents found to verify this claim."

    # Step 2: Prepare context and fill prompt
    context = "\n\n".join(context_docs[:3])  # limit to top 3 for token safety
    prompt = DISINFO_PROMPT_TEMPLATE.format(query=query, context=context)

    # Step 3: Run through LLM
    try:
        completion = await kernel.services.get(AzureChatCompletion).complete(prompt)
        response = completion.get_final_result()

        # Step 4: Validate result
        if "no supporting evidence" in response.lower():
            return "🛡️ The claim could not be validated — no credible sources found."
        return response
    except Exception as e:
        return f"❌ Error validating claim: {e}"

