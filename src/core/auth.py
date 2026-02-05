from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from src.core.security import JWTService
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
class AuthHandler:
    def __init__(self):
        self.jwt_service = JWTService()

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        try:
            return self.jwt_service.decode_token(token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
# auth_handler = AuthHandler()
