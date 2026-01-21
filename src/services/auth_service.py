class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def register(self, data: dict):
        existing = await self.user_repo.find_by_email(data["email"])
        if existing:
            return False
        await self.user_repo.create_user(data)
        return True