from fastapi import APIRouter, HTTPException, Response, Request
from loader import crud
from typing import Optional

router = APIRouter()

invalid_token = HTTPException(detail='Invalid token', status_code=401)



async def check_token(token: Optional[str]) -> None:
    if not token:
        raise invalid_token
    
    checked = await crud.check_token(token)

    if not checked:
        raise invalid_token



@router.post("/auth")
async def auth(request: Request, response: Response):
    data = await request.json()

    if "token" not in data:
        raise invalid_token
    
    print(data)
    await check_token(data["token"])    
    response.set_cookie(key="token", value=data["token"], httponly=True)
    response.status_code = 200
    return response
    

@router.post("/is_authenticated")
async def is_authenticated(request: Request, response: Response):
    token = request.cookies.get("token")
    await check_token(token)
    response.status_code = 200
    return response