from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True

class UserSettings(BaseModel):
    temp_threshold: int

class ClothingCreate(BaseModel):
    name: str
    category: str
    weather: str
    color: str
    style: str
    image_url: Optional[str] = None

class ClothingResponse(ClothingCreate):
    id: int
    usage_penalty: float
    class Config:
        from_attributes = True

class ClothingUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    weather: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None
    image_url: Optional[str] = None