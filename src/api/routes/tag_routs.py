from fastapi import APIRouter, Depends
from src.core.role_checker import RoleChecker

class TagRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.create_tag, methods=["POST"])
        self.router.add_api_route("/", self.get_tags, methods=["GET"])
        self.router.add_api_route("/delete", self.delete_tag, methods=["DELETE"], dependencies=[Depends(RoleChecker(["ADMIN"]))])
    async def create_tag(self):
        pass
    async def get_tags(self):
        return {"message": "get_tag"}
    async def delete_tag(self):
        pass