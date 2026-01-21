from fastapi import APIRouter, Depends, HTTPException
from src.schemas.auth_schema import RegisterRequest
from src.core.database import get_db
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository


class AuthRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route("/register", self.register, methods=["POST"])

    async def register(self, data : RegisterRequest , db = Depends(get_db)):
        service = AuthService(UserRepository(db))
        success = await service.register(data.dict())
        
        if not success:
            raise HTTPException(400, "User already exists")

        return {"message": "User registered successfully"}


