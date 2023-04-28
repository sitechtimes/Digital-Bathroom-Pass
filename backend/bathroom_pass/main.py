from fastapi import FastAPI
import backend

app = FastAPI()

@app.get("/getStatus/{room_id}")
async def read_item(room_id):
    message = backend.readDoc(room_id)
    return {"message" : message}