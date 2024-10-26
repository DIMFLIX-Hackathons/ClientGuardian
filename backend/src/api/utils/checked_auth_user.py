from fastapi import Request
from loader import crud

from .errors import invalid_token


async def checked_auth_user(request: Request):
    token = request.cookies.get("token")
    print("DEPENDS   ", token)

    if not token:
        raise invalid_token

    checked = await crud.check_token(token)

    if not checked:
        raise invalid_token

    return True
