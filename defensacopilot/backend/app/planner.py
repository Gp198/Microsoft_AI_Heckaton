# === Planner ===
# This module acts as a simple rule-based dispatcher
# It selects the appropriate agent based on the user's query intent

from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent
from agents.rag_agent import rag_agent
from agents.live_intel_agent import live_intel_agent  # ✅ NEW agent

# === Dispatcher Function ===
async def plan_and_run(query: str, kernel=None) -> str:
    """
    Directs the query to the correct agent based on keywords.

    Args:
        query (str): User input question.
        kernel (Kernel): Optional Semantic Kernel instance for agents needing LLMs.

    Returns:
        str: Response from the selected agent.
    """
    q = query.lower()

    try:
        # === Agent Selection Logic ===

        # 1. Detect misinformation-related queries
        if any(term in q for term in ["fake news", "disinformation", "hoax"]):
            return await disinfo_agent(query)

        # 2. Detect threat-related queries
        elif any(term in q for term in ["troop", "missile", "attack", "border", "escalation"]):
            return await threat_agent(query)

        # 3. Detect policy-related queries
        elif any(term in q for term in ["budget", "spending", "defense policy", "nato summit"]):
            return await policy_agent(query)

        # 4. Detect intent for **live updates from real-time web sources**
        elif any(term in q for term in ["latest", "live", "real-time", "nato update", "breaking"]):
            return await live_intel_agent(query, kernel=kernel)

        # 5. Fallback to RAG-based general knowledge search
        else:
            return await rag_agent(query)

    except Exception as e:
        return f"❌ Planner failed to dispatch query: {e}"
