"""
Server configuration — reads from .env and provides defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
GOOGLE_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_CREDENTIALS_PATH", os.path.join(os.path.dirname(__file__), "credentials.json")
)

# Server settings
SERVER_NAME = "Business Intelligence Server"
SERVER_VERSION = "1.0.0"