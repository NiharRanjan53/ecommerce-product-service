from src.schemas.tag_schema import TagInDB
from slugify import slugify

class TagService:
    def __init__(self, tag_repo):
        self.repository = tag_repo

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
    
    async def approve_tag(self, tag_id: str):
        print(f"Service {tag_id}")
        return await self.repository.approve_tag(tag_id)

    