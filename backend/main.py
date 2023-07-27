import gspread
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, Request
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel
load_dotenv()

google_account = gspread.service_account(filename="credentials.json")
main_sheets = google_account.open_by_key(os.getenv('BATHROOM_PASS_MAIN_SHEET_KEY'))
basement_sheets = google_account.open_by_key(os.getenv('BATHROOM_PASS_BASEMENT_KEY'))
floor1_sheets = google_account.open_by_key(os.getenv('BATHROOM_PASS_FIRST_FLOOR_KEY'))
floor2_sheets = google_account.open_by_key(os.getenv('BATHROOM_PASS_SECOND_FLOOR_KEY'))
floor3_sheets = google_account.open_by_key(os.getenv('BATHROOM_PASS_THIRD_FLOOR_KEY'))

main_master_sheet = main_sheets.get_worksheet(0)
allowed_email_sheet = main_sheets.get_worksheet(1)
currently_out_sheet = main_sheets.get_worksheet(2)
basement_master_sheet = basement_sheets.get_worksheet(0)
floor1_master_sheet = floor1_sheets.get_worksheet(0)
floor2_master_sheet = floor2_sheets.get_worksheet(0)
floor3_master_sheet = floor3_sheets.get_worksheet(0)

# room ranges for all floors
basement_range = range(0, 59)
first_floor_range = range(100, 171)
second_floor_range = range(200, 271)
third_floor_range = range(300, 359)

def get_room_status(room_number: int):
    cell = main_master_sheet.find(str(room_number))
    print(f"Cell found at {cell.row}, {cell.col}")
    is_available = main_master_sheet.cell(cell.row, cell.col + 1).value
    user_email = main_master_sheet.cell(cell.row, cell.col + 3).value
    return {
        "isAvailable": is_available,
        "userEmail": user_email
    }

def checkUserStatus(email: str) -> bool:
    email_cell = main_master_sheet.find(email)
    if email_cell is None:
        print("This user has not taken out a bathroom pass")
        return True
    else:
        
        pass_is_available = main_master_sheet.cell(email_cell.row, 2).value
        print(f"Pass is available: {pass_is_available}")
        if pass_is_available  == "FALSE":
            print("This user has already taken a bathroom pass")
            return False
        else:
            print("This user didn't take out a pass yet")
            return True

