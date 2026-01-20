from fastapi import FastAPI
from src.api.api_router import register_route

app = FastAPI()
register_route(app)
@app.get("/")
def health():
    return {"Status": "OK"}