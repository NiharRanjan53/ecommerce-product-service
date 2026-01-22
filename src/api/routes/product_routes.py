from fastapi import APIRouter, Depends
from src.core.role_checker import RoleChecker


class ProductRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.create_product, methods=["POST"], dependencies=[Depends(RoleChecker(["ADMIN", "SELLER", "admin"]))])

    async def create_product(self):
        return {"message":"create product"}
    def get_products(self):
        pass
    def delete_product(self):
        pass