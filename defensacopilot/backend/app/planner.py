# planner.py
# ----------------------------------------------------------------------------------
# Query Planner - Routes queries to the most appropriate agent
# Now includes live_intel_agent for real-time defense intelligence
# ----------------------------------------------------------------------------------

from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent
from agents.rag_agent import rag_agent
from agents.live_intel_agent import live_intel_agent  # ✅ NEW

# === Main dispatcher ===
async def plan_and_run(query: str) -> str:
    """
    Routes user input to the correct agent based on keywords and topic.

    Parameters:
        query (str): User input question.

    Returns:
        str: Agent response.
    """

    query_lower = query.lower()

    # === Real-time intelligence trigger ===
    if any(k in query_lower for k in [
        "nato update", "recent event", "latest news", "situation report", 
        "real-time", "current threat", "live", "now", "today"
    ]):
        return await live_intel_agent(query)

    # === Disinformation analysis ===
    elif "fake news" in query_lower or "misinformation" in query_lower:
        return await disinfo_agent(query)

    # === Threat analysis ===
    elif any(k in query_lower for k in ["troop", "tank", "border", "attack", "escalation"]):
        return await threat_agent(query)

    # === Defense policy ===
    elif any(k in query_lower for k in ["policy", "budget", "investment", "spending", "treaty"]):
        return await policy_agent(query)

    # === RAG for general document intelligence ===
    elif any(k in query_lower for k in ["report", "intel", "sipri", "eda", "capability"]):
        return await rag_agent(query)

    # === Default fallback ===
    else:
        return (
            "🤔 I'm not sure how to answer that. "
            "Try asking about real-time threats, defense budgets, or verified reports."
        )

