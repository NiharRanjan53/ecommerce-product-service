from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from src.enums.tag_types import TagType

class TagCreate(BaseModel):
    name: str
    type: TagType

class TagInDB(BaseModel):
    name: str
    slug: str
    type: TagType
    is_active: bool = True
    approved: bool = False
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)