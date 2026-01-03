# Запуск FastAPI
from fastapi import FastAPI
from src.routes import users, auth, admin , photos



app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(admin.router, prefix="/api") 
app.include_router(photos.router, prefix="/api") 
