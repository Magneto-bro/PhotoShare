from pydantic import BaseModel


class PhotoCreate(BaseModel):
    title: str
    description: str | None = None

class PhotoUpdate(BaseModel):
    description: str

class PhotoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True