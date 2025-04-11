import feedparser
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# RSS feeds de fontes confiáveis de defesa (podes ajustar conforme necessário)
RSS_FEEDS = [
    "https://www.nato.int/cps/en/natolive/news_rss.htm",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
]

# === Função para agregar manchetes recentes ===
def fetch_latest_headlines():
    headlines = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:3]:  # Limita a 3 notícias por fonte
            headlines.append(f"- {entry.title}")
    return "\n".join(headlines)

# === Agente de inteligência em tempo real ===
async def live_intel_agent(query: str, kernel: Kernel) -> str:
    try:
        # Obter headlines atualizadas
        headlines = fetch_latest_headlines()

        # Construir prompt com guardrails
        system_prompt = (
            "You are an AI military intelligence analyst. "
            "Based ONLY on the real-time headlines provided, respond concisely to the user's question. "
            "If the answer is not found in the data, say: 'There is no confirmed update on that at this time.'\n\n"
            "HEADLINES:\n"
            f"{headlines}\n\n"
            "USER QUESTION:\n"
            f"{query}"
        )

        # Obter o serviço de chat configurado
        chat_service = kernel.get_service(AzureChatCompletion)

        # Obter resposta
        response = await chat_service.complete_chat(messages=[
            {"role": "system", "content": system_prompt},
        ])

        return response.strip()

    except Exception as e:
        return f"❌ Live intelligence agent failed: {e}"
