# live_intel_agent.py — Real-time NATO News Agent with RSS + Azure OpenAI

import feedparser
from datetime import datetime, timedelta

# Top reputable military/geopolitical sources
RSS_FEEDS = [
    "https://www.nato.int/cps/en/natohq/106110.html",
    "https://www.reuters.com/live/",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1",
    "https://www.dw.com/pt-br/guerra-na-ucr%C3%A2nia/t-60942474",
]

def fetch_live_news_snippets(limit: int = 3) -> list[str]:
    """Fetches the latest news snippets from defense-related RSS feeds."""
    snippets = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                title = entry.title
                published = entry.get("published", "")
                summary = entry.get("summary", "").split(".")[0]
                link = entry.link

                snippet = f"{title} ({published}) – {summary}. Source: {link}"
                snippets.append(snippet)
        except Exception as e:
            snippets.append(f"⚠️ Failed to fetch from {url}: {e}")

    return snippets
