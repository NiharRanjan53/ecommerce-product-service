from fastapi import FastAPI
from src.api.routes import auth_routes, product_routes, tag_routs
def register_route(app: FastAPI):
    app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
    app.include_router(product_routes.router, prefix="/products", tags=["products"])
    app.include_router(tag_routs.router, prefix="/tags", tags=["tags"])