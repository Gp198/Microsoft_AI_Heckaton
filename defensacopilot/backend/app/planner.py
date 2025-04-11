# planner.py — Modular Dispatcher for DefensaCopilot Agents

from agents.disinfo_agent import disinfo_agent
from agents.policy_agent import policy_agent
from agents.threat_agent import threat_agent
from agents.rag_agent import rag_agent
from agents.live_intel_agent import live_intel_agent

# === Main Routing Logic ===
async def plan_and_run(query: str, kernel=None) -> str:
    """
    Directs the user query to the appropriate agent based on keyword detection.

    Args:
        query (str): The user's question.
        kernel (Kernel): Optional Semantic Kernel instance for agents that require LLM services.

    Returns:
        str: Response from the selected agent.
    """
    query_lower = query.lower()

    # Conversational live news updates
    if any(k in query_lower for k in ["live", "real-time", "breaking", "nato", "update"]):
        return await live_intel_agent(query, kernel)

    # Disinformation analysis
    elif any(k in query_lower for k in ["fake news", "disinfo", "is it true", "rumor"]):
        return await disinfo_agent(query)

    # Threat analysis
    elif any(k in query_lower for k in ["troop", "attack", "missile", "border", "drone"]):
        return await threat_agent(query)

    # Policy and budget questions
    elif any(k in query_lower for k in ["budget", "policy", "spending", "treaty"]):
        return await policy_agent(query)

    # Default fallback to RAG-based document analysis
    else:
        return await rag_agent(query)
