from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status


credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class OAuth2Utils:
    def __init__(self, jwt_token_secret: str, access_token_exp: int, jwt_algorithm: str = "HS256") -> None:
        self.jwt_token_secret = jwt_token_secret
        self.access_token_exp = access_token_exp
        self.jwt_algorithm = jwt_algorithm

    @property
    def pwd_context(self) -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    def check_auth_token(self, token: str) -> dict:
        decoded = self.decode_token(token)
        try:
            if decoded is not None and "exp" in decoded and "username" in decoded:
                if datetime.utcnow() < datetime.fromtimestamp(decoded["exp"]):
                    return decoded
        except Exception:
            ...

        raise credentials_exc

    def decode_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                token, self.jwt_token_secret, algorithms=self.jwt_algorithm
            )
        except:
            return None

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        to_encode.update(
            {"exp": datetime.utcnow() + timedelta(minutes=self.access_token_exp)}
        )
        encoded_jwt = jwt.encode(
            to_encode, self.jwt_token_secret, algorithm=self.jwt_algorithm
        )
        return encoded_jwt
    
