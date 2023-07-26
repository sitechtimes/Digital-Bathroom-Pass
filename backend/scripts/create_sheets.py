import gspread
import os
from dotenv import load_dotenv

load_dotenv()

google_account = gspread.service_account(filename='../sheets_credentials.json')
main_sheets = google_account.open_by_key(os.getenv('BATHROOM_PASS_MAIN_SHEET_KEY'))
shb = google_account.open_by_key(os.getenv('BATHROOM_PASS_BASEMENT_KEY'))
sh1 = google_account.open_by_key(os.getenv('BATHROOM_PASS_FIRST_FLOOR_KEY'))
sh2 = google_account.open_by_key(os.getenv('BATHROOM_PASS_SECOND_FLOOR_KEY'))
sh3 = google_account.open_by_key(os.getenv('BATHROOM_PASS_THIRD_FLOOR_KEY'))

