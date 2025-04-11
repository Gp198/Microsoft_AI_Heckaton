# DefensaCopilot - Main Orchestrator
# Powered by Azure OpenAI + Semantic Kernel + Modular Planning

import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from planner import plan_and_run
from agents.live_intel_agent import live_intel_agent

# === Load environment variables from the .env file ===
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# === Retrieve Azure OpenAI environment variables ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# === Validate that all required environment variables are present ===
if not all([OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_DEPLOYMENT]):
    raise EnvironmentError("❌ Error: Required environment variables not loaded from .env")

# === Initialize Semantic Kernel with Azure Chat Completion ===
kernel = Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name=OPENAI_DEPLOYMENT,
        endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    )
)

# === Chat interaction for Live Intel Agent ===
async def live_chat_mode():
    print("\n🧠 Live Intel Agent: Real-time defense intelligence at your service.")
    print("Type 'exit' to return to the main menu.\n")

    while True:
        user_input = input("🟡 Question: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            break

        try:
            response = await live_intel_agent(user_input, kernel)
            print(f"\n🤖 Response:\n{response}\n")
        except Exception as e:
            print(f"❌ Agent error: {e}")

# === Single-question interaction for other agents ===
async def single_query_mode():
    print("\n🧠 Multi-Agent Planner Mode")
    print("Type your question (or 'exit' to return to menu):\n")

    while True:
        query = input("🟡 Question: ")
        if query.strip().lower() in ["exit", "quit"]:
            break

        try:
            response = await plan_and_run(query)
            print(f"\n🤖 Agent Response:\n{response}\n")
        except Exception as e:
            print(f"❌ Error: {e}")

# === Main Application Loop ===
async def main():
    print("\n🛡️ Welcome to DefensaCopilot — your AI-powered defense assistant.")

    while True:
        print("\n🔘 Choose a mode:")
        print("1️⃣  Live Intelligence Chat Agent")
        print("2️⃣  Ask a single question to all agents")
        print("❌  Type 'exit' to quit")

        option = input("\n➡️ Select option (1/2/exit): ").strip().lower()

        if option in ["1", "live", "chat"]:
            await live_chat_mode()
        elif option in ["2", "multi", "question"]:
            await single_query_mode()
        elif option in ["exit", "quit"]:
            print("👋 Goodbye. Stay safe on your mission.")
            break
        else:
            print("⚠️ Invalid option. Please choose 1, 2 or 'exit'.")

# === Entry Point ===
if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
