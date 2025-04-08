# DefensaCopilot - Setup Inicial (Semantic Kernel + Azure AI)

# Requisitos: semantic-kernel, azure-search-documents, openai, azure-functions, python-dotenv
# Instala com: pip install semantic-kernel openai azure-search-documents azure-functions python-dotenv

import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion

# Carregar variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# Inicializar Semantic Kernel com Azure OpenAI
kernel = Kernel()
kernel.add_text_completion_service(
    "azure-openai",
    OpenAITextCompletion(
        service_id="azure-openai",
        deployment_name=OPENAI_DEPLOYMENT,
        endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    )
)

# Definir planner simples
async def plan_and_run(query: str) -> str:
    if "fake news" in query.lower():
        return await disinfo_agent(query)
    elif any(k in query.lower() for k in ["troop", "tank", "border", "attack"]):
        return await threat_agent(query)
    elif any(k in query.lower() for k in ["policy", "defense budget", "spending"]):
        return await policy_agent(query)
    else:
        return "I'm not sure how to answer that. Please try rephrasing."

# Agente simulado 1: Ameaça
async def threat_agent(query: str) -> str:
    return "Simulated analysis: Increased troop movement observed near the eastern border. Source: NATO Report 2023."

# Agente simulado 2: Políticas de defesa
async def policy_agent(query: str) -> str:
    return "Defense budgets have increased by 12% in 2024 among EU countries. Source: EDA 2024 Data."

# Agente simulado 3: Verificação de desinformação
async def disinfo_agent(query: str) -> str:
    return "Claim: 'Country X is invading Country Y' - No credible sources confirm this. Marked as potential misinformation."

# Exemplo de execução
if __name__ == "__main__":
    import asyncio
    user_input = input("Pergunta: ")
    result = asyncio.run(plan_and_run(user_input))
    print("\nResposta do DefensaCopilot:\n", result)
