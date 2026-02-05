from pydantic import Field
from datetime import datetime
from src.core.security import JWTService
from src.core.password_hasher import PasswordHasher
from src.schemas.auth_schema import UserInDB

class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.jwt_service = JWTService()

    async def register(self, data: dict):
        existing = await self.user_repo.find_by_email(data["email"])
        if existing:
            return False
        
        # data["password"] = PasswordHasher.hash(data["password"])
        # data["role"] = data["role"].value
        user = UserInDB(
            name = data["name"],
            email = data["email"],
            password_hash = PasswordHasher.hash(data["password"]),
            role = data["role"].value,
        )
        await self.user_repo.create_user(user)

        return True
    
    async def login(self, mail: str, password: str):
        user = await self.user_repo.find_by_email(mail)

        if not PasswordHasher.verify(password, user["password_hash"]):
            return None


        payload = {
            "user_id": str(user["_id"]),
            "role": user["role"]
        }
        return self.jwt_service.create_token(payload)
    

    async def update_profile(self, user_id: str, data: dict):
        if data.get("password"):
            data["password_hash"] = PasswordHasher.hash(data.pop("password"))

        clean_data = {k: v for k, v in data.items() if v is not None}
        print(clean_data)

        return await self.user_repo.update_profile(user_id, clean_data)