from flask import Flask, render_template_string
import json
import os
import logging
import re
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load articles
try:
    with open("ai_signal_articles.json", "r") as f:
        articles = json.load(f)
except Exception as e:
    logging.error(f"Failed to load JSON: {e}")
    articles = []

# Clean and categorize articles
def clean_html(text):
    text = re.sub(r"<img[^>]+>", "", text)  # Remove img tags
    text = re.sub(r"<a [^>]+>(.*?)</a>", r"\1", text)  # Replace links with text
    text = re.sub(r"<[^>]+>", "", text)  # Strip remaining tags
    return text.strip()

def assign_priority(title):
    lowered = title.lower()

    high_keywords = ["military", "global", "artificial superintelligence"]
    medium_keywords = ["security", "risk", "safety", "ethics", "ai", "artificial intelligence", "agi"]
    low_keywords = ["photonic", "optical computing", "photonic chip", "quantum computing"]

    if any(keyword in lowered for keyword in high_keywords):
        return "high"
    elif any(keyword in lowered for keyword in medium_keywords):
        return "medium"
    else:
        return "low"  # Default to low if no high/medium match


for article in articles:
    summary = article.get("summary", "")
    summary = clean_html(summary)
    summary = "\n".join([line for line in summary.split("\n") if not line.strip().lower().startswith("the post")])
    article["summary"] = summary.strip()
    article["priority"] = assign_priority(article.get("title", ""))

# Group articles by priority
from collections import defaultdict
grouped_articles = defaultdict(list)
for article in articles:
    grouped_articles[article["priority"]].append(article)

# Sort groups: high → medium → low
ordered_priorities = ["high", "medium", "low"]
grouped_articles = {p: grouped_articles[p] for p in ordered_priorities if p in grouped_articles}

# Load last updated timestamp
try:
    with open("last_updated.txt", "r") as f:
        last_updated = f.read().strip()
except FileNotFoundError:
    last_updated = "Unknown"

@app.route("/")
def index():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Signal News Digest</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #222; }
            h2 { margin-top: 30px; color: #2c3e50; }
            .article { margin-bottom: 15px; }
            .article-title { font-size: 18px; font-weight: bold; }
            .summary { font-size: 15px; margin-top: 4px; color: #444; }
            .icon { vertical-align: middle; margin-right: 8px; }
        </style>
    </head>
    <body>
        <h1><span style="font-size: 2em;">🧠</span> AI Signal News Digest</h1>
        <p><em>Last updated: {{ last_updated }}</em></p>
        {% for priority, articles in grouped_articles.items() %}
            <h2>{{ priority.capitalize() }} Priority</h2>
            {% for article in articles %}
                <div class="article">
                    <div class="article-title">
                        <img class="icon" src="/static/priority_{{ article.priority }}.svg" width="16" height="16" />
                        <strong>{{ article.source }}:</strong>
                        <a href="{{ article.link }}" target="_blank">{{ article.title }}</a>
                    </div>
                    {% if article.summary %}
                        <div class="summary">{{ article.summary }}</div>
                    {% endif %}
                </div>
            {% endfor %}
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html_template, grouped_articles=grouped_articles, last_updated=last_updated)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
