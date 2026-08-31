from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from . import schemas, security, database

router = APIRouter()

@router.put("/auth/settings")
def settings(
    body: schemas.UserSettings,
    current_user = Depends(security.get_current_user),
    db: Session = Depends(database.get_db)
):

    current_user.temp_threshold = body.temp_threshold
    db.commit()
    return {"mensagem": f"Preferência atualizada para {body.temp_threshold} graus"}