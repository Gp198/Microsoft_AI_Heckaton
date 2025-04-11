# === Planner ===
# This module acts as a simple rule-based dispatcher
# It selects the appropriate agent based on the user's query intent

# planner.py — Orchestrates agent selection and delegation

from agents.disinfo_agent import disinfo_agent
from agents.policy_agent import policy_agent
from agents.threat_agent import threat_agent
from agents.rag_agent import rag_agent
from agents.live_intel_agent import live_intel_agent

# Main decision-making logic that delegates queries to the appropriate agent
async def plan_and_run(query: str) -> str:
    lowered_query = query.lower()

    # Check for disinformation-related topics
    if "fake news" in lowered_query or "disinfo" in lowered_query:
        return await disinfo_agent(query)

    # Check for live intel update requests
    elif any(kw in lowered_query for kw in ["live", "real-time", "breaking news", "updates"]):
        return await live_intel_agent(query)

    # Check for troop movements or military threats
    elif any(kw in lowered_query for kw in ["troop", "tank", "border", "attack", "drone"]):
        return await threat_agent(query)

    # Check for policy or budget-related questions
    elif any(kw in lowered_query for kw in ["policy", "defense budget", "spending", "strategy"]):
        return await policy_agent(query)

    # Default fallback to RAG agent (Azure Cognitive Search)
    else:
        return await rag_agent(query)
