# planner.py — Modular Dispatcher for DefensaCopilot Agents

import asyncio
from semantic_kernel import KernelFunctionReference
from agents.disinfo_agent import disinfo_agent
from agents.policy_agent import policy_agent
from agents.threat_agent import threat_agent
from agents.live_intel_agent import live_intel_agent

# === Task planner and router ===
async def plan_and_run(question: str, kernel):
    """
    Routes the user question to the appropriate agent based on keywords.

    Args:
        question (str): The user-provided question.
        kernel: The Semantic Kernel instance.

    Returns:
        str: The response from the selected agent.
    """
    question_lower = question.lower()

    try:
        if "live" in question_lower or "update" in question_lower:
            return await live_intel_agent(question)
        elif any(kw in question_lower for kw in ["disinfo", "misinfo", "propaganda"]):
            return await disinfo_agent(question, kernel)
        elif any(kw in question_lower for kw in ["policy", "regulation", "legal"]):
            return await policy_agent(question, kernel)
        elif any(kw in question_lower for kw in ["threat", "attack", "risk"]):
            return await threat_agent(question, kernel)
        else:
            return "🤔 I'm not sure which agent should handle this question. Please rephrase or provide more context."

    except Exception as e:
        return f"❌ Agent execution failed: {e}"
