# Запуск FastAPI
from fastapi import FastAPI
from src.routes import users, auth, admin , photo, profile



app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(admin.router, prefix="/api") 
app.include_router(photo.router, prefix="/api") 
app.include_router(profile.router, prefix="/api") 
