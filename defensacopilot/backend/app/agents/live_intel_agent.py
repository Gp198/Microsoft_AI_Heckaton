# live_intel_agent.py

import os
import feedparser
import aiohttp
from openai import AsyncAzureOpenAI

# === Load environment variables ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# === Real-time Defense Agent Class ===
class LiveIntelAgent:
    def __init__(self):
        # Initialize Azure OpenAI client
        self.client = AsyncAzureOpenAI(
            api_key=OPENAI_API_KEY,
            api_version="2023-07-01-preview",
            azure_endpoint=OPENAI_ENDPOINT
        )
        self.deployment = OPENAI_DEPLOYMENT

    async def fetch_latest_news(self, topic="defense"):
        """Fetch latest news articles from RSS feeds about the given topic."""
        url = f"https://news.google.com/rss/search?q={topic}+when:7d&hl=en&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        entries = feed.entries[:5]

        if not entries:
            return "No recent articles were found on this topic."

        articles = "\n".join([f"- {entry.title}" for entry in entries])
        return f"Latest news headlines:\n{articles}"

    async def answer(self, user_input):
        """Combine real-time info with LLM reasoning"""
        # Guardrails: Reject overly vague prompts
        if len(user_input.strip()) < 5:
            return "⚠️ Please provide a more detailed question."

        context = await self.fetch_latest_news(user_input)

        prompt = f"""
You are DefensaCopilot, an AI specialized in live defense intelligence.

Your role:
- Answer concisely using only facts.
- If you’re unsure, say “I don’t have that information.”
- Use the news context below to support your answer.

News Context:
{context}

User Question:
{user_input}

Answer:
"""

        # Call Azure OpenAI Chat Completion
        response = await self.client.chat.completions.create(
            deployment_id=self.deployment,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in defense and geopolitics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        reply = response.choices[0].message.content.strip()

        # Simple validation
        if any(x in reply.lower() for x in ["i don't know", "unsure", "no data"]):
            return "❌ Sorry, I couldn't find a reliable answer based on current information."

        return reply
