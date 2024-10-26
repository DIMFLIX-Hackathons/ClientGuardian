from fastapi import File, UploadFile
from .utils.routers import protected_api


@protected_api.post("/create_task")
async def create_task(files: list[UploadFile] = File(...)):
    for file in files:
        ...
