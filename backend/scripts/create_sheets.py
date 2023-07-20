import gspread
import os
from dotenv import load_dotenv

load_dotenv()

google_account = gspread.service_account(filename='../sheets_credentials.json')
b_sh = google_account.open_by_key(os.getenv('BATHROOM_PASS_BASEMENT_KEY'))
sh1 = google_account.open_by_key(os.getenv('BATHROOM_PASS_FIRST_FLOOR_KEY'))
sh2 = google_account.open_by_key()
sh3 = google_account.open_by_key("Bathroom Pass Third Floor")

room_range=range(51)

#creating new sheets
# sh3.add_worksheet(title="Master", rows=51, cols=26)

# for x in room_range:
#     sh3.add_worksheet(title=str(x), rows=3, cols=5) 

# for x in room_range:  
#     sh3.get_worksheet(x + 47).update('A1', 'Status')
#     sh3.get_worksheet(x + 47).update('C1', 'Email')
#     sh3.get_worksheet(x + 47).update('D1', 'Timestamp')
#     sh3.get_worksheet(x + 47).update('B1', 'Name')

room_worksheet = sh1.worksheet(str(1))
status_cell = room_worksheet.find('available')
body= ['','','','','available' ]

try:
    if status_cell.row == room_worksheet.row_count: 
        room_worksheet.add_rows(1)
        room_worksheet.update_cell(status_cell.row, status_cell.col, "unavailable")
        room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
    else:
        room_worksheet.update_cell(status_cell.row, status_cell.col, "unavailable")
        room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
except:
    print('something went wrong')

