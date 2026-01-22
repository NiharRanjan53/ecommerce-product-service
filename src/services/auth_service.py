from src.core.security import JWTService
from src.core.password_hasher import PasswordHasher
class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.jwt_service = JWTService()

    async def register(self, data: dict):
        existing = await self.user_repo.find_by_email(data["email"])
        if existing:
            return False
        
        data["password"] = PasswordHasher.hash(data["password"])
        await self.user_repo.create_user(data)
        
        return True
    
    async def login(self, mail: str, password: str):
        user = await self.user_repo.find_by_email(mail)

        if not PasswordHasher.verify(password, user["password"]):
            return None


        payload = {
            "user_id": str(user["_id"]),
            "role": user["role"]
        }
        return self.jwt_service.create_token(payload)
    