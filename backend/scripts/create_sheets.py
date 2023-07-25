import gspread
import os
from dotenv import load_dotenv

load_dotenv()

google_account = gspread.service_account(filename='../sheets_credentials.json')
shb = google_account.open_by_key(os.getenv('BATHROOM_PASS_BASEMENT_KEY'))
sh1 = google_account.open_by_key(os.getenv('BATHROOM_PASS_FIRST_FLOOR_KEY'))
sh2 = google_account.open_by_key(os.getenv('BATHROOM_PASS_SECOND_FLOOR_KEY'))
sh3 = google_account.open_by_key(os.getenv('BATHROOM_PASS_THIRD_FLOOR_KEY'))

basement_range = range(0, 58)
first_floor_range = range(100, 170)
second_floor_range = range(200, 270)
third_floor_range = range(300, 358)

testsheet = shb.worksheet("Test")

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

for x in basement_range:
    print(x)