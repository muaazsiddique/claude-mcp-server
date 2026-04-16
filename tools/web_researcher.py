"""
Tool 5 — Web Researcher
Uses SerpAPI to search the web and return summarized results.
"""

import os
import requests


def research_web(query: str) -> dict:
    """Search the web for recent information using SerpAPI."""

    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return {
            "error": "SERPAPI_KEY not configured. Add it to config/.env",
            "query": query,
        }

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 8,
        "gl": "pk",  # Pakistan — change to your target market
    }

    try:
        response = requests.get(
            "https://serpapi.com/search", params=params, timeout=15
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {"error": f"SerpAPI request failed: {str(e)}", "query": query}

    # Extract organic results
    results = []
    for item in data.get("organic_results", [])[:5]:
        results.append(
            {
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "date": item.get("date", ""),
            }
        )

    # Extract news results if available
    news = []
    for item in data.get("news_results", [])[:3]:
        news.append(
            {
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "source": item.get("source", ""),
                "date": item.get("date", ""),
            }
        )

    # Extract "People Also Ask" for extra context
    related_questions = [
        q.get("question", "")
        for q in data.get("related_questions", [])[:3]
    ]

    return {
        "query": query,
        "organic_results": results,
        "news_results": news,
        "related_questions": related_questions,
        "total_results": data.get("search_information", {}).get(
            "total_results", "unknown"
        ),
        "source": "SerpAPI Google Search",
    }