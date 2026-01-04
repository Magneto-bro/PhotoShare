from pydantic import BaseModel

class PhotoCreate(BaseModel):
    description: str | None = None

class PhotoResponse(BaseModel):
    id: int
    image_url: str
    description: str

    class Config:
        from_attributes = True
