# DefensaCopilot - Main Orchestrator

import feedparser
import requests
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os
from datetime import datetime

# === Load environment variables ===
AZURE_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# === Prompt Engineering (Advanced) ===
INTEL_PROMPT = """
You are a highly specialized military intelligence analyst.
Your task is to provide reliable, fact-based, and concise answers about global defense activity.

You must:
- Use the retrieved context below as your source of truth.
- If uncertain, clearly say you are not confident.
- Never make up facts or speculate.
- Suggest verification sources if applicable.

### Context:
{{$context}}

### User question:
{{$input}}

Provide a response in fluent, formal English and avoid hallucinations.
"""

# === RAG: Fetch live defense updates ===
def get_live_context():
    feed_urls = [
        "https://www.nato.int/cps/en/natohq/news.xml",  # NATO RSS
        "https://www.defense.gov/Newsroom/News/Transcripts/rss.xml"
    ]
    
    context_snippets = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:  # Limit to latest 3 from each feed
            snippet = f"{entry.title}. {entry.summary}"
            context_snippets.append(snippet)

    return "\n\n".join(context_snippets)

# === Semantic Kernel Setup ===
def get_kernel():
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=AZURE_DEPLOYMENT,
            endpoint=AZURE_ENDPOINT,
            api_key=AZURE_API_KEY
        )
    )
    return kernel

# === Validate response heuristically ===
def validate_response(response: str) -> bool:
    red_flags = [
        "I don't know", "as an AI", "I cannot access", "might be", "possibly"
    ]
    return not any(flag in response.lower() for flag in red_flags)

# === Main inference logic ===
async def answer_question(query: str) -> str:
    context = get_live_context()
    kernel = get_kernel()

    func = kernel.create_semantic_function(
        function_name="LiveIntelAnalysis",
        plugin_name="IntelChat",
        prompt=INTEL_PROMPT,
        description="Answer defense-related questions using live context.",
        max_tokens=1024,
        temperature=0.3,
        top_p=0.8
    )

    result = await func.invoke_async(query, context=context)

    if not validate_response(result):
        return "⚠️ I couldn’t confidently answer based on reliable sources."

    return str(result)

