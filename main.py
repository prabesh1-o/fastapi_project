from fastapi import FastAPI
from database import engine
from app import models
import os
from fastapi.responses import FileResponse

from app.users import router as users_router
from app.tasks import router as tasks_router

# create tables in thje database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task management",
    description="a simple backend project"

)

app.include_router(users_router)
app.include_router(tasks_router)

# @app.get("/favicon.ico")
# def favicon():
#     return FileResponse("favicon.ico")
@app.get("/",response_class=FileResponse)
def home():
    return FileResponse("index.html")
    # return {'message':"task app is running"}