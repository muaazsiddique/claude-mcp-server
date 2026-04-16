"""
Business Intelligence MCP Server
Built by Muaaz Siddique

A custom MCP server that gives Claude (or any MCP client) access to
business intelligence tools: company lookup, lead scoring, email drafting,
CRM logging, and web research.
"""

from mcp.server.fastmcp import FastMCP
import os
import sys
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "config", ".env"))

# Configure logging to stderr (NEVER use print — it corrupts STDIO transport)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# Import tool implementations
from tools.company_lookup import lookup_company_data
from tools.lead_scorer import score_lead_data
from tools.email_drafter import draft_email_data
from tools.crm_logger import log_to_crm_data
from tools.web_researcher import research_web

# Create the MCP server
mcp = FastMCP("Business Intelligence Server")


# ─── Tool 1: Company Lookup ─────────────────────────────────────────────────
@mcp.tool()
def lookup_company(company_name: str) -> str:
    """
    Look up detailed information about a company including industry,
    size, location, website, and description.

    Args:
        company_name: The name of the company to look up (e.g., "Techlogix")
    """
    logger.info(f"Tool called: lookup_company({company_name})")
    try:
        result = lookup_company_data(company_name)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"lookup_company failed: {e}")
        return json.dumps({"error": str(e), "company": company_name})


# ─── Tool 2: Lead Scorer ────────────────────────────────────────────────────
@mcp.tool()
def score_lead(
    company_name: str,
    industry: str,
    size: str,
    website: str = "",
) -> str:
    """
    Score a B2B lead from 1-10 based on company profile, industry fit,
    and potential for AI/automation services.

    Args:
        company_name: Name of the company
        industry: The company's industry (e.g., "Technology", "Healthcare")
        size: Company size (e.g., "50-200 employees", "Enterprise")
        website: Company website URL (optional)
    """
    logger.info(f"Tool called: score_lead({company_name})")
    try:
        result = score_lead_data(company_name, industry, size, website)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"score_lead failed: {e}")
        return json.dumps({"error": str(e), "company": company_name})


# ─── Tool 3: Email Drafter ──────────────────────────────────────────────────
@mcp.tool()
def draft_email(
    company_name: str,
    industry: str,
    context: str = "",
) -> str:
    """
    Write a personalized cold outreach email for a B2B prospect.

    Args:
        company_name: Name of the target company
        industry: The company's industry
        context: Additional context like recent news, pain points, or notes
    """
    logger.info(f"Tool called: draft_email({company_name})")
    try:
        result = draft_email_data(company_name, industry, context)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"draft_email failed: {e}")
        return json.dumps({"error": str(e), "company": company_name})


# ─── Tool 4: CRM Logger ─────────────────────────────────────────────────────
@mcp.tool()
def log_to_crm(
    company_name: str,
    website: str,
    industry: str,
    score: int,
    reason: str,
) -> str:
    """
    Log a scored lead to the Google Sheets CRM with all details.

    Args:
        company_name: Name of the company
        website: Company website URL
        industry: The company's industry
        score: Lead score from 1-10
        reason: Reasoning behind the score
    """
    logger.info(f"Tool called: log_to_crm({company_name}, score={score})")
    try:
        result = log_to_crm_data(company_name, website, industry, score, reason)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"log_to_crm failed: {e}")
        return json.dumps({"error": str(e), "company": company_name})


# ─── Tool 5: Web Researcher ─────────────────────────────────────────────────
@mcp.tool()
def research_company(query: str) -> str:
    """
    Search the web for recent information about a company or topic.
    Returns a summary of top search results.

    Args:
        query: Search query (e.g., "Techlogix Lahore recent news")
    """
    logger.info(f"Tool called: research_company({query})")
    try:
        result = research_web(query)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"research_company failed: {e}")
        return json.dumps({"error": str(e), "query": query})


# ─── Start the server ────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting Business Intelligence MCP Server...")
    mcp.run()