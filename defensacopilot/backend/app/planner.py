# planner.py - Main agent orchestrator for DefensaCopilot

from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent
from agents.rag_agent import rag_agent

async def plan_and_run(query: str) -> str:
    """
    Analyzes the user query and routes it to the appropriate agent
    based on keywords and intent classification.
    """
    q = query.lower()

    # Handle misinformation or fact-checking queries
    if "fake news" in q or "disinformation" in q or "is it true" in q:
        return await disinfo_agent(query)

    # Handle military activity and threat detection queries
    elif any(word in q for word in ["troop", "border", "tank", "missile", "attack", "military"]):
        return await threat_agent(query)

    # Handle defense policy, budget, and geopolitical questions
    elif any(word in q for word in ["policy", "budget", "spending", "eu", "nato", "eda"]):
        return await policy_agent(query)

    # Fallback: use RAG to search indexed knowledge base for context
    elif any(word in q for word in ["intel", "report", "search", "document", "info"]):
        return await rag_agent(query)

    # Default response if no intent is matched
    return (
        "I'm not sure how to help with that.\n"
        "Try asking about defense threats, EU/NATO policy, misinformation, or intelligence reports."
    )
