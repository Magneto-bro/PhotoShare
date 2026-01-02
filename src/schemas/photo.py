from pydantic import BaseModel
from typing import List

class PhotoCreate(BaseModel):
    title: str
    description: str | None = None
    tags: List[str] = [] 

class PhotoUpdate(BaseModel):
    description: str
    
class TagResponse(BaseModel):
    id: int
    name: str    

class PhotoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    user_id: int
    tags: List[TagResponse] = []


    class Config:
        from_attributes = True