# live_intel_agent.py — Real-time NATO News Agent with RSS Integration

import os
import feedparser
from dotenv import load_dotenv

# Load .env configuration for consistency if needed
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

# Top reputable military/geopolitical sources
RSS_FEEDS = [
    "https://www.nato.int/cps/en/natohq/106110.html",
    "https://www.reuters.com/live/",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1",
    "https://www.dw.com/pt-br/guerra-na-ucr%C3%A2nia/t-60942474",
]

def fetch_live_news_snippets(limit: int = 3) -> list:
    """
    Fetch the latest defense-related news headlines from trusted RSS feeds.
    Returns a list of strings with formatted summaries.
    """
    snippets = []
    seen_titles = set()

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "[No Title]").strip()
                if title in seen_titles:
                    continue

                summary = entry.get("summary", "No summary available.").split(".")[0].strip()
                link = entry.get("link", "")
                published = entry.get("published", "")
                
                snippet = f"• {title} ({published})\n  {summary}.\n  🔗 {link}"
                snippets.append(snippet)
                seen_titles.add(title)

                if len(snippets) >= limit:
                    return snippets

        except Exception as e:
            snippets.append(f"⚠️ Error fetching feed {url}: {e}")

    return snippets if snippets else ["⚠️ No live news available at this time."]
