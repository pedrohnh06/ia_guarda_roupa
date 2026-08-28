from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True

class ClothingCreate(BaseModel):
    name: str
    category: str
    weather: str

class ClothingResponse(ClothingCreate):
    id: int
    usage_penalty: float
    class Config:
        from_attributes = True