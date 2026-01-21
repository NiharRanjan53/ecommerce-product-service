from fastapi import FastAPI
from src.core.database import connect_db, close_db
from src.api.api_router import register_route

async def lifespan(app: FastAPI):
    # 🔹 STARTUP
    await connect_db()

    yield  # 👈 application runs here

    # 🔹 SHUTDOWN
    await close_db()


app = FastAPI(lifespan=lifespan)
register_route(app)

@app.get("/")
def health():
    return {"Status": "OK"}