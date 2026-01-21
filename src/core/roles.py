from fastapi import Depends, HTTPException, status
from src.core.auth import AuthHandler

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
        self.auth_handler = AuthHandler()

    def __call__(self, user=Depends(AuthHandler().get_current_user)):
        if user.get("role") not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user
