import feedparser
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# NATO RSS feed (pode adicionar mais)
RSS_FEED_URL = "https://www.nato.int/cps/en/natolive/news.rss"

# === Coleta notícias recentes ===
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

# === Agente de conversa com contexto em tempo real ===
async def live_intel_agent(query: str, kernel: Kernel) -> str:
    try:
        if kernel is None:
            return "⚠️ Kernel not initialized."

        # Coleta headlines atualizadas
        headlines = fetch_recent_news()

        # Define mensagens estilo chat
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a defense analyst AI who provides clear, concise, and helpful answers "
                    "based only on the latest NATO updates. Do not hallucinate. If no information is found, say so.\n\n"
                    f"Live Headlines:\n{headlines}"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]

        # Executa chat com Azure OpenAI
        chat_service = kernel.get_service("azure-openai")
        result = await chat_service.complete_chat(messages)
        return result.strip()

    except Exception as e:
        return f"❌ Live chat agent failed: {e}"
