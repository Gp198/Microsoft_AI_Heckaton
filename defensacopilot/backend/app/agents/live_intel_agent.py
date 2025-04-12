# live_intel_agent.py — Real-time NATO News Agent with RSS + Azure OpenAI

import os
import feedparser
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, RateLimitError, OpenAIError

# === Load environment variables ===
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# === Init Azure OpenAI Client ===
client = AsyncAzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version="2024-02-15-preview",
)

# === Trusted NATO-related feeds ===
RSS_FEEDS = [
    "https://www.nato.int/cps/en/natolive/news_rss.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.reutersagency.com/feed/?best-topics=defence&post_type=best",
    "https://apnews.com/rss"
]

# === Fetch latest NATO/defense-related news ===
def fetch_live_news(limit=5):
    entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if "nato" in entry.title.lower() or "defense" in entry.title.lower():
                published = entry.get("published", "")
                entries.append(f"- {entry.title.strip()} ({published})\n{entry.link}")
                if len(entries) >= limit:
                    break
        if len(entries) >= limit:
            break
    return entries if entries else ["No live NATO-related news found at this time."]

# === System-level prompt with safety ===
system_prompt = (
    "You are DefensaCopilot, an expert defense intelligence AI. Always base answers strictly on factual, verifiable information. "
    "Do not speculate or hallucinate. If unsure, say 'I cannot confirm this information at this time.'"
)

# === Query Azure OpenAI with real-time context ===
async def query_with_live_context(user_question: str):
    # 1. Get current defense headlines
    context_snippets = fetch_live_news(limit=5)
    context_block = "\n\n".join(context_snippets)

    # 2. Build prompt with current context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here is today's defense intelligence context:\n{context_block}\n\nUser question: {user_question}"},
    ]

    # 3. Call Azure OpenAI with error handling
    try:
        response = await client.chat.completions.create(
            model=OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=0.4,
            max_tokens=700,
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        return "⏳ Rate limit hit. Please wait and try again."
    except OpenAIError as e:
        return f"❌ OpenAI Error: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"

# === For test use ===
if __name__ == "__main__":
    async def run():
        question = input("Ask DefensaCopilot: ")
        response = await query_with_live_context(question)
        print("\n🛰️ Response:\n", response)

    asyncio.run(run())
