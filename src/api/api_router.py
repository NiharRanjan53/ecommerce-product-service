from fastapi import FastAPI
from src.api.routes.auth_routes import AuthRouter
from src.api.routes.product_routes import ProductRouter
from src.api.routes import  tag_routs
def register_route(app: FastAPI):
    app.include_router(AuthRouter().router, prefix="/auth", tags=["auth"])
    app.include_router(ProductRouter().router, prefix="/products", tags=["products"])
    app.include_router(tag_routs.router, prefix="/tags", tags=["tags"])