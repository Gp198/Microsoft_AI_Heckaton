# DefensaCopilot - Main Orchestrator

# main.py – DefensaCopilot: Centralized Live Intelligence Agent (Azure OpenAI + RAG)

import os
import asyncio
from dotenv import load_dotenv
from agents.live_intel_agent import LiveIntelAgent

# === Load .env file from explicit path ===
env_path = "C:/Users/Utilizador/Documents/GitHub/Microsoft_AI_Heckaton/defensacopilot/backend/app/.env"
load_dotenv(dotenv_path=env_path)

# === Azure OpenAI environment variables ===
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not all([API_KEY, ENDPOINT, DEPLOYMENT]):
    raise EnvironmentError("\n❌ Missing Azure OpenAI credentials. Please check your .env file")

# === Initialize live intelligence agent ===
agent = LiveIntelAgent(
    api_key=API_KEY,
    endpoint=ENDPOINT,
    deployment=DEPLOYMENT
)

# === CLI interaction ===
async def main():
    print("\n\U0001F6E1 Welcome to DefensaCopilot – your live defense intelligence assistant")
    print("Type your defense-related question (or 'exit' to quit):")

    while True:
        query = input("\n\U0001F4AC Question: ")
        if query.strip().lower() in ["exit", "quit"]:
            print("\U0001F44B Goodbye. Stay safe.")
            break
        try:
            response = await agent.answer(query)
            print(f"\n\U0001F916 Response:\n{response}")
        except Exception as e:
            print(f"❌ Agent error: {e}")

if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())

    
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

