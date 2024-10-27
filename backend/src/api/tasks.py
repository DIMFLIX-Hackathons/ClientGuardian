import os
import io
import shutil
import zipfile
from dataclasses import dataclass
from typing import List, Optional

import aiofiles
from config import allowed_extensions, path_to_originals
from database.models import Task, Token
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from loader import crud

from .utils.checked_auth_user import checked_auth_user
from .utils.errors import invalid_token, not_allowed_extension

router = APIRouter()


@dataclass
class FileInfo:
    name: str
    extension: str
    content: bytes


@router.post("/create_task")
async def create_task(
    request: Request,
    uploaded_files: list[UploadFile] = File(...),
    is_authenticated=Depends(checked_auth_user),
):
    if not is_authenticated:
        raise invalid_token

    token = request.cookies.get("token")
    token_info: Optional[Token] = await crud.get_token_info_by_token(token)

    if token_info is None:
        raise invalid_token

    files = {
        "Привязка ID": None,
        "Объёмы перевозок": None,
        "Обращения": None,
        "Интересы": None,
        "МС_Республика Чувашия": None,
        "МС_Республика Удмуртия": None,
        "МС_Республика Татарстан": None,
        "МС_Республика Мордовия": None,
        "МС_Республика Марий Эл": None,
        "МС_Нижегородская область": None,
        "МС_Кировская область": None,
        "МС_Владимирская область": None,
    }

    if len(uploaded_files) != len(files.keys()):
        raise HTTPException(
            status_code=400, detail="Not all required files were uploaded"
        )

    for file in uploaded_files:
        filename, extension = os.path.splitext(file)

        if extension not in allowed_extensions:
            raise not_allowed_extension

        if filename in files and files[filename] is not None:
            content = await file.read()
            files[filename] = FileInfo(
                name=filename, extension=extension, content=content
            )

    fs = [value for value in files.values() if value is not None]
    if len(fs) != len(files.keys()):
        raise HTTPException(status_code=400, detail="Not all files were uploaded")

    task_id = await crud.create_task(token_id=token_info.id)
    os.makedirs(path_to_originals / task_id, exist_ok=True)

    for file in fs:
        async with aiofiles.open(
            path_to_originals / task_id / f"{file.name}.{file.extension}", "wb"
        ) as buffer:
            await buffer.write(file.content)


@router.post("/get_my_tasks")
async def get_my_tasks(request: Request, is_authenticated=Depends(checked_auth_user)):
    if not is_authenticated:
        raise invalid_token

    token = request.cookies.get("token")
    token_info: Optional[Token] = await crud.get_token_info_by_token(token)

    if token_info is None:
        raise invalid_token

    my_tasks: List[Task] = await crud.get_my_tasks(token_info.id)
    return {"tasks": my_tasks}


@router.post("/get_original_unloading")
async def get_original_file(
    request: Request, is_authenticated=Depends(checked_auth_user)
):
    if not is_authenticated:
        raise invalid_token

    data = await request.json()
    task_id = data.get("task_id", "")

    result = await crud.get_task_by_id(task_id)

    if result is None:
        raise HTTPException(status_code=304, detail="task_id is undefined")

    foldername = path_to_originals / task_id
    if foldername.exists() and foldername.isdir():
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(str(foldername)):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, str(foldername)))

        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type='application/zip', headers={"Content-Disposition": "attachment; filename=archive.zip"})
    else:
        raise HTTPException(status_code=404, detail="task_id is undefined")


@router.post("/delete_task")
async def delete_task(request: Request, is_authenticated=Depends(checked_auth_user)):
    if not is_authenticated:
        raise invalid_token

    token = request.cookies.get("token")
    data = await request.json()
    task_id = data.get("task_id", "")

    token_info: Optional[Token] = await crud.get_token_info_by_token(token)

    if token_info is None:
        raise invalid_token
    
    folder_path = path_to_originals / task_id

    await crud.delete_task(token_info.id, task_id)
    
    if folder_path.exists() and folder_path.isdir():
        shutil.rmtree(folder_path)
