# policy_agent.py
# -----------------------------------------------------------------
# Defense Policy Agent - Simulates a policy-based response engine
# This module provides contextual answers based on defense budget,
# treaties, or policy-related topics.
# -----------------------------------------------------------------

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables
load_dotenv()
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/"

# Setup Azure Search Client
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AZURE_SEARCH_KEY
)

# Prompt template for defense policy answers
POLICY_PROMPT_TEMPLATE = """
You are a senior AI defense policy advisor for NATO.

Your job is to provide concise, evidence-based answers on defense budgets, national policies, alliances, and military investments.

Only use the provided context below. Do NOT assume or fabricate data. If the information is not found, say:
"No verified policy information is available at this time."

---
Context:
{context}

---
Question:
{query}

---
Respond with a brief, factual and authoritative answer, using formal tone.
"""

# Setup Semantic Kernel
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("OPENAI_DEPLOYMENT"),
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Main function for policy agent
async def policy_agent(query: str) -> str:
    try:
        results = search_client.search(query, top=5)
        context_docs = [doc["content"] for doc in results]

        if not context_docs:
            return "📉 No relevant policy documents found."

        context = "\n\n".join(context_docs[:3])  # limit to top 3 to reduce tokens
        prompt = POLICY_PROMPT_TEMPLATE.format(query=query, context=context)

        completion = await kernel.services.get(AzureChatCompletion).complete(prompt)
        response = completion.get_final_result()

        # Guardrail: handle fallback message
        if "no verified policy" in response.lower():
            return "⚠️ The answer could not be confirmed with the available documents."

        return response
    except Exception as e:
        return f"❌ Policy advisor error: {e}"

