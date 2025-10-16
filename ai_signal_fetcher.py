import feedparser
from datetime import datetime
import json

# Add additional trusted feeds here
AI_FEEDS = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/news/feed.xml",
    "DeepMind": "https://www.deepmind.com/blog/feed.xml",
    "GoogleAI": "https://blog.google/technology/ai/rss/",
    "MetaAI": "https://ai.facebook.com/blog/rss/",
    "MicrosoftAI": "https://www.microsoft.com/en-us/research/feed/",
    "arXiv_ET": "https://export.arxiv.org/rss/cs.ET",
    "SciTechDaily": "https://feeds.feedburner.com/scitechdaily",
}

def fetch_articles(limit_per_feed=10):
    all_articles = []
    for source, url in AI_FEEDS.items():
        print(f"Fetching: {source}...")
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit_per_feed]:
            article = {
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", "No date"),
                "summary": entry.get("summary", ""),
                "source": source,
                "timestamp": datetime.utcnow().isoformat(),
                "novelty_score": None,         # Placeholder for classification
                "importance_score": None       # Placeholder for classification
            }
            all_articles.append(article)
    return all_articles



if __name__ == "__main__":
    articles = fetch_articles()
    with open("ai_signal_articles.json", "w") as f:
        json.dump(articles, f, indent=2)

    # Save a list of all article titles grouped by source
    from collections import defaultdict

    titles_by_source = defaultdict(list)
    for article in articles:
        titles_by_source[article["source"]].append(article["title"])

    with open("all_article_titles.json", "w") as f:
        json.dump(titles_by_source, f, indent=2)

    # Save the fetch timestamp
    with open("last_updated.txt", "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Saved {len(articles)} articles to ai_signal_articles.json")


