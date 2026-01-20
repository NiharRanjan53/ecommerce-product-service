from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_tag():
    pass

@router.get("/")
def get_tag():
    pass