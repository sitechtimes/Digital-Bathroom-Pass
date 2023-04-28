from fastapi import FastAPI, Header
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import string
import gspread
import datetime;



gc = gspread.service_account(filename='credentials.json')
sh = gc.open("Bathroom Pass Testing")
worksheet1 = sh.get_worksheet(0)
worksheet2 = sh.get_worksheet(1)

room_range = range(100, 231)

def getStatus(roomNumber: string):
    findCell = worksheet1.find(roomNumber)
    return (worksheet1.cell(findCell.row, findCell.col + 1).value, worksheet1.cell(findCell.row, findCell.col + 2).value)

def checkUser(email: string) -> bool:
    emailCell = worksheet1.find(email)
    if emailCell is None:
        # The user has not taken a pass out yet
        print("This user has not taken a pass out yet")
        return False
    else:
        # The user has already taken a pass out before, check if they are trying to take another pass out while they already have a pass
        print(emailCell.row)
        print("email cell value = " + worksheet1.cell(emailCell.row, 2).value)
        if worksheet1.cell(emailCell.row, 2).value == "FALSE":
            # This user is trying to take another pass out
            print("This user has already taken a pass out")
            return False
        else:
            print("This user doesn't have an already taken pass")
            return True

def updateStatus(roomNumber: string, changeTo: string, firstName: string, lastName: string, email: string):
    if changeTo == "false":
        #Check if this user already has a pass
        if checkUser(email=email) == False:
            # The user already has a pass from another room
            return("User has already taken another pass out")

    # Find the room the user wants to check the pass out from
    findRoom_Main = worksheet1.find(roomNumber)
    currentValue = worksheet1.cell(findRoom_Main.row, findRoom_Main.col + 1).value
    print("changeToVal: " + currentValue)
    print("changeTo: " + changeTo)

    # Check if the change to value is equal to the already existing status of the room
    if currentValue != changeTo.upper():
        current_time = datetime.datetime.now()
        # Updating the values in the master sheet
        worksheet1.update_cell(findRoom_Main.row, findRoom_Main.col + 1, changeTo)
        worksheet1.update_cell(findRoom_Main.row, findRoom_Main.col + 2, firstName + " " + lastName)
        worksheet1.update_cell(findRoom_Main.row, findRoom_Main.col + 3, email)

        # Aquire the individual sheet of the room of which the status is being changed to log the new entry
        room_worksheet = sh.worksheet(roomNumber)
        worksheet_find_cell = room_worksheet.find('available')
        print(worksheet_find_cell.row, worksheet_find_cell.col)
         
        # Log the entry
        room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 4, changeTo)
        room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 3, firstName + " " + lastName)
        room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 2, email)
        room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 1, str(current_time))
        room_worksheet.update_cell(worksheet_find_cell.row + 1, worksheet_find_cell.col, 'available')
        room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col, 'unavailable')

        return("Successful")
    else:
        return("Attempting to change the status to the same value")

def createEntry(roomNumber: string):
    findCell = worksheet1.find(roomNumber)
    worksheet1.update_cell(findCell.row, findCell.col + 1, "available")

def checkEmailValidity(email: string) -> bool:
    findCell = worksheet2.find(email)
    if findCell is None:
        return False
    else:
        return True




# MARK: - GOOGLE SIGN IN METHODS:
from google.oauth2 import id_token
from google.auth.transport import requests

def authenticateGoogle(token: any):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), 100005545758663475318)
        return (idinfo['sub'])
    except ValueError:
        # Invalid token
        return ("Invalid Token")


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8100",
    "http://localhost:8101",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_status/{room_id}")
async def read_item(room_id):
    # message = backend.readDoc(room_id)
    # return {"message" : message}
    message = getStatus(room_id)
    return {"message" : message}

@app.get("/change_status/{room_id}/{change_to}/{first_name}/{last_name}/{email}")
async def change_status(room_id, change_to, first_name, last_name, email) :
    if (change_to == "true" or change_to == "false")  and (100<int(room_id)<232):
        if checkEmailValidity(email) == True:
            #There is a valid value for room_id and change_to value
            message = updateStatus(room_id, change_to, first_name, last_name, email)
            return {"message" : message}
        else:
            return {"message" : "Email is not valid"}
    else:
        return{"message" : "Something went wrong. Either change_to parameter is not valid or room_id is not within specified range"}

@app.post("/token_sign_in")
async def authenticate_google (user_agent: Annotated[str | None, Header()] = None):
    return {"Token": authenticateGoogle(token=user_agent)}