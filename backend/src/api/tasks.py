import json
from typing import List, Optional

import aiofiles
from config import allowed_extensions, path_to_originals
from database.models import Task, Token
from fastapi import APIRouter, Depends, File, Request, UploadFile,HTTPException
from fastapi.responses import JSONResponse, FileResponse
from loader import crud

from .utils.checked_auth_user import checked_auth_user
from .utils.errors import invalid_token, not_allowed_extension

router = APIRouter()


@router.post("/create_task")
async def create_task(
    request: Request,
    files: list[UploadFile] = File(...),
    is_authenticated=Depends(checked_auth_user),
):
    if not is_authenticated:
        raise invalid_token

    token = request.cookies.get("token")
    token_info: Optional[Token] = await crud.get_token_info_by_token(token)

    if token_info is None:
        raise invalid_token

    for file in files:
        filename = file.filename
        extension = file.filename.split(".")[-1]

        if extension not in allowed_extensions:
            raise not_allowed_extension

        task_id = await crud.create_task(
            token_id=token_info.id, original_filename=filename
        )

        async with aiofiles.open(
            path_to_originals / f"{task_id}.{extension}", "wb"
        ) as buffer:
            content = await file.read()
            await buffer.write(content)


@router.post("/get_my_tasks")
async def get_my_tasks(request: Request, is_authenticated=Depends(checked_auth_user)):
    if not is_authenticated:
        raise invalid_token

    token = request.cookies.get("token")
    token_info: Optional[Token] = await crud.get_token_info_by_token(token)

    if token_info is None:
        raise invalid_token

    my_tasks: List[Task] = await crud.get_my_tasks(token_info.id)
    print(my_tasks)
    return {"tasks": my_tasks}



@router.post("/get_original_file")
async def get_original_file(request:Request, is_authenticated=Depends(checked_auth_user)):
    if not is_authenticated:
        raise invalid_token

    data = await request.json()
    task_id = data.get("task_id", "")
   

    result = await crud.get_original_file_path(task_id)

    if result is None:
         raise HTTPException(status_code=304, detail="task_id is undefined")   

    filename = task_id + "." + result.original_filename.split(".")[-1] 
    print(filename)

    if (path_to_originals / filename).exists():
        file_path = path_to_originals / filename
        print(file_path)
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)


@router.post("/delete_task")
async def delete_task(request:Request, is_authenticated=Depends(checked_auth_user)):
    if not is_authenticated:
        raise invalid_token
        
    token = request.cookies.get("token")

    data = await request.json()
    
    task_id = data.get("task_id", "")

    token_info: Optional[Token] = await crud.get_token_info_by_token(token)

    if token_info is None:
        raise invalid_token

    await crud.delete_task(token_info.id, task_id)

    
    
    
