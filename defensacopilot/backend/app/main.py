# === DefensaCopilot - Main Orchestrator ===
# Powered by Azure OpenAI + Semantic Kernel + Modular Planning

# DefensaCopilot - Main Orchestrator
# Powered by Azure OpenAI + Semantic Kernel + Modular Planning

import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from planner import plan_and_run

# === Load environment variables from the .env file ===
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# === Retrieve Azure OpenAI environment variables ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# === Validate that all required environment variables are present ===
if not all([OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_DEPLOYMENT]):
    raise EnvironmentError("❌ ERROR: Missing one or more required environment variables in .env")

# === Initialize Semantic Kernel and AzureChatCompletion service ===
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=OPENAI_DEPLOYMENT,
        endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    ),
    service_id="azure-openai"
)

# === Main execution loop ===
async def main():
    print("\n🛡 Welcome to DefensaCopilot — your AI-powered defense assistant.")
    print("Type your defense-related question below (or 'exit' to quit):\n")

    while True:
        query = input("🌟 Question: ")
        if query.strip().lower() in ["exit", "quit"]:
            print("👋 Goodbye. Stay safe on your mission.")
            break

        try:
            response = await plan_and_run(query, kernel)
            print("\n🤖 Agent Response:")
            print(response)
        except Exception as e:
            print(f"❌ ERROR: {e}")

# === Entry point for script execution ===
if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
