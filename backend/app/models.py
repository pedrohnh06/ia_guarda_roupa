# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey, Float
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    clothes = relationship("ClothingItem", back_populates="owner")
    temp_threshold = Column(Integer, default=22)

class ClothingItem(Base):
    __tablename__ = "clothes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    weather = Column(String)
    usage_penalty = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="clothes")
    color = Column(String)
    style = Column(String)