"""
DefensaCopilot — Planner Module
This module routes user queries to the appropriate specialized agent
based on keywords and context. It supports real-time news via RSS,
RAG, policy insights, misinformation checks, and threat detection.

Author: DefenseCopilot Team
"""

# === Imports ===
from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent
from agents.rag_agent import rag_agent
from agents.live_intel_agent import live_intel_agent  # 🔥 NEW live agent


# === Main Planning Function ===
async def plan_and_run(query: str, kernel=None) -> str:
    """
    Determines the most appropriate agent to handle the user's query
    and returns the agent's response.

    Args:
        query (str): User input question or task
        kernel (Kernel): Semantic Kernel instance used for LLM inference

    Returns:
        str: Response from the selected agent
    """
    query_lower = query.strip().lower()

    # ✅ Live News Agent (e.g. NATO activity, real-time events)
    if any(k in query_lower for k in ["live", "breaking", "update", "nato", "real-time"]):
        return await live_intel_agent(query, kernel)

    # 🛡 Threat Detection Agent
    elif any(k in query_lower for k in ["troop", "tank", "border", "attack", "drone", "movement"]):
        return await threat_agent(query)

    # 💼 Defense Policy Agent
    elif any(k in query_lower for k in ["policy", "budget", "spending", "defense law", "military reform"]):
        return await policy_agent(query)

    # ❌ Misinformation Check Agent
    elif any(k in query_lower for k in ["fake", "hoax", "rumor", "is it true", "disinformation"]):
        return await disinfo_agent(query)

    # 📄 Default fallback — Retrieval-Augmented Generation
    else:
        return await rag_agent(query)
