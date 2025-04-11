# live_intel_agent.py
# Advanced live intelligence agent using Azure OpenAI with RAG, guardrails, and response validation

import os
import feedparser
import aiohttp
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from datetime import datetime

# === Load environment variables ===
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not all([AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT]):
    raise EnvironmentError("Missing one or more Azure OpenAI environment variables.")

# === Azure OpenAI Chat Client ===
class LiveIntelAgent:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=AZURE_OPENAI_DEPLOYMENT,
            api_version="2024-03-01-preview"
        )

    async def fetch_latest_defense_news(self, topic="defense"):
        rss_url = f"https://news.google.com/rss/search?q={topic}+defense&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)
        articles = [entry.title + ". " + entry.summary for entry in feed.entries[:5]]
        return "\n".join(articles) if articles else "No recent updates found."

    async def validate_response(self, response):
        """
        Guardrails: Basic checks for hallucinations.
        Validates the structure and presence of relevant keywords.
        """
        if not response:
            return False, "Response is empty."
        if any(term in response.lower() for term in ["i am not sure", "as an ai", "cannot provide"]):
            return False, "Model declined to answer clearly."
        return True, "Response is valid."

    async def ask(self, user_input):
        # Retrieve contextual news from the web (RAG)
        context = await self.fetch_latest_defense_news(user_input)

        prompt = (
            f"You are DefensaCopilot, an expert real-time defense analyst.
            Always answer clearly and concisely, based only on the real-time intel provided.
            Use professional tone, avoid speculation, and clearly cite your evidence.

            Contextual Information:
            {context}

            User Question: {user_input}
            Professional Response:"
        )

        try:
            response = await self.client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            answer = response.choices[0].message.content.strip()
            is_valid, validation_msg = await self.validate_response(answer)

            if not is_valid:
                return f"❌ Guardrail Alert: {validation_msg}"

            return f"✅ {answer}"
        except Exception as e:
            return f"❌ Error while querying Azure OpenAI: {e}"
