from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from models.intelligence import Intelligence

router = APIRouter(
    prefix="/intelligence",
    tags=["Intelligence"]
)


@router.get("/")
def get_intelligence(db: Session = Depends(get_db)):

    articles = (
        db.query(Intelligence)
        .order_by(
            Intelligence.dashboard_score.desc()
        )
        .all()
    )

    return articles