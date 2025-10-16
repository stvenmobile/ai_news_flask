# AI News Flask

A Flask-based application to aggregate, process, and serve AI / tech news content. Built with Python 3.12, running via Docker, with a rebuild pipeline for content updates.

## Features

- Aggregates news (via RSS / other sources)  
- Processes / filters / classifies articles  
- Serves a web interface + API endpoints  
- Optional static generation, caching, reindexing  
- Dockerized for portability  

## Requirements

- Docker + Docker Compose (or Docker CLI)  
- Python 3.12 dependencies (in `requirements.txt`)  
- Sufficient storage & memory for news data  

## Getting Started (Development)

```bash
# Clone repo
git clone https://github.com/stvenmobile/ai_news_flask.git
cd ai_news_flask

# Build & run via Docker Compose
docker compose up --build

# Alternatively, if not using compose:
docker build -t ai_news_flask .
docker run -d -p 8000:8000 ai_news_flask
