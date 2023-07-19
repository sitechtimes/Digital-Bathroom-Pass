import gspread

google_account = gspread.service_account(filename='../sheets_credentials.json')
""" basement_sheets = google_account.open("Bathroom Pass Basement")
floor1_sheets = google_account.open("Bathroom Pass First Floor")
floor2_sheets = google_account.open("Bathroom Pass Second Floor")
floor3_sheets = google_account.open("Bathroom Pass Third Floor") """

""" all_sheets = [basement_sheets, floor1_sheets, floor2_sheets, floor3_sheets] """

sh = google_account.open("test gspread")
test_master_sheet = sh.get_worksheet(0)
room_range=range(51)

""" for x in room_range:
    sh.add_worksheet(title=str(x), rows=10000, cols=5) """

for x in room_range: 
    sh.get_worksheet(x + 1).update('D1', 'Timestamp')