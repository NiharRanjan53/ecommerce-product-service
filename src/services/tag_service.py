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

    