from fastapi import APIRouter, Depends
from . import schemas, models, database, security, services
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
        owner_id = current_user.id,
        color = clothing.color,
        style = clothing.style
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

@router.get("/recommend", response_model=list[schemas.ClothingResponse])
def recommend_outfit(
    city: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):

    generated_look = services.generate_outfit(
        current_user.id,
        city=city,
        threshold=current_user.temp_threshold,
        db=db)

    return generated_look