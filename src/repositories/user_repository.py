from datetime import datetime
from bson import ObjectId
from pymongo import ReturnDocument
from src.models.user_model import USER_COLLECTION
from src.schemas.auth_schema import UserInDB

class UserRepository:
    def __init__(self, db):
        self.collection = db[USER_COLLECTION]

    async def find_by_email(self, email: str):
        return await self.collection.find_one({"email": email})
    
    async def create_user(self, user: UserInDB):
        await self.collection.insert_one(user.dict())

    async def find_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def update(self, user_id: str, data: dict):
        data["updated_at"] = datetime.utcnow()
    
        # find_one_and_update returns the actual document (dict)
        return await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": data},
            # return_document=ReturnDocument.AFTER ensures you get the NEW data
            return_document=ReturnDocument.AFTER 
        )