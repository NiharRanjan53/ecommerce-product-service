from fastapi import APIRouter

class TagRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.create_tag, methods=["POST"])
        self.router.add_api_route("/", self.get_tags, methods=["GET"])
        # self.router.add_api_route("/", self.create_product, methods=["POST"], dependencies=[Depends(RoleChecker(["ADMIN", "SELLER"]))])
    async def create_tag(self):
        return  {"message": "create_tag"}
    async def get_tags(self):
        return {"message": "get_tag"}