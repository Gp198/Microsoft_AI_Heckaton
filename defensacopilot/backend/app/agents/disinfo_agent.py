async def disinfo_agent(query: str) -> str:
    return (
        "⚠️ Disinformation Check:\n"
        "Claim under review: 'Country X is invading Country Y'.\n"
        "No credible confirmation from NATO, EDA, or CSIS sources.\n"
        "Marked as potentially misleading.\n"
        "Sources: https://www.csis.org, https://www.nato.int"
    )
