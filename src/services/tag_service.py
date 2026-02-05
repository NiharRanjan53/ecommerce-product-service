from src.schemas.tag_schema import TagInDB
from slugify import slugify
from src.services.email_service import EmailService

class TagService:
    def __init__(self, tag_repo, user_repo=None):
        self.repository = tag_repo
        self.user_repo = user_repo

    async def create_tag(self, data:dict):
        print(data)
        tag = TagInDB(
            name=data["name"],
            slug=slugify(data["name"]),
            type=data["type"],             
            created_by=data["created_by"]   
        )
        return await self.repository.create_tag(tag.dict())
    
    async def delete_tag(self, tag_id: str):
        return await self.repository.delete_tag(tag_id)
    
    async def get_all_tags(self):
        return await self.repository.get_all_tags()

    async def get_active_tags(self):
        return await self.repository.get_active_tags()
    
    async def approve_tag(self, tag_id: str, background_tasks):
        tag = await self.repository.get_tag_by_id(tag_id)
        if not tag:
            return None

        await self.repository.approve_tag(tag_id)
        print(f"tag {tag}")
        creator = await self.user_repo.find_by_id(tag["created_by"])
        print(f"creator {creator}")
        if creator:
            background_tasks.add_task(
                EmailService.send_tag_approved_email,
                creator["email"],
                tag["name"]
            )
        return tag
        

    