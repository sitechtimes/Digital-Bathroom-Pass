import gspread
import os
from dotenv import load_dotenv

load_dotenv()

google_account = gspread.service_account(filename='../sheets_credentials.json')
shb = google_account.open_by_key(os.getenv('BATHROOM_PASS_BASEMENT_KEY'))
sh1 = google_account.open_by_key(os.getenv('BATHROOM_PASS_FIRST_FLOOR_KEY'))
sh2 = google_account.open_by_key(os.getenv('BATHROOM_PASS_SECOND_FLOOR_KEY'))
sh3 = google_account.open_by_key(os.getenv('BATHROOM_PASS_THIRD_FLOOR_KEY'))

room_range=range(71)

testsheet = shb.worksheet("Test")

# room_worksheet = sh1.worksheet(str(100))
# status_cell = room_worksheet.find('available')
# body= ['','','','','available' ]

# adding new rows
# if status_cell.row == room_worksheet.row_count: 
#     room_worksheet.add_rows(1)
#     room_worksheet.update_cell(status_cell.row, status_cell.col, "unavailable")
#     room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
# else:
#     room_worksheet.update_cell(status_cell.row, status_cell.col, "unavailable")
#     room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")

print(len(testsheet.col_values(1)))
empty_row = len(testsheet.col_values(1)) + 1
testsheet.update_cell( empty_row, '1', "asadsfjf")

# worksheet.update_acell("A{}".format(next_row), "dfa")
# worksheet.update_acell("{}".format(next_row), "dfa")
