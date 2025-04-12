# live_intel_agent.py – Dynamic RAG-based Agent Only

import os
from dotenv import load_dotenv
from agents.semantic_rag import fetch_semantic_context
from openai import AsyncAzureOpenAI

# === Load environment variables ===
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.3))
OPENAI_RETRY_ATTEMPTS = int(os.getenv("OPENAI_RETRY_ATTEMPTS", 3))

if not all([OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_DEPLOYMENT]):
    raise EnvironmentError("❌ Missing OpenAI .env configuration.")

# === Initialize client ===
client = AsyncAzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version="2024-02-15-preview",
)

# === Core Prompt ===
system_prompt = (
    "You are DefensaCopilot, a defense-focused assistant. Respond only with factual, verified, and document-grounded information. "
    "Avoid speculation or hallucination. If unsure or lacking support from documents, respond with: "
    "'I cannot confirm this information at this time.'"
)

# === Function to handle queries with RAG only ===
async def query_rag_only_agent(user_query: str) -> str:
    try:
        document_context = fetch_semantic_context(user_query)
    except Exception:
        document_context = "[RAG context unavailable]"

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Refer to the internal documents below to answer:
\n{document_context}\n\nUser question: {user_query}"
        },
    ]

    for attempt in range(OPENAI_RETRY_ATTEMPTS):
        try:
            response = await client.chat.completions.create(
                model=OPENAI_DEPLOYMENT,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=800,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            if attempt == OPENAI_RETRY_ATTEMPTS - 1:
                return f"❌ Failed after {OPENAI_RETRY_ATTEMPTS} attempts: {e}"

    return "❌ Unable to produce a valid response after retries."

# === Exported entry point ===
__all__ = ["query_rag_only_agent"]
