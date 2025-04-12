import feedparser

# === NATO RSS Feed URL ===
NATO_FEED_URL = "https://www.nato.int/cps/en/natolive/news.htm?rss=true"

# === Optional: Add additional trusted defense-related RSS feeds ===
TRUSTED_FEEDS = [
    NATO_FEED_URL,
    "https://www.defensenews.com/arc/outboundfeeds/rss/category/news/",
    "https://www.armyrecognition.com/rss/army_news.xml"
]

def get_defense_news(max_items=5):
    """
    Parses RSS feeds from trusted defense sources and returns the latest headlines with links.
    """
    news_entries = []

    for feed_url in TRUSTED_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_items]:
                news_entries.append(f"- {entry.title}\n  🔗 {entry.link}")
        except Exception as e:
            news_entries.append(f"⚠️ Failed to parse feed {feed_url}: {e}")

    if not news_entries:
        return "No recent defense news found from trusted sources."

    return "\n".join(news_entries[:max_items])
