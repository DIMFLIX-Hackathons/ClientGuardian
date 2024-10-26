from fastapi import HTTPException

invalid_token = HTTPException(detail="Invalid token", status_code=401)

not_allowed_extension = HTTPException(detail="extension not allowed", status_code=510)
