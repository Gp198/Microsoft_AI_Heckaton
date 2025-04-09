# planner.py - Agente orquestrador do DefensaCopilot

from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent
from agents.rag_agent import rag_agent

# Função de planeamento e distribuição da consulta para o agente certo
async def plan_and_run(query: str) -> str:
    query_lower = query.lower()

    if "fake news" in query_lower or "misinformation" in query_lower:
        return await disinfo_agent(query)

    elif any(k in query_lower for k in ["troop", "tank", "border", "attack", "surveillance"]):
        return await threat_agent(query)

    elif any(k in query_lower for k in ["policy", "defense budget", "spending", "eda"]):
        return await policy_agent(query)

    elif any(k in query_lower for k in ["intel", "search", "report", "rag", "nuclear", "sipri"]):
        return await rag_agent(query)

    else:
        return "I'm not sure how to answer that. Please try rephrasing."
