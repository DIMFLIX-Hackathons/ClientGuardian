from fastapi import APIRouter, Depends, Request, Response
from loader import crud

from .utils.checked_auth_user import checked_auth_user
from .utils.errors import invalid_token

router = APIRouter()


@router.post("/auth")
async def auth(request: Request, response: Response):
    token = (await request.json()).get("token", None)

    if not token:
        raise invalid_token

    checked = await crud.check_token(token)

    if not checked:
        raise invalid_token

    response.set_cookie(key="token", value=token, httponly=True)
    response.status_code = 200
    return response


@router.post("/is_authenticated")
async def is_authenticated(
    response: Response, is_authenticated=Depends(checked_auth_user)
):
    if is_authenticated:
        response.status_code = 200
        return response

    raise invalid_token
