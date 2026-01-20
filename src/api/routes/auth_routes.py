from fastapi import APIRouter
router = APIRouter()

@router.post("/signup")
def signup():
    return {"signup": "From Sign up route"}