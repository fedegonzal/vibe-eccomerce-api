from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()

def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract and validate the bearer token from the Authorization header.
    This token will be used to isolate data between different students.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
