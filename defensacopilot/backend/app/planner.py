# planner.py - Orquestrador do DefensaCopilot

from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent

async def plan_and_run(query: str) -> str:
    """
    Decide qual agente deve tratar a pergunta com base em palavras-chave.
    """
    q = query.lower()

    if "fake news" in q or "disinformation" in q or "is it true" in q:
        return await disinfo_agent(query)
    elif any(word in q for word in ["troop", "border", "tank", "missile", "attack", "military"]):
        return await threat_agent(query)
    elif any(word in q for word in ["policy", "budget", "spending", "eu", "nato", "eda"]):
        return await policy_agent(query)
    else:
        return "I'm not sure how to help with that. Try asking about defense policies, threats or misinformation."
