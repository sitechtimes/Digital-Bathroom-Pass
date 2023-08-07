from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes.api import router as api_routes
from dotenv import load_dotenv
import os
load_dotenv()

# The app serving our SPA
app = FastAPI()

allowed_origins = [
    "http://localhost",
    "http://localhost:8100",
    "http://localhost:1738",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dist_directory = os.path.join(os.path.dirname(__file__), '../bathroomPass/dist')
image_directory = os.path.join(os.path.dirname(__file__), '../bathroomPass/dist/images')
css_directory = os.path.join(os.path.dirname(__file__), '../bathroomPass/dist/css')
js_directory = os.path.join(os.path.dirname(__file__), '../bathroomPass/dist/js')

app.mount('/static', StaticFiles(directory=dist_directory), name='static')
app.mount('/images', StaticFiles(directory=image_directory), name='images')
app.mount('/css', StaticFiles(directory=css_directory), name='css')
app.mount('/js', StaticFiles(directory=js_directory), name='js')

@app.get('/')
async def return_app():
    return HTMLResponse(content=open(f"{dist_directory}/index.html").read())

@app.get('/pass')
async def return_app():
    return HTMLResponse(content=open(f"{dist_directory}/index.html").read())

@app.get('/home')
async def return_app():
    return HTMLResponse(content=open(f"{dist_directory}/index.html").read())

@app.get('/signin')
async def return_app():
    return HTMLResponse(content=open(f"{dist_directory}/index.html").read())

app.include_router(api_routes)