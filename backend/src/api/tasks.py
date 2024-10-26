import json
from typing import List, Optional

import aiofiles
from config import allowed_extensions, path_to_originals
from database.models import Task, Token
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse
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
    return JSONResponse(json.dumps({"tasks": my_tasks}))
