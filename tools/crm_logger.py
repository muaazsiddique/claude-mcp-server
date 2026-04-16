"""
Tool 4 — CRM Logger
Logs scored leads to a Google Sheets spreadsheet acting as a simple CRM.
"""

import os
from datetime import datetime

# Google Sheets imports
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def _get_sheets_service():
    """Authenticate and return a Google Sheets API service object."""

    creds_path = os.getenv(
        "GOOGLE_CREDENTIALS_PATH",
        os.path.join(os.path.dirname(__file__), "..", "config", "credentials.json"),
    )

    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"Google credentials file not found at {creds_path}. "
            "Download it from Google Cloud Console → Service Accounts → Keys."
        )

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    return build("sheets", "v4", credentials=creds)


def log_to_crm_data(
    company_name: str,
    website: str,
    industry: str,
    score: int,
    reason: str,
) -> dict:
    """Append a lead row to the Google Sheets CRM."""

    sheet_id = os.getenv("GOOGLE_SHEETS_ID")
    if not sheet_id:
        return {
            "error": "GOOGLE_SHEETS_ID not configured. Add it to config/.env",
            "company": company_name,
        }

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        timestamp,
        company_name,
        website,
        industry,
        score,
        reason,
        "New",  # Status column
    ]

    try:
        service = _get_sheets_service()
        sheet = service.spreadsheets()

        # Append the row to the first sheet
        result = (
            sheet.values()
            .append(
                spreadsheetId=sheet_id,
                range="Sheet1!A:G",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": [row]},
            )
            .execute()
        )

        updated_range = result.get("updates", {}).get("updatedRange", "unknown")

        return {
            "status": "success",
            "company": company_name,
            "score": score,
            "row_range": updated_range,
            "timestamp": timestamp,
            "message": f"Lead '{company_name}' logged to CRM successfully.",
        }

    except FileNotFoundError as e:
        return {"error": str(e), "company": company_name}
    except Exception as e:
        return {
            "error": f"Google Sheets API failed: {str(e)}",
            "company": company_name,
        }