from fastapi import FastAPI, Header, Request
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import gspread
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests

google_account = gspread.service_account(filename="credentials.json")
sheets = google_account.open("Bathroom Pass Testing")

master_sheet = sheets.get_worksheet(0)
allowed_email_sheet = sheets.get_worksheet(1)
room_range = range(100, 231)

def get_room_status(room_number: int):
    cell = master_sheet.find(str(room_number))
    print(f"Cell found at {cell.row}, {cell.col}")
    is_available = master_sheet.cell(cell.row, cell.col + 1).value
    user_email = master_sheet.cell(cell.row, cell.col + 3).value
    return {
        "isAvailable": is_available,
        "userEmail": user_email
    }

def checkUserStatus(email: str) -> bool:
    email_cell = master_sheet.find(email)
    if email_cell is None:
        print("This user has not taken out a bathroom pass")
        return True
    else:
        
        pass_is_available = master_sheet.cell(email_cell.row, 2).value
        print(f"Pass is available: {pass_is_available}")
        if pass_is_available  == "FALSE":
            print("This user has already taken a bathroom pass")
            return False
        else:
            print("This user didn't take out a pass yet")
            return True


def update_status(room_number: int, change_to: bool, first_name: str, last_name: str, email: str):
    if change_to == False:
        if checkUserStatus(email=email) == False:
            return({
                "message": "The user has already taken a pass out",
                "isAvailable": False
            })
    # Preventing user from changing to same boolean value for the room status
    current_status = str(change_to).upper()
    room_cell = master_sheet.find(str(room_number))
    is_available_value = master_sheet.cell(room_cell.row, room_cell.col + 1).value
    
    if is_available_value != current_status:
        print(f"Changing the availibility of room {room_number} from {is_available_value} to {change_to}")
        current_status = str(change_to).upper()
        current_time = datetime.datetime.now()
        # Updating the values of the row associated with the room
        full_name = first_name + " " + last_name
        cell_list = master_sheet.range(f"B{room_cell.row}:D{room_cell.row}")
        cell_values = [change_to, full_name, email]
        
        for i, value in enumerate(cell_values):
            cell_list[i].value = value
        
        master_sheet.update_cells(cell_list)
        
    #    master_sheet.update(f"B{room_cell.row}:D{room_cell.row}", [change_to, full_name, email]) 
        print("Updated master sheet")
        # Update the sheet of the corresponding room for the room log
        room_worksheet = sheets.worksheet(str(room_number))
        print(room_worksheet)
        status_cell = room_worksheet.find('available')
        print(status_cell)
        print(f"Status cell for room {room_number} found at {status_cell.row} {status_cell.col}")

        # Adding the entry into the log, then move the status cell down one row
        log_cells = room_worksheet.range(f"A{status_cell.row}:E{status_cell.row}")
        log_values = [change_to, full_name, email, str(current_time), "unavailable"]
        
        for i, value in enumerate(log_values):
            log_cells[i].value = value
        
        room_worksheet.update_cells(log_cells)
        print(status_cell.row)
    #    room_worksheet.update(f"A{status_cell.row}:E{status_cell.row}", [change_to, full_name, email, str(current_time), "unavailable"])
        room_worksheet.update_cell(status_cell.row + 1, status_cell.col, "available")
        
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
        id_info = id_token.verify_oauth2_token(new_token, requests.Request(), '970810655131-49b3ktgaaf0jdm7f8gqvsab9hm4ri5bj.apps.googleusercontent.com') 
        user_info = {
            "email": id_info["email"],
            "name": id_info["name"]
        }
        return user_info
    except ValueError:
        return "Invalid token provided"

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

@app.get("/change_status/")
async def read_item(room_id: int, change_to: bool, first_name: str, last_name: str, email: str):
    is_in_range = (100 < room_id < 232)
    if isinstance(change_to, bool) and is_in_range:
        is_valid_email = check_email_validity(email)
        if is_valid_email == True:
            print("Email is valid")
            result = update_status(room_id, change_to, first_name, last_name, email)
            return result
        else:
            return {
                "message": "The provided email address is invalid"
            }
    else:
        return {
            "message": "Something went wrong. Invalid change_to parameter or room_id"
        }

@app.post("/token_sign_in")
async def login(request:Request):
    header = request.headers.get('user_agent')
    return {
        "message": authenticate_google(token=header)
    }