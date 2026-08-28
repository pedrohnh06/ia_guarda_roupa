from app.models import User
from app.database import get_db
from datetime import datetime, timedelta, timezone
from jose import jwt 
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from . import database, models

SECRET_KEY = "chave-secreta-do-smartwardrobe-mude-depois"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_enconde = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"exp": expire})
    token_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload  = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM]) 
    email = payload.get("sub")
    if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    else:
        user = db.query(User).filter(email == User.email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user