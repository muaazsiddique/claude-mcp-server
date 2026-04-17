# 🧠 Business Intelligence MCP Server

A custom **Model Context Protocol (MCP)** server that connects Claude Desktop (or any MCP-compatible AI client) to real-time business intelligence tools — company research, AI-powered lead scoring, personalized email drafting, CRM logging, and web research.

Built with Python, FastMCP, and integrated with OpenAI, SerpAPI, and Google Sheets.

---

## What It Does

Type a natural language request in Claude Desktop, and the AI automatically calls the right tools:

> *"Research Techlogix, score them as a lead, draft an outreach email, and log everything to my CRM."*

Claude will chain all 5 tools together to complete the entire workflow automatically.

---

## Tools

| Tool | Description | Powered By |
|------|-------------|------------|
| **Company Lookup** | Search for company details — industry, size, HQ, website | SerpAPI |
| **Lead Scorer** | AI scores a B2B lead 1–10 with reasoning | OpenAI GPT-4o-mini |
| **Email Drafter** | Generates personalized cold outreach emails | OpenAI GPT-4o-mini |
| **CRM Logger** | Logs scored leads to a Google Sheets CRM | Goo