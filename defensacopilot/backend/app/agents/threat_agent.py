# threat_agent.py
# ---------------------------------------------------------------------
# Threat Analysis Agent - Simulates the detection of military movements,
# geopolitical escalations, or strategic alerts.
# ---------------------------------------------------------------------

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

# Initialize Azure Search
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AZURE_SEARCH_KEY
)

# Prompt template for threat intelligence
THREAT_PROMPT_TEMPLATE = """
You are an AI military threat intelligence analyst.

Your task is to assess the level of geopolitical or military threat related to the user's query, based strictly on the context provided.

Do not speculate or generate data not found in the context.
If no relevant intelligence is found, reply:
"No threat indicators were detected in the available intelligence."

---
Context:
{context}

---
Threat Inquiry:
{query}

---
Respond with a short tactical summary, specifying the nature of the threat, location, and severity level.
"""

# Initialize Semantic Kernel
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("OPENAI_DEPLOYMENT"),
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Threat agent function
async def threat_agent(query: str) -> str:
    try:
        results = search_client.search(query, top=5)
        context_docs = [doc["content"] for doc in results]

        if not context_docs:
            return "⚠️ No intelligence indicators were found."

        context = "\n\n".join(context_docs[:3])
        prompt = THREAT_PROMPT_TEMPLATE.format(query=query, context=context)

        completion = await kernel.services.get(AzureChatCompletion).complete(prompt)
        response = completion.get_final_result()

        # Basic guardrail check
        if "no threat indicators" in response.lower():
            return "🛡️ No credible threat detected in the current intelligence."

        return response
    except Exception as e:
        return f"❌ Threat agent error: {e}"

