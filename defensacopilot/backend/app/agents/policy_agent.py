# policy_agent.py
# -----------------------------------------------------------------
# Defense Policy Agent - Simulates a policy-based response engine
# This module provides contextual answers based on defense budget,
# treaties, or policy-related topics.
# -----------------------------------------------------------------

async def policy_agent(query: str) -> str:
    """
    Simulates a response to a query about defense policy, budget,
    or strategic planning topics.

    Parameters:
        query (str): User input concerning defense policy matters.

    Returns:
        str: Policy analysis or statement.
    """
    # Static simulated response for demo purposes
    response = f"""
📘 Defense Policy Brief

📝 Question:
\"{query}\"

💬 Summary:
European defense budgets increased by an average of 12% in 2024, 
marking the highest regional investment since 2008.

📈 Trends:
- Increased NATO contributions.
- Rising investment in cyber defense and drones.
- Strategic reallocation from traditional to hybrid defense models.

📊 Source:
🗂 European Defence Agency (EDA), 2024 Public Report.

"""
    return response.strip()
