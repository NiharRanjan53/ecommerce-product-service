from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Body, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.schemas.auth_schema import RegisterRequest, TokenResponse, UserUpdate
from src.core.database import get_db
from src.core.auth import AuthHandler
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository

router = APIRouter()

# --- Dependency Provider ---
# This is the "Industry Way": Decouple creation logic from the route
def get_auth_service(db= Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

# Using Annotated for cleaner, reusable dependencies (Modern FastAPI style)
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(
    data: RegisterRequest = Body(..., description="User registration details"),
    service: AuthServiceDep = None
):
    success = await service.register(data.model_dump())
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email/username already exists"
        )
    return {"status": "success", "message": "User registered successfully"}


@router.post(
    "/login", 
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    service: AuthServiceDep = None
):
    token = await service.login(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
    current_user = Depends(AuthHandler().get_current_user)
):
    return current_user


@router.put("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def update_profile(
    background_tasks: BackgroundTasks, # Injected by FastAPI
    # Path parameter validation
    user_id: str = Path(..., title="The ID of the user to update", min_length=24, max_length=24),
    # Body validation with partial update support
    data: UserUpdate = Body(..., description="Fields to update"),
    # Query parameter example (e.g., notifying user via email)
    notify: bool = Query(False, description="Whether to send a confirmation email"),
    service: AuthServiceDep = None,
    current_user = Depends(AuthHandler().get_current_user)
):
    # We pass background_tasks to the service so it can schedule the mail
    updated_user = await service.update_user_profile(
        requested_by=current_user,
        target_user_id=user_id,
        update_data=data,
        notify=notify,
        background_tasks=background_tasks 
    )
    
    # Return a structured response using the data returned from service
    return {
        "status": "success", 
        "message": "Profile updated",
        "data": {
            "user_id": user_id,
            "email": updated_user.get("email")
        },
        "notifications_triggered": notify
    }


# class AuthRouter:
#     def __init__(self):
#         self.router = APIRouter()

#         self.router.add_api_route("/register", self.register, methods=["POST"])
#         self.router.add_api_route("/login", self.login, methods=["POST"], response_model=TokenResponse)
#         self.router.add_api_route("/me", self.get_me, methods=['GET'])
#         self.router.add_api_route("/update-profile", self.update_profile, methods=["PUT"])

#     async def register(self, data : RegisterRequest , db = Depends(get_db)):
#         service = AuthService(UserRepository(db))
#         success = await service.register(data.dict())
        
#         if not success:
#             raise HTTPException(400, "User already exists")

#         return {"message": "User registered successfully"}
    
#     async def login(self,  form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
#         service = AuthService(UserRepository(db))
#         token = await service.login(form_data.username, form_data.password)
        
#         if not token:
#             raise HTTPException(401, "Invalid credentials")
        
#         return TokenResponse(access_token=token)
    
#     async def get_me(self, user = Depends(AuthHandler().get_current_user)):
#         return user

#     async def update_profile(self, data: UserUpdate, db=Depends(get_db), current_user=Depends(AuthHandler().get_current_user)):
#         service = AuthService(UserRepository(db))
#         print(current_user)
#         updated = await service.update_profile(current_user["user_id"], data.dict())

#         if not updated:
#             raise HTTPException(400, "Profile update failed")

#         return {"message": "Profile updated successfully"}
