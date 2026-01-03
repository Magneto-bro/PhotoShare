from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    photo_id: int
    text: str

class CommentUpdate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    id: int
    photo_id: int
    user_id: int
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
