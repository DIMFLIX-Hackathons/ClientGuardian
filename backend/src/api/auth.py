from fastapi import Response, Request
from loader import crud

from .utils.errors import invalid_token
from .utils.routers import unprotected_api, protected_api


@unprotected_api.post("/auth")
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
    

@protected_api.post("/is_authenticated")
async def is_authenticated(response: Response):
    response.status_code = 200
    return response
