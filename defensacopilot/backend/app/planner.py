# planner.py
# ----------------------------------------------------------------------------------
# Query Planner - Routes queries to the most appropriate agent
# Now includes live_intel_agent for real-time defense intelligence
# ----------------------------------------------------------------------------------

# planner.py — Modular Task Router for DefensaCopilot

# === Import AI agents ===
from agents.threat_agent import threat_agent
from agents.policy_agent import policy_agent
from agents.disinfo_agent import disinfo_agent
from agents.rag_agent import rag_agent
from agents.live_intel_agent import live_intel_agent  # ✅ NEW

# === Intelligent router to determine which agent to activate ===
async def plan_and_run(query: str) -> str:
    lower_q = query.lower()

    # 🧠 Dynamic intent classification by keyword patterns
    if "fake news" in lower_q or "misinformation" in lower_q or "is it true" in lower_q:
        return await disinfo_agent(query)

    elif any(term in lower_q for term in ["budget", "spending", "strategy", "policy", "defense plan"]):
        return await policy_agent(query)

    elif any(term in lower_q for term in ["troop", "attack", "border", "invasion", "missile", "alert"]):
        return await threat_agent(query)

    elif any(term in lower_q for term in ["nato", "ukraine", "russia", "breaking news", "live", "real-time", "update", "situation"]):
        return await live_intel_agent(query)  # ✅ NEW routing for live intelligence

    else:
        # Default fallback to document-grounded RAG agent
        return await rag_agent(query)