def update_status(room_number: int, change_to: bool, first_name: str, last_name: str, email: str):
    def update_sheets(room_worksheet, floor_master):
            status_cell = room_worksheet.find('available')
            print(f"Status cell for {room_number} found at row {status_cell.row}, column {status_cell.col}")
            # Adding the entry into the log, then move the status cell down one row
            log_cells = room_worksheet.range(f"A{status_cell.row}:E{status_cell.row}")
            log_values = [change_to, full_name, email, new_current_time, "unavailable"]
            for i, value in enumerate(log_values):
                log_cells[i].value = value

            # updating the master sheets in each individual floor
            floor_room_cell = floor_master.find(str(room_number))
            master_cell_list = floor_master.range(f"B{floor_room_cell.row}:D{floor_room_cell.row}")
            master_cell_values = [change_to, full_name, email]

            for i, value in enumerate(master_cell_values):
                master_cell_list[i].value = value

            floor_master.update_cells(master_cell_list) 

            # updating the individual cells in the individual sheets
            if status_cell.row == room_worksheet.row_count:
                room_worksheet.add_rows(1)
                room_worksheet.update_cells(log_cells)
                room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
            else:
                room_worksheet.update_cells(log_cells)
                room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
    if change_to == False:
        if checkUserStatus(email=email) == False:
            return({
                "message": "The user has already taken a pass out",
                "isAvailable": False
            })
    # Preventing user from changing to same boolean value for the room status
    current_status = str(change_to).upper()
    room_cell = main_master_sheet.find(str(room_number))
    is_available_value = main_master_sheet.cell(room_cell.row, room_cell.col + 1).value
    
    if is_available_value != current_status:

        print(f"Changing the availibility of room {room_number} from {is_available_value} to {change_to}")
        current_status = str(change_to).upper()
        # setting the current time to be more readable
        fmt = '%H:%M:%S'
        current_time = datetime.today()
        if current_time.hour > 12:
            time_tail = " PM"
            current_time = current_time - timedelta(hours=12)
            new_current_time = current_time.strftime(fmt) + time_tail
        else:
            time_tail =  " AM"
            new_current_time = current_time.strftime(fmt) + time_tail
        
        # Updating the values of the row associated with the room
        full_name = first_name + " " + last_name
        cell_list = main_master_sheet.range(f"B{room_cell.row}:D{room_cell.row}")
        cell_values = [change_to, full_name, email]
        
        for i, value in enumerate(cell_values):
            cell_list[i].value = value
        
        main_master_sheet.update_cells(cell_list)
        
        print("Updated master sheet")    

    #   Update the sheet of the corresponding room for the room log
        if room_number in basement_range:
            room_worksheet = basement_sheets.worksheet(str(room_number))
            floor_master = basement_sheets.get_worksheet(0)
            update_sheets(room_worksheet, floor_master)
        if room_number in first_floor_range:
            room_worksheet = floor1_sheets.worksheet(str(room_number))
            floor_master = floor1_sheets.get_worksheet(0)
            update_sheets(room_worksheet, floor_master)
        if room_number in second_floor_range: 
            room_worksheet = floor2_sheets.worksheet(str(room_number))
            floor_master = floor2_sheets.get_worksheet(0)
            update_sheets(room_worksheet, floor_master)
        if room_number in third_floor_range:
            room_worksheet = floor3_sheets.worksheet(str(room_number))
            floor_master = floor3_sheets.get_worksheet(0)
            update_sheets(room_worksheet, floor_master)
        
        if change_to == False: 
            next_row = len(currently_out_sheet.col_values(1)) + 1
            currently_out_sheet.update_cell(next_row, 1, full_name)
            currently_out_sheet.update_cell(next_row, 2, email)
            currently_out_sheet.update_cell(next_row, 3, new_current_time)
            currently_out_sheet.update_cell(next_row, 4, str(room_number)) 
        else:
            user_cell = currently_out_sheet.find(full_name)
            currently_out_sheet.delete_row(user_cell.row)
            currently_out_sheet.add_rows(1)
        return({
            "message": "Successfully updated bathroom pass log"
        })
    else:
        return({
            "message": "The bathroom pass is already in this state"
        })

def check_email_validity(email: str) -> bool:
    email_cell = allowed_email_sheet.find(email)
    if email_cell is None:
        return False
    else:
        return True

def authenticate_google(token: any):
    #Removing the double quotes in the token
    new_token = token.replace('"', "")
    
    try:
        id_info = id_token.verify_oauth2_token(new_token, requests.Request(), os.getenv('GOOGLE_OAUTH_CLIENT_ID')) 
        user_info = {
            "email": id_info["email"],
            "name": id_info["name"]
        }
        return user_info
    except ValueError:
        return "Invalid token provided!"

app = FastAPI()

allowed_origins = [
    "http://localhost",
    "http://localhost:8100",
    "http://localhost:8101",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_status/{room_id}")
async def read_item(room_id: int):
    data = get_room_status(room_id)
    return data

class Item(BaseModel):
    change_to: bool
    first_name: str
    last_name: str
    email: str

@app.patch("/change_status/{room_id}")
async def update_item(room_id: int, item: Item):
    in_range = 0 <= room_id <= 359
    if isinstance(item.change_to, bool) and in_range:
        valid_email = check_email_validity(item.email)
        if(valid_email):
            print(f"User has a valid email, attempting to update pass status for room {room_id}")
            result = update_status(room_id, item.change_to, item.first_name, item.last_name, item.email)
            return result
        else:
            return {
                "message": "The provided email address was invald. Please try again."
            }
    else:
        return {
            "message": "Something went wrong when changing pass status. Invalid change_to parameter or room_id."
        }

@app.post("/token_sign_in")
async def google_login(request: Request):
    header = request.headers.get('user_agent')
    return {
        "message": authenticate_google(token=header)
    }