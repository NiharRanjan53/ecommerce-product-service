from slugify import slugify
from pymongo.errors import DuplicateKeyError
class TagRepository:
    def __init__(self, db):
        self.collection = db["tags"]
    async def create_tag(self, data:dict):
        data["slug"] = slugify(data["name"])
        existing = await self.collection.find_one({"slug": data["slug"]})
        if existing:
            return None

        try:
            await self.collection.insert_one(data)
            return True
        except DuplicateKeyError:
            return None
        

