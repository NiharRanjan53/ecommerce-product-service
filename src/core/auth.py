from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from src.core.security import JWTService

class AuthHandler:
    security = HTTPBearer()

    def __init__(self):
        self.jwt_service = JWTService()

    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        token = credentials.credentials
        print(token)
        try:
            return self.jwt_service.decode_token(token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
