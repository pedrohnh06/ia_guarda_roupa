from pydantic import BaseModel, EmailStr

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

class ClothingResponse(ClothingCreate):
    id: int
    usage_penalty: float
    class Config:
        from_attributes = True
