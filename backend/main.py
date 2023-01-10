from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import string
import gspread
import time
import datetime;



gc = gspread.service_account(filename='credentials.json')
sh = gc.open("Bathroom Pass Testing")
worksheet1 = sh.get_worksheet(0)
worksheet2 = sh.get_worksheet(1)


room_range = range(100, 231)

def getStatus(roomNumber: string) -> string:
    findCell = worksheet1.find(roomNumber)
    return worksheet1.cell(findCell.row, findCell.col + 1).value

def updateStatus(roomNumber: string, changeTo: string, firstName: string, lastName: string, email: string) -> string:
    current_time = datetime.datetime.now()
    findCell = worksheet1.find(roomNumber)
    worksheet1.update_cell(findCell.row, findCell.col + 1, changeTo)
    worksheet1.update_cell(findCell.row, findCell.col + 2, firstName + " " + lastName)
    worksheet1.update_cell(findCell.row, findCell.col + 3, email)
    room_worksheet = sh.worksheet(roomNumber)
    worksheet_find_cell = room_worksheet.find('available')
    print(worksheet_find_cell.row, worksheet_find_cell.col)
    room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 4, changeTo)
    room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 3, firstName + " " + lastName)
    room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 2, email)
    room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col - 1, str(current_time))
    room_worksheet.update_cell(worksheet_find_cell.row + 1, worksheet_find_cell.col, 'available')
    room_worksheet.update_cell(worksheet_find_cell.row, worksheet_find_cell.col, 'unavailable')

    return("Successful")

def createEntry(roomNumber: string):
    findCell = worksheet1.find(roomNumber)
    worksheet1.update_cell(findCell.row, findCell.col + 1, "available")

def checkEmailValidity(email: string) -> bool:
    findCell = worksheet2.find(email)
    if findCell is None:
        return False
    else:
        return True

def delete_sheets():
    range1 = range(230, 230)
    for x in range1:    
        worksheet = sh.worksheet(str(x))
        sh.del_worksheet(worksheet)
        time.sleep(0.5)


def create_sheets():
    range1 = range(221, 230)
    for x in range1:
        worksheet = sh.add_worksheet(title=str(x), rows=10000, cols = 5)
        worksheet.update('A1', 'Status')
        worksheet.update('B1', 'Name')
        worksheet.update('C1', 'Email')
        worksheet.update('D1', 'Timestamp')


def update_sheets():
    range1 = range(100, 231)
    for x in range1:
        worksheet = sh.worksheet(str(x))
        worksheet.update('E1', '')
        time.sleep(0.7)



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

@app.get("/changeStatus/{room_id}/{change_to}/{first_name}/{last_name}/{email}")
async def changeStatus(room_id, change_to, first_name, last_name, email) :
    if (change_to == "true" or change_to == "false")  and (100<int(room_id)<232):
        if checkEmailValidity(email) == True:
            #There is a valid value for room_id and change_to value
            updateStatus(room_id, change_to, first_name, last_name, email)
            return {"message" : "successful"}
        else:
            return {"message" : "Email is not valid"}
    else:
        return{"message" : "Something went wrong. Either change_to parameter is not valid or room_id is not within specified range"}

@app.get("/deleteSheets")
async def deleteSheets():
    delete_sheets()
    return {"message" : "success"}


@app.get("/updateSheets")
async def updateSheets():
    update_sheets()
    return {"message" : "success"}

@app.get("/createSheets")
async def createSheets():
    create_sheets()
    return {"message" : "success"}