from fastapi import FastAPI
from .routes import photos  

app = FastAPI()

app.include_router(photos.router) 