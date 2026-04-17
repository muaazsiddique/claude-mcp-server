# 🧠 Business Intelligence MCP Server

A custom **Model Context Protocol (MCP)** server that connects Claude Desktop (or any MCP-compatible AI client) to real-time business intelligence tools — company research, AI-powered lead scoring, personalized email drafting, CRM logging, and web research.

Built with Python, FastMCP, and integrated with OpenAI, SerpAPI, and Google Sheets.

---

## ✨ Demo

Type a natural language request in Claude Desktop or Claude Code:

> *"Research Systems Limited, score them as a lead, draft an outreach email, and log everything to my CRM."*

Claude automatically chains the right tools together:

1. **Researches** the company using web search
2. **Looks up** company details (industry, size, HQ, CEO)
3. **Scores** them as a lead (8/10 — strong AI focus, enterprise scale)
4. **Drafts** a personalized cold email referencing their recent achievements
5. **Logs** everything to a Google Sheets CRM with timestamp

All from a single natural language prompt — no manual steps.

---

## 🛠️ Tools

| Tool | Description | Powered By |
|------|-------------|------------|
| **Company Lookup** | Search for company details — industry, size, HQ, website, CEO | SerpAPI |
| **Lead Scorer** | AI scores a B2B lead 1–10 with confidence level and reasoning | OpenAI GPT-4o-mini |
| **Email Drafter** | Generates personalized cold outreach emails with subject lines | OpenAI GPT-4o-mini |
| **CRM Logger** | Logs scored leads to a Google Sheets CRM with timestamps | Google Sheets API |
| **Web Researcher** | Searches the web for recent news, results, and related questions | SerpAPI |

---

## 🏗️ Architecture

```
Claude Desktop / Claude Code (MCP Client)
        │
        ▼
   MCP Server (Python + FastMCP)
        │
        ├── lookup_company()    →  SerpAPI Google Search
        ├── score_lead()        →  OpenAI GPT-4o-mini
        ├── draft_email()       →  OpenAI GPT-4o-mini
        ├── log_to_crm()        →  Google Sheets API
        └── research_company()  →  SerpAPI Google Search
```

Communication uses **STDIO transport** with **JSON-RPC 2.0** protocol.

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/muaazsiddique/claude-mcp-server.git
cd claude-mcp-server
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp config/.env.example config/.env
```

Edit `config/.env` and add your keys:

```env
OPENAI_API_KEY=sk-your-key
SERPAPI_KEY=your-serpapi-key
GOOGLE_SHEETS_ID=your-spreadsheet-id
GOOGLE_CREDENTIALS_PATH=config/credentials.json
```

### 5. Set up Google Sheets CRM

1. Create a new Google Sheet with headers: `Timestamp | Company | Website | Industry | Score | Reason | Status`
2. Create a service account in Google Cloud Console
3. Download the credentials JSON and save as `config/credentials.json`
4. Share the Google Sheet with your service account email (Editor access)

### 6. Test the tools

```bash
python tests/test_tools.py
```

Expected output:
```
RESULTS: 5 passed, 0 failed out of 5
```

### 7. Connect to Claude Desktop

Add this to your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "business-intelligence": {
      "command": "python",
      "args": ["/full/path/to/claude-mcp-server/server.py"]
    }
  }
}
```

Restart Claude Desktop — your tools will appear automatically.

### 8. Connect to Claude Code (Alternative)

```bash
claude mcp add business-intelligence -- python /full/path/to/server.py
claude mcp list  # verify: should show ✓ Connected
```

---

## 📁 Project Structure

```
claude-mcp-server/
├── server.py                 # Main MCP server — registers all tools
├── tools/
│   ├── __init__.py           # Package init
│   ├── company_lookup.py     # SerpAPI company search
│   ├── lead_scorer.py        # OpenAI lead scoring
│   ├── email_drafter.py      # OpenAI email generation
│   ├── crm_logger.py         # Google Sheets CRM logging
│   └── web_researcher.py     # SerpAPI web research
├── config/
│   ├── .env.example          # Template for API keys
│   └── settings.py           # Server configuration
├── tests/
│   └── test_tools.py         # Smoke tests for all tools
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md
```

---

## ⚙️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Server language |
| FastMCP | MCP server framework |
| OpenAI GPT-4o-mini | AI-powered lead scoring and email generation |
| SerpAPI | Google Search API for company research |
| Google Sheets API | Lightweight CRM backend |
| Claude Desktop / Code | MCP client for testing and daily use |

---

## 💡 Example Prompts

Once connected, try these in Claude Desktop or Claude Code:

| Prompt | Tools Used |
|--------|-----------|
| *"Look up information about Techlogix"* | Company Lookup |
| *"Research recent news about AI in Pakistan"* | Web Researcher |
| *"Score Techlogix as a lead — they're in IT with 500+ employees"* | Lead Scorer |
| *"Draft a cold email to Systems Limited in IT Services"* | Email Drafter |
| *"Log Systems Limited to my CRM with score 8"* | CRM Logger |
| *"Research, score, email, and log Techlogix as a lead"* | All 5 tools chained |

---

## 🔑 API Keys Setup

| Service | Get Key | Free Tier |
|---------|---------|-----------|
| OpenAI | [platform.openai.com](https://platform.openai.com/api-keys) | $5 credit |
| SerpAPI | [serpapi.com](https://serpapi.com/manage-api-key) | 100 searches/month |
| Google Sheets | [console.cloud.google.com](https://console.cloud.google.com) | Free |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Server not found in Claude Desktop | Check config file path, restart Claude Desktop |
| Tools not showing up | Verify `@mcp.tool()` decorator on each function |
| STDIO corruption | Never use `print()` in server — use `logging` to stderr |
| API key errors | Check `.env` file is loaded, no trailing spaces in keys |
| Google Sheets permission denied | Share the sheet with service account email as Editor |
| CRM logger can't find credentials | Use absolute path in `GOOGLE_CREDENTIALS_PATH` |

---

## 📈 Use Cases

- **Sales teams** — Automate lead research, scoring, and outreach
- **Agencies** — Build AI-powered prospecting pipelines
- **Consultants** — Quickly research and qualify potential clients
- **Startups** — Lightweight CRM with AI-powered data entry

---

## 📄 License

MIT — use it, modify it, ship it.

---

## 👨‍💻 Author

**Muaaz Siddique** — AI Automation Developer

Building AI tools, MCP servers, and automation systems.

*If you'd like a custom MCP server for your business, feel free to reach out.*