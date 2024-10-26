from fastapi import HTTPException

invalid_token = HTTPException(detail='Invalid token', status_code=401)
