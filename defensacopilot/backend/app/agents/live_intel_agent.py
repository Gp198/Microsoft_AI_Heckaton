import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import feedparser

# === Load environment variables ===
load_dotenv()
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/"

# === Azure Search client ===
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AZURE_SEARCH_KEY
)

# === Live news source (NATO RSS) ===
def fetch_nato_news(limit=3):
    url = "https://www.nato.int/cps/en/natolive/news.rss"
    feed = feedparser.parse(url)
    headlines = []

    for entry in feed.entries[:limit]:
        headlines.append(f"📰 {entry.title}\n🔗 {entry.link}")

    return "\n".join(headlines) if headlines else "No NATO updates at the moment."

# === Prompt with live + RAG context ===
LIVE_INTEL_PROMPT = """
You are an AI defense analyst providing a real-time situational report.

Your response must ONLY use the context below: recent NATO headlines and retrieved defense documents.
If no matching information is found, say:
"No relevant live or archived data is available to answer this query."

---
Live News:
{live_context}

---
Archived Context:
{archived_context}

---
Question:
{query}

---
Provide a concise and factual intelligence summary with relevant sources, in professional tone.
"""

# === Kernel with Azure OpenAI ===
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("OPENAI_DEPLOYMENT"),
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# === Agent execution ===
async def live_intel_agent(query: str) -> str:
    try:
        # Step 1: Get live headlines
        live_context = fetch_nato_news()

        # Step 2: Retrieve archived documents from Azure Search
        results = search_client.search(query, top=3)
        docs = [doc["content"] for doc in results]
        archived_context = "\n\n".join(docs) if docs else "None"

        # Step 3: Create prompt
        prompt = LIVE_INTEL_PROMPT.format(
            live_context=live_context,
            archived_context=archived_context,
            query=query
        )

        # Step 4: Run completion
        completion = await kernel.services.get(AzureChatCompletion).complete(prompt)
        response = completion.get_final_result()

        # Step 5: Guardrail
        if "no relevant" in response.lower():
            return "📭 No actionable intelligence found based on live data or archived documents."
        
        return response
    except Exception as e:
        return f"❌ Live intelligence agent failed: {e}"
