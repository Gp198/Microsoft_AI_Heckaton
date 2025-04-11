import os
import feedparser
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# === Configure Azure OpenAI via environment variables ===
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
if not all([OPENAI_DEPLOYMENT, OPENAI_ENDPOINT, OPENAI_API_KEY]):
    raise EnvironmentError("❌ Missing Azure OpenAI environment configuration.")

# === Initialize Semantic Kernel and AzureChatCompletion service ===
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=OPENAI_DEPLOYMENT,
        endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    )
)

# === News feed sources relevant to defense and security ===
FEED_URLS = [
    "https://www.nato.int/cps/en/natolive/news_rss.xml",           # NATO official news
    "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx",   # U.S. Department of Defense
    "https://feeds.bbci.co.uk/news/world/rss.xml",                 # BBC World News
    "https://www.aljazeera.com/xml/rss/all.xml",                   # Al Jazeera
]

# === Extract the latest headlines from RSS feeds ===
def fetch_recent_headlines(max_items=5):
    all_headlines = []

    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_items]:
            title = entry.title
            summary = entry.summary if hasattr(entry, "summary") else ""
            source = feed.feed.title if hasattr(feed, "title") else "Unknown source"
            all_headlines.append(f"- [{source}] {title}: {summary}")

    return "\n".join(all_headlines)


# === Live Intel Agent Function ===
async def live_intel_agent(user_query: str) -> str:
    try:
        # Step 1: Fetch live news
        context_news = fetch_recent_headlines()

        # Step 2: Create an advanced prompt
        prompt = f"""
You are a defense analyst assistant with access to recent military and geopolitical news.
Based on the question below and the real-time updates provided, generate a concise and accurate summary.

Be factual. If information is unclear or unavailable, say: "There is no current confirmed information on that topic."

### User Question:
{user_query}

### Real-time Defense Headlines:
{context_news}

### Response:
"""

        # Step 3: Use Semantic Kernel to generate the response
        result = await kernel.complete(prompt)
        return result.strip()

    except Exception as e:
        return f"❌ Live intelligence agent failed: {e}"
