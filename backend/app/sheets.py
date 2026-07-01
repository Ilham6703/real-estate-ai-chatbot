"""
Google Sheets integration for lead storage.
"""

import logging
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from backend.app.config import settings

logger = logging.getLogger(__name__)

# =====================================================
# Google Sheets
# =====================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

_sheet = None


def get_sheet():
    """
    Return Google Sheet instance.
    """

    global _sheet

    if _sheet is not None:
        return _sheet

    credentials = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEET_ID,
    )

    _sheet = spreadsheet.sheet1

    return _sheet


# =====================================================
# Save Lead
# =====================================================

def save_lead(
    name: str,
    phone: str,
    requirement: str,
):
    """
    Save lead to Google Sheets.
    """

    try:

        sheet = get_sheet()

        sheet.append_row(

            [

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                name,

                phone,

                requirement,

            ],

            value_input_option="USER_ENTERED",

        )
        logger.info("Lead successfully saved to Google Sheets.")

        logger.info(
            "Saving lead: %s | %s | %s",
            name,
            phone,
            requirement,
        )

        return True

    except Exception as e:

        logger.exception(e)

        return False