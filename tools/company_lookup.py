"""
Tool 1 — Company Lookup
Uses SerpAPI to search for company information and returns structured data.
"""

import os
import requests


def lookup_company_data(company_name: str) -> dict:
    """Search for company information using SerpAPI Google Search."""

    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return {
            "error": "SERPAPI_KEY not configured. Add it to config/.env",
            "company": company_name,
        }

    # Search for company info
    params = {
        "q": f"{company_name} company overview industry size employees",
        "api_key": api_key,
        "engine": "google",
        "num": 5,
    }

    try:
        response = requests.get(
            "https://serpapi.com/search", params=params, timeout=15
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {"error": f"SerpAPI request failed: {str(e)}", "company": company_name}

    # Extract knowledge graph if available
    knowledge = data.get("knowledge_graph", {})

    # Extract from organic results as fallback
    snippets = []
    for result in data.get("organic_results", [])[:3]:
        snippets.append(
            {
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", ""),
            }
        )

    return {
        "company": company_name,
        "knowledge_graph": {
            "title": knowledge.get("title", company_name),
            "description": knowledge.get("description", "Not found"),
            "website": knowledge.get("website", "Not found"),
            "type": knowledge.get("type", "Not found"),
            "headquarters": knowledge.get("headquarters", "Not found"),
            "founded": knowledge.get("founded", "Not found"),
            "employees": knowledge.get("employees", "Not found"),
            "ceo": knowledge.get("ceo", "Not found"),
        },
        "top_results": snippets,
        "source": "SerpAPI Google Search",
    }