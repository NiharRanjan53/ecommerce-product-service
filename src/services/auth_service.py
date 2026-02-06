from fastapi import HTTPException, status, BackgroundTasks
from src.core.security import JWTService
from src.core.password_hasher import PasswordHasher
from src.schemas.auth_schema import UserInDB, UserUpdate
from src.services.email_service import EmailService


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
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if not PasswordHasher.verify(password, user["password_hash"]):
            return None


        payload = {
            "user_id": str(user["_id"]),
            "role": user["role"]
        }
        return self.jwt_service.create_token(payload)
    

    async def update_user_profile(
        self, 
        requested_by: dict, 
        target_user_id: str, 
        update_data: UserUpdate,
        notify: bool,
        background_tasks: BackgroundTasks
    ):
        # 1. Business Validation (Ownership Check)
        if requested_by["user_id"] != target_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You do not have permission to update this profile"
            )

        # 2. Data Preparation
        payload = update_data.model_dump(exclude_unset=True)
        if not payload:
            raise HTTPException(status_code=400, detail="No update data provided")

        if "password" in payload:
            payload["password_hash"] = PasswordHasher.hash(payload.pop("password"))

        # 3. Database Operation
        updated_user = await self.user_repo.update(target_user_id, payload)
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 4. Background Job (Non-blocking)
        if notify:
            # We 'register' the task. It runs AFTER the return statement finishes.
            background_tasks.add_task(
                EmailService.send_profile_update_email,
                updated_user["email"],
                updated_user.get("name", "User")
            )

        return updated_user