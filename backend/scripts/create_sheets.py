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

basement_range = range(0, 59)
first_floor_range = range(100, 171)
second_floor_range = range(200, 271)
third_floor_range = range(300, 359)

master_sheet = sh3.worksheet("Master")

for x in third_floor_range:
    master_sheet.update_cell(x - 298, 1, x  )   


# testsheet = shb.worksheet("Test")

# adding completely new rows
# if status_cell.row == room_worksheet.row_count: 
#     room_worksheet.add_rows(1)
#     room_worksheet.update_cell(status_cell.row, status_cell.col, "unavailable")
#     room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
# else:
#     room_worksheet.update_cell(status_cell.row, status_cell.col, "unavailable")
#     room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")

# going to next available row
# print(len(testsheet.col_values(1)))
# empty_row = len(testsheet.col_values(1)) + 1
# testsheet.update_cell( empty_row, '1', "asadsfjf")

# deleting a row moving everything move up if needed
# testsheet.delete_row(var.row)