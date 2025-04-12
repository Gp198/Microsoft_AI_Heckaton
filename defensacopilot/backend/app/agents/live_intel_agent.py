import feedparser
from datetime import datetime

# === Professional System Prompt for Live Intel Agent ===
SYSTEM_PROMPT = (
    "You are DefensaCopilot, a real-time defense intelligence advisor. "
    "Your mission is to provide concise, accurate updates from reliable open sources, such as NATO or globally trusted defense news. "
    "Avoid speculation, cite sources clearly, and always indicate if the information is based on available public reports. "
    "Never fabricate information and do not reference unknown or unverifiable sources."
)

# === RSS Feed Sources (can be expanded with more) ===
RSS_FEEDS = [
    "https://www.nato.int/cps/en/natolive/news.htm?format=rss",  # NATO Official
    "https://www.defensenews.com/arc/outboundfeeds/rss/category/news/",  # DefenseNews
    "https://www.armyrecognition.com/rss/armyrecognition_news.xml",  # Army Recognition
]

def fetch_latest_defense_news(limit=5):
    """
    Fetches the latest defense-related news from trusted RSS feeds.
    Returns a list of formatted strings with title and link.
    """
    headlines = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:limit]:
                published = entry.get("published", "")
                title = entry.get("title", "[No Title]")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                
                formatted_entry = f"\n📰 {title}\n🔗 {link}"
                if published:
                    formatted_entry += f"\n📅 Published: {published}"
                headlines.append(formatted_entry)
        except Exception as e:
            headlines.append(f"⚠️ Failed to parse feed {feed_url}: {e}")

    return headlines[:limit]

def get_live_intel_response():
    """
    Core agent method to generate the real-time defense response from RSS feeds.
    """
    context_snippets = fetch_latest_defense_news()
    return "\n\n".join(context_snippets)

# Optional: Direct test method
if __name__ == "__main__":
    print("\n📡 Fetching real-time defense updates...\n")
    print(get_live_intel_response())
