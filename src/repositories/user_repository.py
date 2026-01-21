from src.models.user_model import USER_COLLECTION

class UserRepository:
    def __init__(self, db):
        self.collection = db[USER_COLLECTION]

    async def find_by_email(self, email: str):
        return await self.collection.find_one({"email": email})
    
    async def create_user(self, user: dict):
        await self.collection.insert_one(user)