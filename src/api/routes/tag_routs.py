from fastapi import APIRouter, Depends, HTTPException
from fastapi import BackgroundTasks
from src.services.email_service import EmailService
from src.enums.roles import Role
from src.core.role_checker import RoleChecker
from src.schemas.tag_schema import TagCreate
from src.core.database import get_db
from src.core.auth import AuthHandler
from src.services.tag_service import TagService
from src.repositories.tag_repository import TagRepository
from src.repositories.user_repository import UserRepository
def serialize_tag(tag):
    tag["id"] = str(tag["_id"])
    tag.pop("_id")
    return tag
class TagRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.create_tag, methods=["POST"], dependencies=[Depends(RoleChecker([Role.ADMIN, Role.SELLER]))])
        self.router.add_api_route("/admin", self.get_all_tags, methods=["GET"], dependencies=[Depends(RoleChecker([Role.ADMIN]))])
        self.router.add_api_route("/", self.get_active_tags, methods=["GET"])
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

    async def get_all_tags(self, db=Depends(get_db)):
        service = TagService(TagRepository(db))
        # return await service.get_all_tags()
        tags = await service.get_all_tags()
        return [serialize_tag(tag) for tag in tags]

    async def get_active_tags(self, db=Depends(get_db)):
        service = TagService(TagRepository(db))
        tags =  await service.get_active_tags()
        return [serialize_tag(tag) for tag in tags]
    
    async def delete_tag(self, tag_id: str, db = Depends(get_db)):
        service = TagService(TagRepository(db))
        deleted = await service.delete_tag(tag_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Tag not found")

        return {"message": "Tag deactivated successfully"}

    async def approve_tag(self, tag_id: str, background_tasks: BackgroundTasks, db = Depends(get_db)):
        # print(tag_id)
        service = TagService(TagRepository(db), UserRepository(db))
        approved = await service.approve_tag(tag_id, background_tasks)
        if not approved:
            raise HTTPException(status_code=404, detail="Tag not found")

        return {"message": "Tag activated successfully"}

    
   