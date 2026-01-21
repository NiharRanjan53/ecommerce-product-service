from fastapi import FastAPI
from src.api.routes.auth_routes import AuthRouter
from src.api.routes import product_routes, tag_routs
def register_route(app: FastAPI):
    app.include_router(AuthRouter().router, prefix="/auth", tags=["auth"])
    app.include_router(product_routes.router, prefix="/products", tags=["products"])
    app.include_router(tag_routs.router, prefix="/tags", tags=["tags"])