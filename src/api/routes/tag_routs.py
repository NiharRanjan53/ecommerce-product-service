from fastapi import APIRouter, Depends, HTTPException
from src.enums.roles import Role
from src.core.role_checker import RoleChecker
from src.schemas.tag_schema import TagCreate
from src.core.database import get_db
from src.core.auth import AuthHandler
from src.services.tag_service import TagService
from src.repositories.tag_repository import TagRepository

class TagRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.create_tag, methods=["POST"], dependencies=[Depends(RoleChecker([Role.ADMIN, Role.USER]))])
        self.router.add_api_route("/", self.get_tags, methods=["GET"])
        self.router.add_api_route("/{tag_id}/delete", self.delete_tag, methods=["DELETE"], dependencies=[Depends(RoleChecker([Role.ADMIN]))])
        self.router.add_api_route("/{tag_id}/approve", self.approve_tag, methods=['PUT'], dependencies=[Depends(RoleChecker([Role.ADMIN]))])
    async def create_tag(self, data :TagCreate, db = Depends(get_db), current_user=Depends(AuthHandler().get_current_user)):
        service = TagService(TagRepository(db))
        tag_data = data.dict()
        print(current_user)
        tag_data["created_by"] = current_user["user_id"]

        created = await service.create_tag(tag_data)
        if not created:
            raise HTTPException(400, "Tag already exists")

        return {"message": "Tag created"}

    async def get_tags(self):
        return {"message": "get_tag"}
    async def delete_tag(self):
        pass
    async def approve_tag(self, tag_id):
        pass