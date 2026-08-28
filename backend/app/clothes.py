from fastapi import APIRouter, Depends, HTTPException
from . import schemas, models, database, security
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session 

router = APIRouter(prefix="/clothes", tags=["Roupas"])

@router.post("/", response_model=schemas.ClothingResponse)
def create_clothings(
    clothing: schemas.ClothingCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):

    create_clothing = models.ClothingItem(
        name = clothing.name,
        category = clothing.category,
        weather = clothing.weather,
        owner_id = current_user.id
    )

    db.add(create_clothing)
    db.commit()
    db.refresh(create_clothing)

    return create_clothing

@router.get("/", response_model=list[schemas.ClothingResponse])
def get_clothings(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):

    return db.query(
        models.ClothingItem
        ).filter(
            models.ClothingItem.owner_id == current_user.id
            ).all()