from slugify import slugify
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime, timezone
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
        
    async def delete_tag(self, tag_id: str):
        result = await self.collection.update_one(
            {"_id": ObjectId(tag_id)},
            {
                "$set": {
                    "is_active": False,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        # print(result)
        return result.modified_count > 0
    
    async def get_tag_by_id(self, tag_id: str):
        exist = await self.collection.find_one({"_id": ObjectId(tag_id)})
        if not exist:
            return None
        return exist 

    async def get_all_tags(self):
        return await self.collection.find().to_list(100)

    async def get_active_tags(self):
        return await self.collection.find({
            "is_active": True,
            "approved": True
        }).to_list(100)

    async def approve_tag(self, tag_id:str):
        print(tag_id)
        result = await self.collection.update_one(
            {"_id": ObjectId(tag_id)},
            {
                "$set": {
                    "is_active": True,
                    "approved": True,
                    "updated_at": datetime.now(timezone.utc)

                }
            }
        )
        # print(result)
        return result.modified_count > 0

