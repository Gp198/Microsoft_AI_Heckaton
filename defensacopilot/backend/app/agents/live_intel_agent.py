# live_intel_agent.py — Conversational Agent with Live Defense Intelligence

import feedparser
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# RSS Feed URL (can be expanded with more sources)
RSS_FEED_URL = "https://www.nato.int/cps/en/natolive/news_rss.xml"

# === Fetch latest NATO news headlines ===
def fetch_recent_news(limit=5):
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        if not feed.entries:
            return "No live headlines found from NATO."

        entries = []
        for entry in feed.entries[:limit]:
            title = entry.get("title", "No title")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            entries.append(f"📰 {title}\n{summary}\n🔗 {link}")

        return "\n\n".join(entries)
    except Exception as e:
        return f"Error fetching news: {e}"

# === Live Intel Conversational Agent ===
async def live_intel_agent(query: str, kernel: Kernel) -> str:
    try:
        if kernel is None:
            return "⚠️ Kernel not initialized."

        # Retrieve latest headlines for context
        headlines = fetch_recent_news()

        # Construct a system message with guardrails and professional tone
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional defense intelligence analyst."
                    " Use ONLY the provided news headlines below to answer the user's question."
                    " If the answer cannot be determined from the headlines, say:"
                    " 'There is no confirmed update regarding this topic at this time.'"
                    " Avoid speculation or assumptions."
                    f"\n\nLatest NATO Headlines:\n{headlines}"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]

        # Execute chat completion
        chat_service = kernel.get_service(AzureChatCompletion)
        result = await chat_service.complete_chat(messages)
        return result.strip()

    except Exception as e:
        return f"❌ Live intelligence agent failed: {e}"
