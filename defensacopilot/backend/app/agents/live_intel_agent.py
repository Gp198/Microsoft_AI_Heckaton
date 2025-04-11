# === Live Intelligence Agent ===
# This agent fetches real-time defense-related news using RSS feeds
# and summarizes it using Azure OpenAI via Semantic Kernel

import feedparser
import datetime
from semantic_kernel import Kernel

# Define a set of trusted defense RSS feeds
RSS_FEEDS = [
    "https://www.nato.int/cps/en/natolive/news.rss",
    "https://www.defense.gov/Newsroom/News/Transcripts/Feed/",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.reutersagency.com/feed/?best-topics=defence&post_type=best",
    # Add more defense-related sources as needed
]

async def live_intel_agent(query: str, kernel: Kernel) -> str:
    """
    This agent gathers the latest defense intelligence using RSS feeds,
    filters based on the user's query, and summarizes key information
    using an LLM from Semantic Kernel.

    Args:
        query (str): The user's defense-related question.
        kernel (Kernel): Initialized Semantic Kernel with AzureChatCompletion.

    Returns:
        str: A concise summary or insight based on live sources.
    """

    if kernel is None:
        return "Live agent failed: Semantic Kernel instance not available."

    try:
        # Fetch the completion service from the Semantic Kernel
        completion = kernel.get_service("azure-openai")
        if completion is None:
            return "Live agent failed: LLM service not found in kernel."

        # Collect news items
        articles = []
        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # Combine title + summary to check if it's relevant
                text = f"{entry.title} {entry.get('summary', '')}".lower()
                if any(term in text for term in query.lower().split()):
                    date = entry.get("published", "Unknown date")
                    articles.append(f"[{date}] {entry.title}: {entry.link}")

        if not articles:
            return "No recent articles found matching the query."

        # Limit number of articles for summarization
        selected = "\n".join(articles[:5])

        # Prompt template to summarize
        prompt = (
            f"You are a defense analyst AI. Summarize the most critical insights from these updates:\n\n"
            f"{selected}\n\n"
            f"Focus on strategic movements, political implications, or military relevance."
        )

        # Call the LLM
        result = await completion.complete(prompt)
        return result.strip()

    except Exception as e:
        return f"Live intelligence agent failed: {e}"
