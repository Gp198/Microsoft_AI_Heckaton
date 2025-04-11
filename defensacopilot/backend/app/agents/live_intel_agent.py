# live_intel_agent.py — Live Defense Intelligence Agent with Web Context

import feedparser
from semantic_kernel.kernel import Kernel

# === Live Intelligence Agent ===
async def run_live_intel_agent(query: str, kernel: Kernel) -> str:
    try:
        # RSS feeds for defense-related news (you can add more sources)
        rss_feeds = [
            "https://www.nato.int/cps/en/natolive/news_rss.htm",
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://www.defense.gov/Newsroom/News/Transcripts/"  # adjust if needed
        ]

        # Extract entries from feeds
        all_entries = []
        for url in rss_feeds:
            feed = feedparser.parse(url)
            all_entries.extend(feed.entries[:5])  # Limit for performance

        # Concatenate headlines and summaries
        text_blob = "\n".join([f"{entry.title}: {entry.summary}" for entry in all_entries])

        # Format the final prompt
        prompt = (
            f"You are an intelligence officer. Based on the news excerpts below, respond professionally and concisely to the query.\n"
            f"News Excerpts:\n{text_blob}\n"
            f"User Question: {query}\n"
            f"Answer:"
        )

        # Use the correct service_id that was registered in main.py
        completion = await kernel.get_service("azure-openai").complete(prompt=prompt)
        return completion

    except Exception as e:
        return f"❌ Live intelligence agent failed: {e}"
