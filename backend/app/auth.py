from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from . import schemas, models, security, database

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):

    verify_email = db.query(
        models.User
        ).filter(
            models.User.email == user.email
            ).first()
    if verify_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed_password = security.get_password_hash(user.password)

    new_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):

    search_user = db.query(
        models.User
        ).filter(models.User.email == form_data.username
        ).first()
    if search_user is None:
        raise HTTPException(status_code=401, detail="Senha e/ou Email incorreto")
    is_password_correct = security.verify_password(form_data.password, search_user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Senha e/ou Email incorreto")
    token = security.create_access_token(data={"sub": search_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }