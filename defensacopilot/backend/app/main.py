# === DefensaCopilot - Main Orchestrator ===
# Powered by Azure OpenAI + Semantic Kernel + Modular Planning

import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from planner import plan_and_run

# === Load environment variables from .env ===
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# === Get OpenAI Azure credentials from environment ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# === Validate that required variables are available ===
if not all([OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_DEPLOYMENT]):
    raise EnvironmentError("❌ ERROR: Missing Azure OpenAI environment variables.")

# === Initialize Semantic Kernel with AzureChatCompletion ===
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        service_id="azure-openai",
        deployment_name=OPENAI_DEPLOYMENT,
        endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    )
)

# === Main application loop ===
async def main():
    print("\n🛡 Welcome to DefensaCopilot — your AI-powered defense assistant.")
    print("Type your defense-related question below (or 'exit' to quit):\n")

    while True:
        try:
            query = input("🌟 Question: ")
            if query.strip().lower() in ["exit", "quit"]:
                print("👋 Goodbye. Stay safe on your mission.")
                break

            response = await plan_and_run(query, kernel=kernel)
            print("\n🤖 Agent Response:\n" + response + "\n")

        except Exception as e:
            print(f"❌ Runtime error: {e}\n")

# === Run with async support (for Jupyter fallback) ===
if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
